"""
Phase 2 Intelligence REST API Routers for NexusAI OS (v0.2.1).
Provides endpoints for Memory retrieval, Explainability, Graph queries, Reflections, History, Snapshots, and Observability Metrics.
"""
from typing import Any, Dict, List, Optional
from fastapi import APIRouter, HTTPException, Query

from nexusai.memory.manager import memory_manager
from nexusai.memory.explainability import memory_explainability
from nexusai.services.knowledge_graph import knowledge_graph
from nexusai.services.reflection import reflection_service
from nexusai.services.state_persistence import state_persistence_manager
from nexusai.services.snapshots import snapshot_manager
from nexusai.core.observability import metrics_tracker

memory_router = APIRouter(prefix="/memory", tags=["Memory Engine"])
graph_router = APIRouter(prefix="/graph", tags=["Knowledge Graph Engine"])
reflection_router = APIRouter(prefix="/reflection", tags=["Reflection Engine"])
history_router = APIRouter(prefix="/workflows", tags=["Workflow Execution History"])
observability_router = APIRouter(prefix="/observability", tags=["Observability Metrics"])
snapshot_router = APIRouter(prefix="/snapshots", tags=["Workflow Snapshots"])


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


@memory_router.get("/explain")
async def get_memory_retrieval_explainability(limit: int = 10):
    """Returns retrieval rationale for why specific memories were selected."""
    return {"explanations": memory_explainability.get_latest_explanations(limit=limit)}


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


# --- Observability APIs ---
@observability_router.get("/metrics")
async def get_observability_metrics():
    """Returns operational metrics (retrieval latency, cache hit ratio, vector search latency)."""
    return metrics_tracker.get_metrics_summary()


# --- Snapshot APIs ---
@snapshot_router.get("/{workflow_id}")
async def get_workflow_snapshots(workflow_id: int):
    """Gets historical state snapshots for a workflow."""
    snaps = await snapshot_manager.get_snapshots_for_workflow(workflow_id)
    return {"workflow_id": workflow_id, "snapshot_count": len(snaps), "snapshots": [s.model_dump() for s in snaps]}


@snapshot_router.post("/{workflow_id}/rollback")
async def rollback_workflow_to_snapshot(workflow_id: int, snapshot_id: str):
    """Rolls back workflow state to a specific snapshot ID."""
    try:
        restored_cp = await snapshot_manager.rollback_to_snapshot(workflow_id, snapshot_id)
        return {"status": "SUCCESS", "message": f"Rolled back Workflow #{workflow_id} to Snapshot #{snapshot_id}", "checkpoint": restored_cp.model_dump()}
    except ValueError as exc:
        raise HTTPException(status_code=400, detail=str(exc))
