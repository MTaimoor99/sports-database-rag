import httpx
import json
import time
from redis.asyncio import Redis
from app.core.config import settings
from constants import LIVE_SCORES_TTL

class FootballService:
    def __init__(self, client: httpx.AsyncClient, redis: Redis):
        self.client = client
        self.redis = redis
        self.base_url = settings.api_sports_base_url
        self.headers = {
            "x-apisports-key": settings.api_sports_key
        }

    async def get_live_scores(self, league_id: int | None = None) -> dict:
        cache_key = f"live_scores:{league_id or 'all'}"

        redis_start = time.time()
        cached = await self.redis.get(cache_key)
        if cached:
            return json.loads(cached)

        params = {"live": "all"}
        if league_id:
            params["league"] = league_id

        response = await self.client.get(
            f"{self.base_url}/fixtures",
            headers=self.headers,
            params=params
        )
        response.raise_for_status()
        json_response = response.json()

        await self.redis.setex(cache_key, LIVE_SCORES_TTL, json.dumps(json_response))
        return json_response


    async def get_fixtures_by_date(self, date: str) -> dict:
        async with httpx.AsyncClient() as client:
            response = await client.get(
                f"{settings.api_sports_base_url}/fixtures",
                headers={"x-apisports-key": settings.api_sports_key},
                params={"date": date}
            )
            response.raise_for_status()
            return response.json()

    async def get_team_recent_results(self, team_id: int) -> dict:
        async with httpx.AsyncClient() as client:
            response = await client.get(
                f"{settings.api_sports_base_url}/fixtures",
                headers={"x-apisports-key": settings.api_sports_key},
                params={
                    "team": team_id,
                    "last": 5
                }
            )
            response.raise_for_status()
            return response.json()

    async def search_team(self, name: str) -> dict:
        async with httpx.AsyncClient() as client:
            response = await client.get(
                f"{settings.api_sports_base_url}/teams",
                headers={"x-apisports-key": settings.api_sports_key},
                params={"search": name}
            )
            response.raise_for_status()
            return response.json()

