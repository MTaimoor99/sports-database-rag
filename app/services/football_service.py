import httpx
from app.core.config import settings

class FootballService:
    def __init__(self,client:httpx.AsyncClient):
        self.client = client
        self.base_url = settings.api_sports_base_url
        self.headers = {
            "x-apisports-key":settings.api_sports_key
        }

    async def get_live_scores(self, league_id: int | None = None)-> dict:
        params = {"live":"all"}
        if league_id:
            params["league_id"] = league_id

        response = await self.client.get(
            f"{self.base_url}/fixtures",
            headers = self.headers,
            params = params
        )
        response.raise_for_status()
        return response.json()    


    async def get_fixtures_by_date(self,date:str)->dict:
        pass
    
    async def get_team_recent_results(self, team_id: int) -> dict:
        pass

    async def search_team(self, name: str) -> dict:
        pass

