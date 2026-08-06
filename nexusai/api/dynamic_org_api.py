"""
Adaptive AI Organization REST API Routers for NexusAI OS (v0.3.1).
Provides endpoints for Dynamic Org Planning, Resource Manager Metrics, Skill Profiles, Specialist Spawning, Debates, and Replanning.
"""
from typing import Any, Dict, List, Optional
from fastapi import APIRouter, HTTPException, Query, Body

from nexusai.workflows.dynamic_org import dynamic_org_planner
from nexusai.agents.spawner import agent_spawner
from nexusai.agents.resource_manager import resource_manager
from nexusai.agents.skill_profiles import agent_skill_registry
from nexusai.services.negotiation import negotiation_engine, DebateStatement
from nexusai.workflows.replanning import autonomous_replanner
from nexusai.services.company_learning import company_learning_service

org_router = APIRouter(prefix="/org", tags=["Adaptive AI Organization"])


@org_router.post("/plan")
async def generate_dynamic_org_plan(goal_prompt: str = Body(...), project_name: str = Body("DynamicProject")):
    """Generates an adaptive organization plan (skipping unnecessary roles, identifying parallel branches)."""
    plan = await dynamic_org_planner.create_dynamic_org_plan(goal_prompt, project_name)
    return plan.model_dump()


@org_router.get("/resources")
async def get_resource_manager_metrics():
    """Returns live CPU/Memory usage, active task queues, and agent Busy/Idle states."""
    return resource_manager.get_resource_metrics()


@org_router.get("/skills")
async def get_agent_skill_profiles():
    """Lists agent domain experience, success rates, average execution times, and confidence scores."""
    profiles = agent_skill_registry.list_skill_profiles()
    return {"count": len(profiles), "profiles": profiles}


@org_router.post("/spawn")
async def spawn_specialist_agent(specialist_name: str = Body(...), domain: str = Body(...)):
    """Dynamically spawns an ephemeral specialist agent."""
    agent = await agent_spawner.spawn_specialist(specialist_name, domain)
    return {"status": "SPAWNED", "specialist": agent.name, "role": agent.role}


@org_router.get("/specialists")
async def list_active_specialists():
    """Lists active ephemeral specialist agents."""
    active = agent_spawner.list_active_specialists()
    return {"active_count": len(active), "specialists": active}


@org_router.post("/debate")
async def execute_agent_debate(topic: str = Body(...), statements: List[DebateStatement] = Body(...), workflow_id: int = Body(1)):
    """Executes structured multi-agent debate and voting resolution."""
    res = await negotiation_engine.execute_agent_debate(topic, statements, workflow_id)
    return res.model_dump()


@org_router.post("/replan")
async def handle_agent_failure_replan(workflow_id: int = Body(...), failed_agent: str = Body(...), failure_reason: str = Body(...), goal_prompt: str = Body(...)):
    """Executes autonomous failure recovery, specialist spawning, and LLM failover."""
    decision = await autonomous_replanner.handle_agent_failure_and_replan(workflow_id, failed_agent, failure_reason, goal_prompt)
    return decision.model_dump()
