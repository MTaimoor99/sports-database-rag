import asyncio
from pinecone import Pinecone
from langchain_google_genai import GoogleGenerativeAIEmbeddings
from app.core.config import settings
import httpx
from app.utils.get_current_season import get_current_season
from constants import PREMIER_LEAGUE_ID, PRIORITY_LEAGUE_IDS

#Initialization logic
pc = Pinecone(api_key=settings.pinecone_api_key)
index = pc.Index(settings.pinecone_index_name)

#Initialize Gemini Embeddings
embeddings = GoogleGenerativeAIEmbeddings(
    model = "models/gemini-embedding-2",
    google_api_key=settings.google_api_key,
    output_dimensionality=768
)

async def fetch_league_fixtures(client: httpx.AsyncClient, league_id: int) -> list[dict]:
    response = await client.get(
        f"{settings.api_sports_base_url}/fixtures",
        headers={"x-apisports-key": settings.api_sports_key},
        params={
            "league": league_id,
            "season": get_current_season(),
            "status": "FT"
        }
    )
    response.raise_for_status()
    data = response.json()
    print(f"League {league_id}: fetched {len(data['response'])} fixtures")
    return data["response"]

#Function for concurrent fetching of league fixtures.
async def fetch_historical_fixtures() -> list[dict]:
    async with httpx.AsyncClient() as client:
        results = await asyncio.gather(
            *[fetch_league_fixtures(client, league_id) for league_id in PRIORITY_LEAGUE_IDS]
        )
    
    fixtures = []
    for result in results:
        fixtures.extend(result)
    return fixtures

def fixture_to_text(fixture:dict) -> str:
    #Converting JSON fixture to readable text chunk, placeholder for now
    home_team = fixture["teams"]["home"]["name"]
    away_team = fixture["teams"]["away"]["name"]
    home_score = fixture["goals"]["home"]
    away_score = fixture["goals"]["away"]
    date = fixture["fixture"]["date"][:10]  # YYYY-MM-DD
    league = fixture["league"]["name"]
    season = fixture["league"]["season"]
    status = fixture["fixture"]["status"]["long"]

    return (
        f"{home_team} vs {away_team} on {date}. "
        f"League: {league}, Season: {season}. "
        f"Final Score: {home_team} {home_score} - {away_score} {away_team}. "
        f"Status: {status}."
    )

async def populate_db():
    fixtures = await fetch_historical_fixtures()

    vectors = []

    for fixture in fixtures:
        fixture_id = str(fixture["fixture"]["id"])
        # Skip if already exists in Pinecone
        existing = index.fetch(ids=[fixture_id])
        if existing.vectors:
            print(f"Skipping {fixture_id}, already exists")
            continue

        text = fixture_to_text(fixture)
        vector = embeddings.embed_query(text)
        vectors.append({
            "id": fixture_id,
            "values": vector,
            "metadata": {"text": text}
        })

    # Batch upsert
    batch_size = 100
    for i in range(0, len(vectors), batch_size):
        batch = vectors[i:i + batch_size]
        index.upsert(vectors=batch)
        print(f"Upserted batch {i // batch_size + 1} of {len(vectors) // batch_size + 1}")


if __name__=="__main__":
    asyncio.run(populate_db())
