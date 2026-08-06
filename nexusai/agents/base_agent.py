"""
Base Agent Persona Structure for NexusAI OS.
Agents communicate EXCLUSIVELY via Event Bus, Memory Engine, Knowledge Graph, and Tool Registry.
Zero direct inter-agent calls.
"""
from abc import ABC, abstractmethod
import logging
from typing import Any, Dict, List, Optional
from pydantic import BaseModel, Field

from nexusai.core.event_bus import AgentEvent, event_bus
from nexusai.core.intelligent_router import intelligent_router
from nexusai.memory.retrieval import context_retrieval_engine
from nexusai.services.knowledge_graph import knowledge_graph

logger = logging.getLogger("nexusai.agents")


class BaseAgentPersona(BaseModel):
    """Abstract Base Agent Persona."""
    name: str = Field(..., description="Agent name/role")
    role: str = Field(..., description="Engineering role title")
    capabilities: List[str] = Field(default_factory=list)
    system_prompt: str = Field(...)

    async def execute_task(
        self,
        task_prompt: str,
        correlation_id: str,
        workflow_id: Optional[int] = None,
        project_id: Optional[str] = None
    ) -> Dict[str, Any]:
        """Executes task with dynamic context retrieval, memory packing, LLM routing, and event publishing."""
        logger.info(f"Agent [{self.name}] starting task execution (CorrID: {correlation_id})...")

        # 1. Retrieve & Compress Context
        ctx = await context_retrieval_engine.build_compressed_context(
            agent_name=self.name,
            task_prompt=task_prompt,
            workflow_id=workflow_id,
            project_id=project_id
        )

        # 2. Format System Context Prompt
        enhanced_prompt = (
            f"Role: {self.role}\n"
            f"Agent Name: {self.name}\n"
            f"Task: {task_prompt}\n"
            f"Context: {ctx.get('compressed_lessons', [])}\n"
            f"Graph Relationships: {ctx.get('graph_relationships', [])}\n"
        )

        # 3. Generate response using Task-based Intelligent Router
        res = await intelligent_router.route_and_generate(
            prompt=enhanced_prompt,
            system_prompt=self.system_prompt
        )

        # 4. Emit Completion Event on Event Bus
        event = AgentEvent(
            event_type=f"{self.role.upper().replace(' ', '_')}_COMPLETED",
            correlation_id=correlation_id,
            sender_agent=self.name,
            payload={
                "task_prompt": task_prompt,
                "output": res["output"],
                "provider_used": res["provider_used"],
                "latency_ms": res["latency_ms"]
            }
        )
        await event_bus.publish(event)

        return {
            "agent_name": self.name,
            "role": self.role,
            "task_prompt": task_prompt,
            "output": res["output"],
            "provider_used": res["provider_used"],
            "latency_ms": res["latency_ms"]
        }
