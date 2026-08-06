"""
Memory Retrieval Explainability Engine for NexusAI OS.
Records and details WHY specific memories were selected for agent context.
"""
from typing import Any, Dict, List, Optional
from pydantic import BaseModel, Field


class RetrievalExplanation(BaseModel):
    memory_id: str
    content_snippet: str
    similarity_score: float
    importance_score: float
    recency_score: float
    relationship_score: float
    composite_score: float
    explainability_rationale: str


class MemoryExplainabilityEngine:
    """Explainability tracker logging retrieval rationale."""

    def __init__(self):
        self.last_explanations: List[RetrievalExplanation] = []

    def log_retrieval_rationale(
        self,
        memory_id: str,
        content: str,
        similarity_score: float,
        importance_score: float,
        recency_score: float = 0.8,
        relationship_score: float = 0.5
    ) -> RetrievalExplanation:
        composite = (0.4 * similarity_score) + (0.3 * importance_score) + (0.15 * recency_score) + (0.15 * relationship_score)
        rationale = (
            f"Selected memory '{memory_id}' (Composite: {round(composite, 3)}) due to "
            f"similarity={similarity_score}, importance={importance_score}, recency={recency_score}."
        )

        exp = RetrievalExplanation(
            memory_id=memory_id,
            content_snippet=content[:100],
            similarity_score=similarity_score,
            importance_score=importance_score,
            recency_score=recency_score,
            relationship_score=relationship_score,
            composite_score=round(composite, 3),
            explainability_rationale=rationale
        )
        self.last_explanations.append(exp)
        return exp

    def get_latest_explanations(self, limit: int = 10) -> List[Dict[str, Any]]:
        return [e.model_dump() for e in self.last_explanations[-limit:]]


memory_explainability = MemoryExplainabilityEngine()
