from typing import TypedDict, Annotated
from langgraph.graph import StateGraph, END
from langgraph.graph.message import add_messages
from langchain_core.messages import BaseMessage

from langchain_google_genai import ChatGoogleGenerativeAI
from langchain_core.messages import SystemMessage
from app.core.config import settings
from langgraph.prebuilt import ToolNode

from app.tools.sports_tools import (
    get_live_scores,
    get_fixtures_by_date,
    get_team_recent_results,
    search_team,
)

class AgentState(TypedDict):
    messages: Annotated[list[BaseMessage], add_messages]

llm = ChatGoogleGenerativeAI(
    model = "gemini-3.1-flash-lite-preview",
    google_api_key = settings.google_api_key,
)
tools = [
    get_live_scores,
    get_fixtures_by_date,
    get_team_recent_results,
    search_team,
]
llm_with_tools = llm.bind_tools(tools)

SYSTEM_PROMPT = """You are a sports assistant with access to live and historical sports data.
When a user asks about scores, fixtures, or team performance, use the available tools to fetch real data.
Never make up scores or statistics."""

def should_continue(state:AgentState):
    last_message = state['messages'][-1]
    if last_message.tool_calls:
        return "tools"
    return END

def agent_node(state:AgentState) -> AgentState:
    messages = [SystemMessage(content=SYSTEM_PROMPT)] + state['messages']
    response = llm_with_tools.invoke(messages)
    return {"messages":response}

tool_node = ToolNode(tools)

#Building the graph
graph_builder = StateGraph(AgentState)

graph_builder.add_node("agent",agent_node)
graph_builder.add_node("tools",tool_node)

graph_builder.set_entry_point("agent")

graph_builder.add_conditional_edges(
    "agent",
    should_continue,
)

graph_builder.add_edge("tools","agent")
graph = graph_builder.compile()