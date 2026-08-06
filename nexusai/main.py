"""
NexusAI OS FastAPI Control Plane Entrypoint (v0.3.0).
Registers Auth, Workflows, MCP Tools, Memory, Explainability, Knowledge Graph, Reflection, History, Snapshots, Observability, and Autonomous Workforce.
"""
from contextlib import asynccontextmanager
from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware

from nexusai.core.config import settings
from nexusai.api.intelligence import (
    memory_router, graph_router, reflection_router, history_router,
    observability_router, snapshot_router
)
from nexusai.api.mcp_api import mcp_router
from nexusai.api.workforce_api import workforce_router
from nexusai.mcp.engine import discovery_engine


@asynccontextmanager
async def lifespan(app: FastAPI):
    """Lifecycle startup initialization: auto-discover MCP tools."""
    await discovery_engine.discover_and_index_all_tools()
    yield


app = FastAPI(
    title=settings.APP_NAME,
    description="NexusAI OS Enterprise Control Plane & Autonomous Workforce API",
    version="0.3.0",
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
app.include_router(observability_router, prefix="/api/v1")
app.include_router(snapshot_router, prefix="/api/v1")
app.include_router(mcp_router, prefix="/api/v1")
app.include_router(workforce_router, prefix="/api/v1")


@app.get("/health")
async def health_check():
    return {
        "status": "healthy",
        "app_name": settings.APP_NAME,
        "version": "0.3.0",
        "default_llm_provider": settings.DEFAULT_LLM_PROVIDER,
        "hitl_enabled": settings.ENABLE_HITL_APPROVAL
    }
