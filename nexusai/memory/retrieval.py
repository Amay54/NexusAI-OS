"""
Context Retrieval & Compression Engine for NexusAI OS.
Automatically retrieves recent conversation, current workflow state, relevant historical executions,
similar previous projects, and relevant lessons learned, compressing them to prevent token overflow.
"""
from typing import Any, Dict, List, Optional
from nexusai.memory.manager import memory_manager
from nexusai.services.knowledge_graph import knowledge_graph


class ContextRetrievalEngine:
    """Agent context aggregation and intelligent compression engine."""

    def __init__(self, max_context_chars: int = 4000):
        self.memory_mgr = memory_manager
        self.graph_svc = knowledge_graph
        self.max_context_chars = max_context_chars

    async def build_compressed_context(
        self,
        agent_name: str,
        task_prompt: str,
        workflow_id: Optional[int] = None,
        project_id: Optional[str] = None
    ) -> Dict[str, Any]:
        """Asynchronously gathers short-term state, long-term vector lessons, and graph topology."""

        # 1. Retrieve Short-Term & Long-Term Vector Memories
        raw_ctx = await self.memory_mgr.retrieve_context_for_agent(agent_name, task_prompt)
        short_term = raw_ctx.get("short_term_state") or {}
        lessons = raw_ctx.get("relevant_experiences") or []

        # 2. Retrieve Graph Relationships if project_id is specified
        graph_rels = []
        if project_id:
            graph_rels = await self.graph_svc.query_relationships(project_id)

        # 3. Intelligent Context Compression
        compressed_lessons = []
        current_char_count = 0

        for l in lessons:
            content = l.get("content", "")
            if current_char_count + len(content) <= self.max_context_chars:
                compressed_lessons.append(content)
                current_char_count += len(content)
            else:
                # Truncate remaining
                avail = self.max_context_chars - current_char_count
                if avail > 50:
                    compressed_lessons.append(content[:avail] + "...")
                break

        return {
            "agent_name": agent_name,
            "short_term_state": short_term,
            "compressed_lessons": compressed_lessons,
            "graph_relationships": graph_rels,
            "total_context_chars": current_char_count,
            "compressed": len(lessons) > len(compressed_lessons)
        }


context_retrieval_engine = ContextRetrievalEngine()
