import httpx
from redis.asyncio import Redis
from app.services.football_service import FootballService
from app.core.config import settings

def get_football_service() -> FootballService:
    client = httpx.AsyncClient()
    redis = Redis.from_url(settings.redis_url)
    return FootballService(client=client, redis=redis)