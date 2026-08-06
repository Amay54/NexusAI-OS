"""
Provider-Agnostic Memory Manager for NexusAI OS.
Supports memory versioning, importance scoring, and backward-compatible experience storage.
"""
from typing import Any, Dict, List, Optional
import uuid
from nexusai.memory.base import (
    BaseShortTermMemoryProvider, BaseLongTermMemoryProvider, MemoryItem, ImportanceLevel
)
from nexusai.memory.providers.redis_provider import RedisShortTermMemory
from nexusai.memory.providers.qdrant_provider import QdrantLongTermMemory


class MemoryManager:
    """Unified provider-agnostic memory service."""

    def __init__(
        self,
        short_term_provider: Optional[BaseShortTermMemoryProvider] = None,
        long_term_provider: Optional[BaseLongTermMemoryProvider] = None,
    ):
        self.short_term = short_term_provider or RedisShortTermMemory()
        self.long_term = long_term_provider or QdrantLongTermMemory()

    async def store_experience(
        self,
        exp_id: str,
        lesson: str,
        metadata: Optional[Dict[str, Any]] = None,
        importance_level: ImportanceLevel = ImportanceLevel.MEDIUM,
        source_agent: str = "SYSTEM"
    ) -> MemoryItem:
        """Stores experience in long-term memory asynchronously (supports versioning)."""
        item = MemoryItem(
            memory_id=exp_id,
            content=lesson,
            source_agent=source_agent,
            importance_level=importance_level,
            tags=metadata.get("tags", []) if metadata else []
        )
        await self.long_term.store(item)
        return item

    async def retrieve_context_for_agent(self, agent_name: str, task_prompt: str) -> Dict[str, Any]:
        """Concurrent memory retrieval for agents before making decisions."""
        relevant_memories = await self.long_term.search(task_prompt, top_k=3)
        recent_state = await self.short_term.get(f"state_{agent_name}")

        return {
            "short_term_state": recent_state,
            "relevant_experiences": [m.model_dump() for m in relevant_memories]
        }


memory_manager = MemoryManager()
