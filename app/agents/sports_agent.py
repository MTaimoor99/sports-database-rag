from typing import TypedDict, Annotated
from langgraph.graph import StateGraph, END
from langgraph.graph.message import add_messages
from langchain_core.messages import BaseMessage

from langchain_google_genai import ChatGoogleGenerativeAI
from langchain_core.messages import SystemMessage
from app.core.config import settings
from langgraph.prebuilt import ToolNode

class AgentState(TypedDict):
    messages: Annotated[list[BaseMessage], add_messages]

llm = ChatGoogleGenerativeAI(
    model = "gemini-3.1-flash-lite-preview",
    google_api_key = settings.google_api_key,
)

SYSTEM_PROMPT = """You are a sports assistant with access to live and historical sports data.
When a user asks about scores, fixtures, or team performance, use the available tools to fetch real data.
Never make up scores or statistics."""

def agent_node(state:AgentState) -> AgentState:
    messages = [SystemMessage(content=SYSTEM_PROMPT)] + state['messages']
    response = llm.invoke(messages)
    return {"messages":response}

def tool_node():
    pass