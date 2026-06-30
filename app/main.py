from contextlib import asynccontextmanager

from fastapi import FastAPI

from app.routes.ingestion import router as ingestion_router
from app.routes.auth import router as auth_router
from app.db.session import init_db
from app.tasks.broker import broker

@asynccontextmanager
async def lifespan(app: FastAPI):
    # Startup
    print("🚀 Starting RAG API...")
    await broker.startup()
    # Example:
    # await redis_client.ping()
    # await vector_service.create_collection_if_not_exists()
    
    await init_db()
    yield

    await broker.shutdown()
    # Shutdown
    print("🛑 Shutting down RAG API...")

    # Example:
    # await redis_client.close()

app=FastAPI(
    title="Agentic RAG API",
    version="1.0.0",
    description="FastAPI backend for document ingestion and retrieval.",
    lifespan=lifespan,
)

app.include_router(
    ingestion_router,
    prefix="/api",
    tags=["ingestion"]
)
 
app.include_router(
    auth_router,
    prefix="/api",
    tags=["auth"]   
)