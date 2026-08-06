"""
NexusAI OS FastAPI Production Control Plane Entrypoint (v0.5.1).
Registers Auth, Workflows, MCP Tools, Memory, Explainability, Knowledge Graph, Reflection, History, Snapshots, Observability,
Workforce, Dynamic Org, Executive Intelligence, WebSockets Telemetry, Built-In Demo Workflows, Project Download, and Hosts the Production React OS Dashboard.
"""
from contextlib import asynccontextmanager
from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from fastapi.staticfiles import StaticFiles
from fastapi.responses import FileResponse
import os

from nexusai.core.config import settings
from nexusai.api.intelligence import (
    memory_router, graph_router, reflection_router, history_router,
    observability_router, snapshot_router
)
from nexusai.api.mcp_api import mcp_router
from nexusai.api.workforce_api import workforce_router
from nexusai.api.dynamic_org_api import org_router
from nexusai.api.executive_api import executive_router
from nexusai.api.executive_explainability_api import explainability_router
from nexusai.api.websocket_api import ws_router
from nexusai.api.demo_api import demo_router
from nexusai.api.project_download_api import download_router
from nexusai.mcp.engine import discovery_engine


@asynccontextmanager
async def lifespan(app: FastAPI):
    """Lifecycle startup initialization: auto-discover MCP tools."""
    await discovery_engine.discover_and_index_all_tools()
    yield


app = FastAPI(
    title=settings.APP_NAME,
    description="NexusAI OS Enterprise Autonomous AI Operating System Control Plane",
    version="0.5.1",
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
app.include_router(org_router, prefix="/api/v1")
app.include_router(executive_router, prefix="/api/v1")
app.include_router(explainability_router, prefix="/api/v1")
app.include_router(demo_router, prefix="/api/v1")
app.include_router(download_router, prefix="/api/v1")
app.include_router(ws_router)


@app.get("/health")
async def health_check():
    return {
        "status": "healthy",
        "app_name": settings.APP_NAME,
        "version": "0.5.1",
        "default_llm_provider": settings.DEFAULT_LLM_PROVIDER,
        "hitl_enabled": settings.ENABLE_HITL_APPROVAL
    }

# Mount React 18 OS Dashboard Static Assets
frontend_dist = os.path.join(os.path.dirname(__file__), "..", "frontend", "dist")
if os.path.exists(frontend_dist):
    app.mount("/assets", StaticFiles(directory=os.path.join(frontend_dist, "assets")), name="static_assets")

    @app.get("/")
    async def serve_dashboard():
        return FileResponse(os.path.join(frontend_dist, "index.html"))
