"""
Built-In Demo Workflows REST API Router for NexusAI OS (v0.4.0).
Provides endpoints to list demonstration workflows and execute them end-to-end.
"""
from typing import Any, Dict, List
from fastapi import APIRouter, HTTPException, Path

from nexusai.services.demo_workflows import demo_workflows_registry

demo_router = APIRouter(prefix="/demo", tags=["Built-In Demonstration Workflows"])


@demo_router.get("/workflows")
async def list_demo_workflows():
    """Lists built-in production demonstration workflows."""
    demos = demo_workflows_registry.list_demo_workflows()
    return {"count": len(demos), "demo_workflows": [d.model_dump() for d in demos]}


@demo_router.post("/execute/{demo_id}")
async def execute_demo_workflow(demo_id: str = Path(...)):
    """Executes selected demonstration workflow end-to-end and returns production project artifacts."""
    artifact = await demo_workflows_registry.execute_demo_workflow(demo_id)
    return artifact.model_dump()
