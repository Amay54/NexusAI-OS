"""
NexusAI OS FastAPI Control Plane Entrypoint.
Registers Auth, Workflows, MCP tools, Approvals, Memory, Knowledge Graph, Reflection, and History REST endpoints.
"""
from contextlib import asynccontextmanager
from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware

from nexusai.core.config import settings
from nexusai.api.intelligence import (
    memory_router, graph_router, reflection_router, history_router
)


@asynccontextmanager
async def lifespan(app: FastAPI):
    """Lifecycle startup and shutdown initialization."""
    yield


app = FastAPI(
    title=settings.APP_NAME,
    description="NexusAI OS Enterprise Control Plane & Intelligence API",
    version="0.2.0",
    lifespan=lifespan
)

# Enable CORS
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Register Routers
app.include_router(memory_router, prefix="/api/v1")
app.include_router(graph_router, prefix="/api/v1")
app.include_router(reflection_router, prefix="/api/v1")
app.include_router(history_router, prefix="/api/v1")


@app.get("/health")
async def health_check():
    return {
        "status": "healthy",
        "app_name": settings.APP_NAME,
        "version": "0.2.0",
        "default_llm_provider": settings.DEFAULT_LLM_PROVIDER,
        "hitl_enabled": settings.ENABLE_HITL_APPROVAL
    }
