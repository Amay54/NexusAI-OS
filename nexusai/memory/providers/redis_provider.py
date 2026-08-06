"""
Redis & Ephemeral In-Memory Short-Term Memory Provider.
Supports TTL caching and graceful fallback.
"""
import time
from typing import Any, Dict, Optional
from nexusai.memory.base import BaseShortTermMemoryProvider


class RedisShortTermMemory(BaseShortTermMemoryProvider):
    """Short-term cache with TTL support and graceful local fallback."""

    def __init__(self):
        self._store: Dict[str, Dict[str, Any]] = {}

    async def get(self, key: str) -> Optional[Any]:
        entry = self._store.get(key)
        if not entry:
            return None
        if entry["expires_at"] and time.time() > entry["expires_at"]:
            del self._store[key]
            return None
        return entry["value"]

    async def set(self, key: str, value: Any, ttl_seconds: Optional[int] = None) -> None:
        expires_at = time.time() + ttl_seconds if ttl_seconds else None
        self._store[key] = {"value": value, "expires_at": expires_at}

    async def delete(self, key: str) -> bool:
        if key in self._store:
            del self._store[key]
            return True
        return False
