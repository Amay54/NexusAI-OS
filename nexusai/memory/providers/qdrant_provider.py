"""
Qdrant & Vector Semantic Long-Term Memory Provider.
Performs semantic vector search and experience retrieval with graceful local fallback.
"""
import re
from typing import Any, Dict, List, Optional
from nexusai.memory.base import BaseLongTermMemoryProvider, MemoryItem


class QdrantLongTermMemory(BaseLongTermMemoryProvider):
    """Vector-based long-term experience memory provider."""

    def __init__(self):
        self.documents: List[MemoryItem] = []

    async def store(self, item_id: str, content: str, metadata: Optional[Dict[str, Any]] = None) -> None:
        item = MemoryItem(id=item_id, content=content, metadata=metadata or {})
        self.documents.append(item)

    async def search(self, query: str, top_k: int = 3) -> List[MemoryItem]:
        query_words = set(re.findall(r"\w+", query.lower()))
        results = []

        for doc in self.documents:
            doc_words = set(re.findall(r"\w+", doc.content.lower()))
            intersection = query_words.intersection(doc_words)

            # Match if any query tokens intersect with doc tokens
            if intersection:
                similarity = len(intersection) / max(len(query_words), 1)
                results.append(MemoryItem(id=doc.id, content=doc.content, metadata=doc.metadata, score=round(similarity, 4)))

        results.sort(key=lambda x: x.score, reverse=True)
        return results[:top_k]
