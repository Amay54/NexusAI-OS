"""
Vector Embedding Provider Abstraction for NexusAI OS.
Abstracts embedding backends (Gemini Embeddings, Ollama Embeddings, SentenceTransformers, Mock).
"""
from abc import ABC, abstractmethod
import math
import re
from typing import List, Optional
from nexusai.core.config import settings


class BaseEmbeddingProvider(ABC):
    """Abstract interface for vector embedding generation."""

    @abstractmethod
    async def embed_text(self, text: str) -> List[float]:
        pass

    @abstractmethod
    async def embed_batch(self, texts: List[str]) -> List[List[float]]:
        pass


class MockEmbeddingProvider(BaseEmbeddingProvider):
    """Deterministic hash-based mock embedding provider for testing and fallback."""

    def __init__(self, vector_dim: int = 64):
        self.vector_dim = vector_dim

    async def embed_text(self, text: str) -> List[float]:
        words = re.findall(r"\w+", text.lower())
        vec = [0.0] * self.vector_dim
        for w in words:
            idx = abs(hash(w)) % self.vector_dim
            vec[idx] += 1.0

        norm = math.sqrt(sum(x * x for x in vec)) or 1.0
        return [round(x / norm, 4) for x in vec]

    async def embed_batch(self, texts: List[str]) -> List[List[float]]:
        return [await self.embed_text(t) for t in texts]


class EmbeddingService:
    """Configurable Embedding Provider Manager."""

    def __init__(self, provider: Optional[BaseEmbeddingProvider] = None):
        self.provider = provider or MockEmbeddingProvider()

    def set_provider(self, provider: BaseEmbeddingProvider) -> None:
        self.provider = provider

    async def embed_text(self, text: str) -> List[float]:
        return await self.provider.embed_text(text)

    async def embed_batch(self, texts: List[str]) -> List[List[float]]:
        return await self.provider.embed_batch(texts)


embedding_service = EmbeddingService()
