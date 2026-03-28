from fastapi import APIRouter
from pydantic import BaseModel

router = APIRouter()

class QueryRequest(BaseModel):
    query: str

class QueryResponse(BaseModel):
    answer: str

@router.post("/query", response_model=QueryResponse)
async def handle_query(request: QueryRequest):
    # LangGraph agent will be wired in here later
    return QueryResponse(answer=f"Received: {request.query}")