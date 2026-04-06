from fastapi import FastAPI
from app.api.v1.endpoints.query import router as query_router
from fastapi.middleware.cors import CORSMiddleware
import platform
import asyncio

if platform.system()=='Windows':
    asyncio.set_event_loop_policy(asyncio.WindowsSelectorEventLoopPolicy())

app = FastAPI(title="Sports Database RAG")

app.add_middleware(
    CORSMiddleware,
    allow_origins=["http://localhost:3000"],
    allow_methods=["*"],
    allow_headers=["*"],
)

app.include_router(query_router, prefix="/api/v1")

@app.get("/health")
async def health():
    return {"status": "ok"}