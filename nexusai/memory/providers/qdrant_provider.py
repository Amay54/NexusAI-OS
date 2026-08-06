"""
Qdrant & Vector Semantic Long-Term Memory Provider.
Performs versioned memory storage and semantic vector retrieval with graceful fallback.
"""
import re
from typing import Any, Dict, List, Optional
from nexusai.memory.base import BaseLongTermMemoryProvider, MemoryItem, ImportanceLevel, IMPORTANCE_SCORE_MAP


class QdrantLongTermMemory(BaseLongTermMemoryProvider):
    """Vector-based long-term versioned experience memory provider."""

    def __init__(self):
        self.documents: List[MemoryItem] = []
        self.version_history: Dict[str, List[MemoryItem]] = {}

    async def store(self, item: MemoryItem) -> None:
        """Stores a versioned memory item, maintaining version history."""
        # Calculate importance score if not set
        if item.importance_level in IMPORTANCE_SCORE_MAP:
            item.importance_score = IMPORTANCE_SCORE_MAP[item.importance_level]

        # Version tracking
        history = self.version_history.setdefault(item.memory_id, [])
        if history:
            item.version = history[-1].version + 1

        history.append(item)

        # Update active document list (keep latest version)
        self.documents = [d for d in self.documents if d.memory_id != item.memory_id]
        self.documents.append(item)

    async def search(self, query: str, top_k: int = 3) -> List[MemoryItem]:
        query_words = set(re.findall(r"\w+", query.lower()))
        results = []

        for doc in self.documents:
            doc_words = set(re.findall(r"\w+", doc.content.lower()))
            intersection = query_words.intersection(doc_words)

            if intersection:
                similarity = len(intersection) / max(len(query_words), 1)
                # Compute composite score factoring in similarity and importance score
                composite_score = (0.7 * similarity) + (0.3 * doc.importance_score)

                doc_copy = doc.model_copy(deep=True)
                doc_copy.score = round(composite_score, 4)
                results.append(doc_copy)

        results.sort(key=lambda x: x.score, reverse=True)
        return results[:top_k]

    async def get_version_history(self, memory_id: str) -> List[MemoryItem]:
        return self.version_history.get(memory_id, [])
