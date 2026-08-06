"""
Autonomous Multi-Agent Workforce Test Suite (NexusAI OS v0.3.0).
Verifies 13 Agent Personas, LangGraph Orchestrator, Consensus Voting, HITL Safety Checkpoints, End-to-End Synthesis, and REST APIs.
"""
import pytest
from httpx import ASGITransport, AsyncClient

from nexusai.agents.personas import workforce_personas
from nexusai.workflows.graph_orchestrator import graph_orchestrator
from nexusai.services.consensus import consensus_engine, AgentVote, VotingStrategy
from nexusai.services.hitl import hitl_service
from nexusai.services.project_synthesizer import project_synthesizer
from nexusai.main import app


def test_workforce_13_agent_personas_count():
    """Verify all 13 specialized agent personas are defined."""
    assert len(workforce_personas) == 13
    assert "ceo" in workforce_personas
    assert "pm" in workforce_personas
    assert "architect" in workforce_personas
    assert "backend" in workforce_personas
    assert "frontend" in workforce_personas
    assert "qa" in workforce_personas
    assert "security" in workforce_personas
    assert "database" in workforce_personas
    assert "devops" in workforce_personas
    assert "documentation" in workforce_personas
    assert "marketing" in workforce_personas
    assert "reflection" in workforce_personas
    assert "reviewer" in workforce_personas


@pytest.mark.asyncio
async def test_langgraph_autonomous_workflow_execution():
    """Test full event-driven workflow execution across the workforce."""
    state = await graph_orchestrator.execute_autonomous_workflow(
        workflow_id=601,
        goal_prompt="Build microservice authentication system"
    )

    assert state.workflow_id == 601
    assert state.status == "COMPLETED"
    assert "ceo" in state.step_results
    assert "backend" in state.step_results
    assert "frontend" in state.step_results
    assert "devops" in state.step_results


@pytest.mark.asyncio
async def test_multi_agent_consensus_voting():
    """Test confidence-weighted voting across agents."""
    votes = [
        AgentVote(agent_name="Architect Agent", decision="APPROVE", confidence=0.95, reasoning="Clean architecture"),
        AgentVote(agent_name="Security Agent", decision="APPROVE", confidence=0.90, reasoning="No OWASP vulnerabilities"),
        AgentVote(agent_name="QA Agent", decision="REJECT", confidence=0.40, reasoning="Needs more edge case tests")
    ]

    res = await consensus_engine.evaluate_consensus(
        topic="Approve Microservice Deployment",
        votes=votes,
        strategy=VotingStrategy.CONFIDENCE_WEIGHTED
    )

    assert res.approved is True
    assert res.conflict_resolved is True
    assert res.weighted_score >= 0.6


@pytest.mark.asyncio
async def test_hitl_approval_checkpoint_lifecycle():
    """Test creating, approving, and querying HITL safety checkpoints."""
    req = await hitl_service.request_approval(
        workflow_id=602,
        agent_name="DevOps Engineer Agent",
        action_type="DEPLOYMENT",
        description="Production Kubernetes deployment",
        danger_level="HIGH"
    )

    assert req.status == "PENDING"

    pending = await hitl_service.get_pending_approvals(602)
    assert len(pending) == 1

    approved = await hitl_service.approve_action(req.approval_id, approver="Lead Architect")
    assert approved.status == "APPROVED"
    assert approved.approver == "Lead Architect"


@pytest.mark.asyncio
async def test_end_to_end_project_synthesis():
    """Test full software project generation (FastAPI inventory management system)."""
    artifact = await project_synthesizer.synthesize_full_project(
        project_name="InventorySystem",
        goal_prompt="Build a FastAPI inventory management system.",
        workflow_id=701
    )

    assert artifact.project_name == "InventorySystem"
    assert "main.py" in artifact.files
    assert "test_main.py" in artifact.files
    assert "FROM python" in artifact.dockerfile
    assert artifact.sandbox_verification["success"] is True


@pytest.mark.asyncio
async def test_workforce_rest_apis():
    """Test FastAPI REST endpoints for Org Chart, Agents, Execution, and Synthesis."""
    async with AsyncClient(transport=ASGITransport(app=app), base_url="http://test") as client:
        # 1. Org Chart
        org_res = await client.get("/api/v1/workforce/orgchart")
        assert org_res.status_code == 200
        assert org_res.json()["total_agents"] == 13

        # 2. List Agents
        agents_res = await client.get("/api/v1/workforce/agents")
        assert agents_res.status_code == 200
        assert agents_res.json()["count"] == 13

        # 3. Synthesize API
        syn_res = await client.post("/api/v1/workforce/synthesize", json={
            "project_name": "InventoryApp",
            "goal_prompt": "Build a FastAPI inventory management system.",
            "workflow_id": 801
        })
        assert syn_res.status_code == 200
        assert syn_res.json()["project_name"] == "InventoryApp"
