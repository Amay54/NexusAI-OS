"""
Abstract Provider Interfaces for NexusAI OS Provider-Agnostic Memory Engine.
Allows swapping Redis, PostgreSQL, Qdrant, or custom backends without modifying agent logic.
"""
from abc import ABC, abstractmethod
from typing import Any, Dict, List, Optional
from pydantic import BaseModel, Field


class MemoryItem(BaseModel):
    id: str
    content: str
    metadata: Dict[str, Any] = Field(default_factory=dict)
    score: float = 1.0


class BaseShortTermMemoryProvider(ABC):
    """Abstract interface for short-term key-value caching with TTL support."""

    @abstractmethod
    async def get(self, key: str) -> Optional[Any]:
        pass

    @abstractmethod
    async def set(self, key: str, value: Any, ttl_seconds: Optional[int] = None) -> None:
        pass

    @abstractmethod
    async def delete(self, key: str) -> bool:
        pass


class BaseWorkingMemoryProvider(ABC):
    """Abstract interface for relational working memory (tasks, runs, executions)."""

    @abstractmethod
    async def save_execution_step(self, workflow_id: int, agent_name: str, step_data: Dict[str, Any]) -> None:
        pass

    @abstractmethod
    async def get_execution_history(self, workflow_id: int) -> List[Dict[str, Any]]:
        pass


class BaseLongTermMemoryProvider(ABC):
    """Abstract interface for vector/semantic long-term memory."""

    @abstractmethod
    async def store(self, item_id: str, content: str, metadata: Optional[Dict[str, Any]] = None) -> None:
        pass

    @abstractmethod
    async def search(self, query: str, top_k: int = 3) -> List[MemoryItem]:
        pass
