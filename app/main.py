from fastapi import FastAPI
from app.api.v1.endpoints.query import router as query_router

app = FastAPI(title="Sports Database RAG")

app.include_router(query_router, prefix="/api/v1")

@app.get("/health")
async def health():
    return {"status": "ok"}