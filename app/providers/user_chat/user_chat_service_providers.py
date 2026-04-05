import httpx
from app.services.football_service import FootballService

def get_football_service() -> FootballService:
    client = httpx.AsyncClient()
    return FootballService(client=client)