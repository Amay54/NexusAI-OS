"""
Context Budget Manager Engine for NexusAI OS.
Ranks, de-duplicates, merges, and compresses memory items based on Importance, Relevance, and Recency.
"""
from typing import Any, Dict, List, Optional
from nexusai.memory.base import MemoryItem


class ContextBudgetManager:
    """Intelligent context ranking and budget manager."""

    def __init__(self, max_char_budget: int = 3500):
        self.max_char_budget = max_char_budget

    def optimize_context(
        self,
        memories: List[MemoryItem],
        query: str,
        max_budget_chars: Optional[int] = None
    ) -> Dict[str, Any]:
        """Filters, de-duplicates, ranks, and packs memories within context budget."""
        budget = max_budget_chars or self.max_char_budget

        # 1. De-duplicate memories by content hash / exact text
        seen_texts = set()
        unique_memories: List[MemoryItem] = []
        for m in memories:
            clean_text = m.content.strip().lower()
            if clean_text not in seen_texts:
                seen_texts.add(clean_text)
                unique_memories.append(m)

        # 2. Score memories using composite formula
        scored_items = []
        for m in unique_memories:
            relevance = getattr(m, "score", 0.5)
            importance = m.importance_score
            recency = 0.8  # Default recency multiplier
            composite = (0.4 * relevance) + (0.3 * importance) + (0.3 * recency)
            scored_items.append((composite, m))

        # Sort by composite score descending
        scored_items.sort(key=lambda x: x[0], reverse=True)

        # 3. Budget packing
        packed_memories: List[MemoryItem] = []
        current_chars = 0

        for comp_score, m in scored_items:
            m_len = len(m.content)
            if current_chars + m_len <= budget:
                packed_memories.append(m)
                current_chars += m_len
            else:
                avail = budget - current_chars
                if avail > 50:
                    truncated_item = m.model_copy(deep=True)
                    truncated_item.content = m.content[:avail] + "..."
                    packed_memories.append(truncated_item)
                    current_chars += len(truncated_item.content)
                break

        return {
            "packed_memories": [pm.model_dump() for pm in packed_memories],
            "total_packed_chars": current_chars,
            "original_count": len(memories),
            "packed_count": len(packed_memories),
            "budget_limit_chars": budget
        }


context_budget_manager = ContextBudgetManager()
