"""
NexusAI OS Versioned Memory Models & Abstract Provider Interfaces.
Supports Memory Versioning, Importance Scoring, and Provider Abstractions.
"""
from abc import ABC, abstractmethod
from datetime import datetime, timezone
from enum import Enum
import uuid
from typing import Any, Dict, List, Optional
from pydantic import BaseModel, Field, model_validator


class ImportanceLevel(str, Enum):
    CRITICAL = "CRITICAL"
    HIGH = "HIGH"
    MEDIUM = "MEDIUM"
    LOW = "LOW"


IMPORTANCE_SCORE_MAP = {
    ImportanceLevel.CRITICAL: 1.0,
    ImportanceLevel.HIGH: 0.75,
    ImportanceLevel.MEDIUM: 0.50,
    ImportanceLevel.LOW: 0.25,
}


class MemoryItem(BaseModel):
    """Versioned memory item schema with metadata and importance scoring."""
    id: str = Field(default="")
    memory_id: str = Field(..., description="Unique memory logical identifier")
    version: int = Field(default=1, description="Version sequence number")
    content: str = Field(..., description="Memory body text")
    source_agent: str = Field(default="SYSTEM", description="Agent that produced this memory")
    workflow_id: Optional[int] = Field(default=None)
    confidence_score: float = Field(default=1.0, ge=0.0, le=1.0)
    importance_level: ImportanceLevel = Field(default=ImportanceLevel.MEDIUM)
    importance_score: float = Field(default=0.50)
    embedding_provider: str = Field(default="mock")
    tags: List[str] = Field(default_factory=list)
    created_at: str = Field(default_factory=lambda: datetime.now(timezone.utc).isoformat())
    updated_at: str = Field(default_factory=lambda: datetime.now(timezone.utc).isoformat())
    score: float = Field(default=1.0, description="Runtime retrieval score")

    @model_validator(mode="after")
    def populate_id(self):
        if not self.id:
            self.id = self.memory_id
        return self


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
    """Abstract interface for relational working memory."""

    @abstractmethod
    async def save_execution_step(self, workflow_id: int, agent_name: str, step_data: Dict[str, Any]) -> None:
        pass

    @abstractmethod
    async def get_execution_history(self, workflow_id: int) -> List[Dict[str, Any]]:
        pass


class BaseLongTermMemoryProvider(ABC):
    """Abstract interface for vector/semantic long-term memory."""

    @abstractmethod
    async def store(self, item: MemoryItem) -> None:
        pass

    @abstractmethod
    async def search(self, query: str, top_k: int = 3) -> List[MemoryItem]:
        pass
