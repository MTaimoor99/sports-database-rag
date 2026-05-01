from pydantic import BaseModel

class QueryRequest(BaseModel):
    query: str

class ContentBlock(BaseModel):
    type: str
    text: str

class QueryResponse(BaseModel):
    answer: list[ContentBlock]