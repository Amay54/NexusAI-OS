"""
Dynamic Organization Engine for NexusAI OS.
Decomposes user prompts into dynamic, adaptive workforce plans (skipping unnecessary roles, selecting parallel branches, and spawning specialists).
"""
import re
from typing import Any, Dict, List, Optional
from pydantic import BaseModel, Field


class DynamicOrgPlan(BaseModel):
    project_name: str
    goal_prompt: str
    complexity_level: str  # SIMPLE, MEDIUM, ENTERPRISE
    selected_agents: List[str]
    skipped_agents: List[str]
    parallel_execution_branches: List[List[str]]
    specialists_to_spawn: List[str]
    estimated_duration_seconds: float


class DynamicOrgPlanner:
    """CEO Dynamic Organization Planner."""

    async def create_dynamic_org_plan(self, goal_prompt: str, project_name: str = "DynamicProject") -> DynamicOrgPlan:
        """Analyzes goal prompt and produces adaptive organization plan."""
        p_lower = goal_prompt.lower()

        # Complexity & Role selection heuristic
        is_simple = any(k in p_lower for k in ["simple", "todo", "cli", "script", "minimal", "basic"])
        is_enterprise = any(k in p_lower for k in ["enterprise", "saas", "production", "ecommerce", "microservice", "distributed"])

        if is_simple:
            complexity = "SIMPLE"
            selected = ["ceo", "pm", "backend", "qa", "reviewer"]
            skipped = ["frontend", "architect", "database", "security", "devops", "documentation", "marketing", "reflection"]
            parallel = [["backend"]]
            specialists = []
            est_duration = 15.0
        elif is_enterprise:
            complexity = "ENTERPRISE"
            selected = [
                "ceo", "pm", "architect", "backend", "frontend", "database",
                "security", "qa", "devops", "documentation", "marketing", "reflection", "reviewer"
            ]
            skipped = []
            parallel = [["database", "backend", "frontend"], ["qa", "security"]]
            specialists = ["OAuth Specialist", "Docker Specialist", "PostgreSQL Specialist"]
            est_duration = 60.0
        else:
            complexity = "MEDIUM"
            selected = ["ceo", "pm", "architect", "backend", "frontend", "database", "qa", "devops", "documentation", "reviewer"]
            skipped = ["security", "marketing", "reflection"]
            parallel = [["backend", "frontend"], ["qa"]]
            specialists = ["Docker Specialist"]
            est_duration = 35.0

        return DynamicOrgPlan(
            project_name=project_name,
            goal_prompt=goal_prompt,
            complexity_level=complexity,
            selected_agents=selected,
            skipped_agents=skipped,
            parallel_execution_branches=parallel,
            specialists_to_spawn=specialists,
            estimated_duration_seconds=est_duration
        )


dynamic_org_planner = DynamicOrgPlanner()
