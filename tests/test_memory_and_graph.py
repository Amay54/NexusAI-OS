"""
Tests for Provider-Agnostic Memory Engine and Knowledge Graph Service.
"""
import pytest
from nexusai.memory.manager import MemoryManager
from nexusai.memory.providers.redis_provider import RedisShortTermMemory
from nexusai.memory.providers.qdrant_provider import QdrantLongTermMemory
from nexusai.services.knowledge_graph import KnowledgeGraphService, InMemoryGraphProvider


@pytest.mark.asyncio
async def test_provider_agnostic_memory_engine():
    """Verify memory operations over Redis and Qdrant provider interfaces."""
    redis_mem = RedisShortTermMemory()
    qdrant_mem = QdrantLongTermMemory()
    manager = MemoryManager(short_term_provider=redis_mem, long_term_provider=qdrant_mem)

    # 1. Short-Term Cache with TTL
    await manager.short_term.set("state_Developer Agent", {"active": True}, ttl_seconds=10)
    state = await manager.short_term.get("state_Developer Agent")
    assert state == {"active": True}

    # 2. Long-Term Vector Store
    await manager.store_experience("exp-nexus-1", "Always validate PostgreSQL Alembic migrations before push.")
    ctx = await manager.retrieve_context_for_agent("Developer Agent", "PostgreSQL Alembic migrations")

    assert ctx["short_term_state"] == {"active": True}
    assert len(ctx["relevant_experiences"]) > 0
    assert ctx["relevant_experiences"][0]["id"] == "exp-nexus-1"


@pytest.mark.asyncio
async def test_generic_knowledge_graph_service():
    """Verify Knowledge Graph service abstractions."""
    in_mem_provider = InMemoryGraphProvider()
    kg_service = KnowledgeGraphService(provider=in_mem_provider)

    await kg_service.add_node("proj-nexus", "Project", {"name": "NexusAI OS"})
    await kg_service.add_node("task-nexus-1", "Task", {"title": "Build Event Bus"})
    await kg_service.add_edge("proj-nexus", "task-nexus-1", "HAS_TASK")

    rel = await kg_service.query_relationships("proj-nexus", "HAS_TASK")
    assert len(rel) == 1
    assert rel[0]["target_node"]["id"] == "task-nexus-1"

    topology = await kg_service.get_full_graph_topology()
    assert topology["node_count"] == 2
    assert topology["edge_count"] == 1
