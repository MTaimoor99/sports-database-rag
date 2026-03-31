from langchain_google_genai import ChatGoogleGenerativeAI
from langchain.agents import create_agent
from app.core.config import settings
from app.agents.sports_agent import graph
class UserChatService:
    async def process_user_query(self,query:str)->str:
        result = await graph.ainvoke(
            {
                "messages":[{"role":"user","content":query}]
            }
        )
        return result["messages"][-1].content