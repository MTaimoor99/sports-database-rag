from langchain_core.tools import tool
from app.services.football_service import FootballService
import httpx
import asyncio
from redis.asyncio import Redis
from app.core.config import settings
from app.scripts.populate_pinecone_index import embeddings, index

football_service = FootballService(
    client=httpx.AsyncClient(),
    redis=Redis.from_url(settings.redis_url)
)

#ReAct Tool
@tool
def get_live_scores(league_id:int | None = None) -> dict:
    """Fetch currently live football scores
    Use this when the user asks about ongoing or live matches.
    league_id is optional — pass it to filter by a specific league.
    """
    return asyncio.run(football_service.get_live_scores(league_id))

#RAG tool
@tool
def search_historical_data(query: str) -> dict:
    """
    Search historical football data for the current season.
    Use this when the user asks about past match results, team performance,
    or historical statistics from the current season.
    """
    query_vector = embeddings.embed_query(query)
    
    results = index.query(
        vector=query_vector,
        top_k=5,
        include_metadata=True
    )
    
    matches = [match["metadata"]["text"] for match in results["matches"]]
    
    return {"results": matches}

@tool
def get_fixtures_by_date(date: str) -> dict:
    """
    Fetch football fixtures for a specific date.
    Use this when the user asks about matches on a particular day.
    date format must be YYYY-MM-DD.
    """
    return asyncio.run(football_service.get_fixtures_by_date(date))

@tool
def get_team_recent_results(team_id: int) -> dict:
    """
    Fetch the last 5 results for a team.
    Use this when the user asks about a team's recent performance or form.
    """
    return asyncio.run(football_service.get_team_recent_results(team_id))

@tool
def search_team(name: str) -> dict:
    """
    Search for a team by name and return their ID and details.
    Use this first when the user mentions a team by name before calling other tools.
    """
    return asyncio.run(football_service.search_team(name))