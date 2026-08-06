"""
Adaptive AI Organization Test Suite (NexusAI OS v0.3.1).
Verifies Dynamic Org Planning, Ephemeral Specialist Spawning, Resource Manager, Skill Profiles, Debates, Replanning, and REST APIs.
"""
import pytest
from httpx import ASGITransport, AsyncClient

from nexusai.workflows.dynamic_org import dynamic_org_planner
from nexusai.agents.spawner import agent_spawner
from nexusai.agents.resource_manager import resource_manager
from nexusai.agents.skill_profiles import agent_skill_registry
from nexusai.services.negotiation import negotiation_engine, DebateStatement
from nexusai.workflows.replanning import autonomous_replanner
from nexusai.main import app


@pytest.mark.asyncio
async def test_dynamic_org_planning_simple_vs_enterprise():
    """Test dynamic organization planning for simple vs enterprise projects."""
    # 1. Simple todo API
    simple_plan = await dynamic_org_planner.create_dynamic_org_plan("Build a simple TODO CLI app")
    assert simple_plan.complexity_level == "SIMPLE"
    assert "backend" in simple_plan.selected_agents
    assert "frontend" in simple_plan.skipped_agents

    # 2. Enterprise SaaS
    ent_plan = await dynamic_org_planner.create_dynamic_org_plan("Build an enterprise SaaS microservices platform")
    assert ent_plan.complexity_level == "ENTERPRISE"
    assert "frontend" in ent_plan.selected_agents
    assert len(ent_plan.specialists_to_spawn) > 0


@pytest.mark.asyncio
async def test_ephemeral_specialist_agent_spawning():
    """Test spawning and terminating temporary specialist agents."""
    specialist = await agent_spawner.spawn_specialist("OAuth Specialist", "authentication")

    assert specialist.name == "OAuth Specialist"
    active = agent_spawner.list_active_specialists()
    assert len(active) > 0


@pytest.mark.asyncio
async def test_resource_manager_and_skill_profiles():
    """Test Resource Manager metrics and Skill Profile tracking."""
    # Resource metrics
    res_metrics = resource_manager.get_resource_metrics()
    assert "system_cpu_usage_percent" in res_metrics

    # Skill profile updates
    agent_skill_registry.record_task_outcome("Backend Engineer Agent", success=True, execution_time_ms=250.0)
    prof = agent_skill_registry.get_profile("Backend Engineer Agent")

    assert prof.total_tasks_executed > 0
    assert prof.success_rate == 1.0


@pytest.mark.asyncio
async def test_agent_debate_and_autonomous_replanning():
    """Test multi-agent debates and failure recovery replanning."""
    # Debate
    statements = [
        DebateStatement(agent_name="Architect Agent", argument="Use PostgreSQL", confidence=0.9),
        DebateStatement(agent_name="Backend Agent", argument="Use PostgreSQL", confidence=0.85)
    ]
    debate_res = await negotiation_engine.execute_agent_debate("Select Database Engine", statements)
    assert debate_res.resolved is True
    assert debate_res.final_consensus == "APPROVED"

    # Replanning
    replan_res = await autonomous_replanner.handle_agent_failure_and_replan(
        workflow_id=901,
        failed_agent="DevOps Agent",
        failure_reason="Docker daemon socket timeout",
        goal_prompt="Deploy microservice"
    )
    assert replan_res.action_taken == "SPAWN_SPECIALIST"
    assert replan_res.new_agent_name is not None


@pytest.mark.asyncio
async def test_dynamic_org_rest_apis():
    """Test FastAPI endpoints for dynamic org planning, resources, skills, and spawning."""
    async with AsyncClient(transport=ASGITransport(app=app), base_url="http://test") as client:
        # 1. Plan API
        plan_res = await client.post("/api/v1/org/plan", json={"goal_prompt": "Build simple API", "project_name": "TestAPI"})
        assert plan_res.status_code == 200
        assert "selected_agents" in plan_res.json()

        # 2. Resources API
        rec_res = await client.get("/api/v1/org/resources")
        assert rec_res.status_code == 200
        assert "system_cpu_usage_percent" in rec_res.json()

        # 3. Skills API
        skills_res = await client.get("/api/v1/org/skills")
        assert skills_res.status_code == 200
        assert "profiles" in skills_res.json()

        # 4. Spawn API
        spawn_res = await client.post("/api/v1/org/spawn", json={"specialist_name": "Docker Expert", "domain": "containers"})
        assert spawn_res.status_code == 200
        assert spawn_res.json()["status"] == "SPAWNED"
