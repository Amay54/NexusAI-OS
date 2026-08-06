"""
Phase 2 Intelligence REST API Routers for NexusAI OS.
Provides endpoints for Memory retrieval, Knowledge Graph query, Reflections, and Workflow Execution History.
"""
from typing import Any, Dict, List, Optional
from fastapi import APIRouter, HTTPException, Query

from nexusai.memory.manager import memory_manager
from nexusai.services.knowledge_graph import knowledge_graph
from nexusai.services.reflection import reflection_service
from nexusai.services.state_persistence import state_persistence_manager

memory_router = APIRouter(prefix="/memory", tags=["Memory Engine"])
graph_router = APIRouter(prefix="/graph", tags=["Knowledge Graph Engine"])
reflection_router = APIRouter(prefix="/reflection", tags=["Reflection Engine"])
history_router = APIRouter(prefix="/workflows", tags=["Workflow Execution History"])


# --- Memory APIs ---
@memory_router.get("")
async def get_agent_memory_context(agent_name: str, task_prompt: str):
    """Retrieves short-term state and relevant long-term memories for an agent."""
    return await memory_manager.retrieve_context_for_agent(agent_name, task_prompt)


@memory_router.get("/search")
async def search_long_term_memory(q: str = Query(..., description="Semantic search query"), top_k: int = 5):
    """Performs semantic vector search over long-term experience memory."""
    results = await memory_manager.long_term.search(q, top_k=top_k)
    return {"query": q, "results_count": len(results), "memories": [r.model_dump() for r in results]}


# --- Knowledge Graph APIs ---
@graph_router.get("")
async def get_graph_topology():
    """Returns the full knowledge graph node & edge topology."""
    return await knowledge_graph.get_full_graph_topology()


@graph_router.get("/node/{node_id}")
async def get_graph_relationships(node_id: str, relation: Optional[str] = None):
    """Queries connected graph relationships for a specific node ID."""
    rels = await knowledge_graph.query_relationships(node_id, relation=relation)
    return {"subject_id": node_id, "relation_filter": relation, "relationships": rels}


# --- Reflection APIs ---
@reflection_router.get("")
async def get_reflection_report(workflow_id: int):
    """Gets retrospective reflection report for a workflow ID."""
    report = await reflection_service.get_reflection(workflow_id)
    if not report:
        raise HTTPException(status_code=404, detail=f"No reflection report found for Workflow #{workflow_id}")
    return report.model_dump()


@reflection_router.get("/search")
async def search_workflow_reflections(q: str = Query(...), top_k: int = 5):
    """Semantically searches indexed workflow lessons learned."""
    results = await reflection_service.search_reflections(q, top_k=top_k)
    return {"query": q, "results": results}


# --- History & Checkpoint APIs ---
@history_router.get("/{workflow_id}/history")
async def get_workflow_execution_history(workflow_id: int):
    """Retrieves detailed execution history (LLM latency, tool calls, trace IDs)."""
    rec = await state_persistence_manager.get_workflow_history(workflow_id)
    if not rec:
        raise HTTPException(status_code=404, detail=f"No execution history record found for Workflow #{workflow_id}")
    return rec.model_dump()


@history_router.get("/{workflow_id}/checkpoint")
async def get_workflow_checkpoint(workflow_id: int):
    """Gets agent state checkpoint for restoring an interrupted workflow."""
    cp = await state_persistence_manager.get_checkpoint(workflow_id)
    if not cp:
        raise HTTPException(status_code=404, detail=f"No active state checkpoint found for Workflow #{workflow_id}")
    return cp.model_dump()
