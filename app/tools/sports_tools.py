from langchain_core.tools import tool
from app.services.football_service import FootballService
import httpx
import asyncio

football_service = FootballService(client=httpx.AsyncClient())

@tool
def get_live_scores(league_id:int | None = None) -> dict:
    """Fetch currently live football scores
    Use this when the user asks about ongoing or live matches.
    league_id is optional — pass it to filter by a specific league.
    """
    return asyncio.run(football_service.get_live_scores(league_id))

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