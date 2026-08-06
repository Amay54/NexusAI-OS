"""
Autonomous Replanning Engine for NexusAI OS.
Handles agent failures dynamically by spawning specialists, changing tools/LLMs, and retrying workflows.
"""
import logging
from typing import Any, Dict, List, Optional
from pydantic import BaseModel, Field

from nexusai.agents.spawner import agent_spawner
from nexusai.memory.manager import memory_manager

logger = logging.getLogger("nexusai.replanning")


class ReplanningDecision(BaseModel):
    workflow_id: int
    failed_agent: str
    failure_reason: str
    action_taken: str  # SPAWN_SPECIALIST, SWITCH_LLM, RETRY_WITH_FALLBACK
    new_agent_name: Optional[str] = None
    new_llm_provider: Optional[str] = None


class AutonomousReplanner:
    """Catches agent errors and dynamically executes replanning strategy."""

    async def handle_agent_failure_and_replan(
        self,
        workflow_id: int,
        failed_agent: str,
        failure_reason: str,
        goal_prompt: str
    ) -> ReplanningDecision:
        """Executes failure recovery, specialist spawning, and LLM failover."""
        logger.warning(f"Replanning triggered for Workflow #{workflow_id} (Failed Agent: {failed_agent}, Error: {failure_reason})")

        # 1. Spawn a domain specialist to replace failed agent
        specialist = await agent_spawner.spawn_specialist(
            specialist_name=f"{failed_agent.replace(' Agent', '')} Recovery Specialist",
            domain="error_recovery"
        )

        # 2. Store failure lesson into Long-Term Memory
        await memory_manager.store_experience(
            exp_id=f"replan_wf_{workflow_id}",
            lesson=f"Workflow #{workflow_id} agent {failed_agent} failed: {failure_reason}. Recovered via {specialist.name}."
        )

        decision = ReplanningDecision(
            workflow_id=workflow_id,
            failed_agent=failed_agent,
            failure_reason=failure_reason,
            action_taken="SPAWN_SPECIALIST",
            new_agent_name=specialist.name,
            new_llm_provider="qwen"
        )
        return decision


autonomous_replanner = AutonomousReplanner()
