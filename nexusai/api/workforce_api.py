"""
Autonomous Workforce REST API Routers for NexusAI OS (v0.3.0).
Provides endpoints for Org Chart, Workforce Execution, Live Workflow State, HITL Approvals, and Full Project Synthesis.
"""
from typing import Any, Dict, List, Optional
from fastapi import APIRouter, HTTPException, Query, Body

from nexusai.agents.personas import workforce_personas
from nexusai.workflows.graph_orchestrator import graph_orchestrator
from nexusai.services.hitl import hitl_service
from nexusai.services.project_synthesizer import project_synthesizer
from nexusai.services.consensus import consensus_engine, AgentVote, VotingStrategy

workforce_router = APIRouter(prefix="/workforce", tags=["Autonomous Multi-Agent Workforce"])


@workforce_router.get("/orgchart")
async def get_organization_chart():
    """Returns the workforce organization chart and hierarchy."""
    chart = []
    for key, p in workforce_personas.items():
        chart.append({
            "key": key,
            "name": p.name,
            "role": p.role,
            "capabilities": p.capabilities
        })
    return {"total_agents": len(chart), "org_chart": chart}


@workforce_router.get("/agents")
async def list_agent_personas():
    """Lists all 13 specialized agent personas."""
    return {"count": len(workforce_personas), "agents": [p.model_dump() for p in workforce_personas.values()]}


@workforce_router.post("/execute")
async def execute_autonomous_workflow(workflow_id: int = Body(...), goal_prompt: str = Body(...)):
    """Triggers autonomous workflow execution across the 13 agents."""
    state = await graph_orchestrator.execute_autonomous_workflow(workflow_id, goal_prompt)
    return state.model_dump()


@workforce_router.get("/workflow/{workflow_id}")
async def get_workflow_live_state(workflow_id: int):
    """Gets current state and step results for a workflow."""
    state = await graph_orchestrator.get_workflow_state(workflow_id)
    if not state:
        raise HTTPException(status_code=404, detail=f"Workflow #{workflow_id} not found")
    return state.model_dump()


@workforce_router.get("/approvals")
async def get_pending_approvals(workflow_id: Optional[int] = None):
    """Lists pending Human-in-the-Loop approval requests."""
    reqs = await hitl_service.get_pending_approvals(workflow_id)
    return {"count": len(reqs), "approvals": [r.model_dump() for r in reqs]}


@workforce_router.post("/workflow/{workflow_id}/approve")
async def approve_hitl_action(workflow_id: int, approval_id: str = Body(...), approver: str = Body("Human Reviewer")):
    """Approves a pending HITL action for a workflow."""
    try:
        req = await hitl_service.approve_action(approval_id, approver)
        return {"status": "APPROVED", "approval": req.model_dump()}
    except ValueError as exc:
        raise HTTPException(status_code=400, detail=str(exc))


@workforce_router.post("/synthesize")
async def synthesize_project(project_name: str = Body(...), goal_prompt: str = Body(...), workflow_id: int = Body(501)):
    """Synthesizes a full software project (e.g. FastAPI inventory management system)."""
    artifact = await project_synthesizer.synthesize_full_project(project_name, goal_prompt, workflow_id)
    return artifact.model_dump()


@workforce_router.post("/consensus")
async def evaluate_multi_agent_vote(topic: str = Body(...), votes: List[AgentVote] = Body(...), strategy: VotingStrategy = Body(VotingStrategy.CONFIDENCE_WEIGHTED)):
    """Evaluates multi-agent consensus voting."""
    res = await consensus_engine.evaluate_consensus(topic, votes, strategy)
    return res.model_dump()
