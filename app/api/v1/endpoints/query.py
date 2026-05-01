from fastapi import APIRouter, Depends
from pydantic import BaseModel

from app.models.request_response.query import QueryResponse, QueryRequest, ContentBlock
from app.services.user_chat_service import UserChatService
from app.providers.user_chat.user_chat_api_providers import get_user_chat_service

router = APIRouter()

@router.post("/process-user-query", response_model=QueryResponse)
async def handle_query(
    request: QueryRequest,
    user_chat_service: UserChatService = Depends(get_user_chat_service)):
    answer = await user_chat_service.process_user_query(request.query)
    if isinstance(answer, list):
        blocks = [ContentBlock(type=block["type"], text=block["text"]) for block in answer]
    else:
        blocks = [ContentBlock(type="text", text=str(answer))]
    return QueryResponse(answer=blocks)