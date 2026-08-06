"""
Ephemeral Specialist Agent Spawner Engine for NexusAI OS.
Dynamically creates temporary specialist agent personas and auto-terminates them upon task completion.
"""
from datetime import datetime, timezone
import logging
import uuid
from typing import Any, Dict, List, Optional
from pydantic import BaseModel, Field

from nexusai.agents.base_agent import BaseAgentPersona

logger = logging.getLogger("nexusai.spawner")


class EphemeralAgentRecord(BaseModel):
    agent_id: str = Field(default_factory=lambda: str(uuid.uuid4()))
    specialist_name: str
    domain: str
    spawned_at: str = Field(default_factory=lambda: datetime.now(timezone.utc).isoformat())
    status: str = "ACTIVE"  # ACTIVE, TERMINATED
    tasks_completed: int = 0


class AgentSpawner:
    """Dynamic Ephemeral Specialist Agent Spawner & Lifecycle Manager."""

    def __init__(self):
        self.active_ephemeral_agents: Dict[str, EphemeralAgentRecord] = {}

    async def spawn_specialist(self, specialist_name: str, domain: str) -> BaseAgentPersona:
        """Spawns an ephemeral specialist agent persona."""
        record = EphemeralAgentRecord(specialist_name=specialist_name, domain=domain)
        self.active_ephemeral_agents[record.agent_id] = record

        logger.info(f"Spawned Ephemeral Specialist [{specialist_name}] (ID: {record.agent_id}, Domain: {domain})")

        return BaseAgentPersona(
            name=specialist_name,
            role=f"{domain.capitalize()} Specialist",
            capabilities=[f"{domain}_expert", "ephemeral_task_execution"],
            system_prompt=f"You are the {specialist_name}, an expert in {domain}. Deliver precise specialist engineering outputs."
        )

    async def terminate_specialist(self, agent_id: str) -> None:
        """Terminates an ephemeral specialist agent upon task completion."""
        rec = self.active_ephemeral_agents.get(agent_id)
        if rec:
            rec.status = "TERMINATED"
            logger.info(f"Terminated Ephemeral Specialist [{rec.specialist_name}] (ID: {agent_id})")

    def list_active_specialists(self) -> List[Dict[str, Any]]:
        return [r.model_dump() for r in self.active_ephemeral_agents.values() if r.status == "ACTIVE"]


agent_spawner = AgentSpawner()
