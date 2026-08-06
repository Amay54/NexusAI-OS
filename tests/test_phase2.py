"""
NexusAI OS Phase 2 Test Suite (v0.2.0).
Verifies Intelligence Layer: Context Retrieval & Compression, Reflection Engine, State Persistence, and REST APIs.
"""
import pytest
from httpx import ASGITransport, AsyncClient

from nexusai.memory.retrieval import ContextRetrievalEngine
from nexusai.services.reflection import ReflectionService
from nexusai.services.state_persistence import StatePersistenceManager, AgentStateCheckpoint
from nexusai.services.knowledge_graph import knowledge_graph
from nexusai.main import app


@pytest.mark.asyncio
async def test_context_retrieval_and_compression():
    """Test context merging and token/character compression."""
    engine = ContextRetrievalEngine(max_context_chars=100)

    # Pre-populate memories
    await engine.memory_mgr.store_experience("exp-c1", "Lesson 1: Use async SQLAlchemy sessions.")
    await engine.memory_mgr.store_experience("exp-c2", "Lesson 2: Always set healthchecks on Docker containers.")

    ctx = await engine.build_compressed_context("Developer Agent", "SQLAlchemy sessions and Docker containers")

    assert ctx["agent_name"] == "Developer Agent"
    assert "compressed_lessons" in ctx
    assert ctx["total_context_chars"] <= 100


@pytest.mark.asyncio
async def test_reflection_service_generation_and_search():
    """Test workflow reflection report generation and searchable lesson index."""
    service = ReflectionService()

    report = await service.generate_workflow_reflection(
        workflow_id=301,
        goal_prompt="Build Microservice API",
        status="COMPLETED",
        timeline=[{"actor": "CEO Agent", "message": "Planning finished"}],
        artifacts={"api.py": "app = FastAPI()"}
    )

    assert report.workflow_id == 301
    assert report.status == "COMPLETED"
    assert len(report.successes) > 0

    # Search reflections
    search_res = await service.search_reflections("Microservice API")
    assert len(search_res) > 0


@pytest.mark.asyncio
async def test_state_persistence_and_interrupted_workflow_recovery():
    """Test saving state checkpoints and retrieving history records."""
    sp_mgr = StatePersistenceManager()

    cp = AgentStateCheckpoint(
        workflow_id=401,
        current_goal="Build E-Commerce System",
        current_agent="Developer Agent",
        execution_status="AWAITING_APPROVAL",
        retry_count=1
    )

    await sp_mgr.save_checkpoint(cp)
    restored = await sp_mgr.get_checkpoint(401)

    assert restored is not None
    assert restored.current_goal == "Build E-Commerce System"
    assert restored.execution_status == "AWAITING_APPROVAL"

    # Record LLM Call
    await sp_mgr.record_llm_call(401, "Developer Agent", "deepseek", 350.5, "Synthesize code")
    history = await sp_mgr.get_workflow_history(401)

    assert history is not None
    assert len(history.llm_metrics) == 1
    assert history.llm_metrics[0]["provider"] == "deepseek"


@pytest.mark.asyncio
async def test_intelligence_rest_apis():
    """Test FastAPI REST endpoints for Memory, Graph, Reflection, and History."""
    async with AsyncClient(transport=ASGITransport(app=app), base_url="http://test") as client:
        # 1. Health
        health_res = await client.get("/health")
        assert health_res.status_code == 200
        assert health_res.json()["version"] == "0.2.0"

        # 2. Graph topology
        graph_res = await client.get("/api/v1/graph")
        assert graph_res.status_code == 200
        assert "node_count" in graph_res.json()

        # 3. Memory search
        mem_res = await client.get("/api/v1/memory/search?q=SQLAlchemy")
        assert mem_res.status_code == 200
        assert "memories" in mem_res.json()
