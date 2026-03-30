from fastapi import APIRouter
from pydantic import BaseModel

from app.models.query import QueryResponse,QueryRequest

router = APIRouter()

@router.post("/process-user-query", response_model=QueryResponse)
async def handle_query(request: QueryRequest):
    # LangGraph agent will be wired in here later
    return QueryResponse(answer=f"Received: {request.query}")