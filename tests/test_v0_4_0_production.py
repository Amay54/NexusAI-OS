"""
Master Production Release Test Suite for NexusAI OS (v0.4.0).
Verifies End-to-End Project Synthesis, Sandbox Test Execution, Demo Workflows Engine, WebSocket Telemetry Manager, and FastAPI Control Plane.
"""
import pytest
from httpx import ASGITransport, AsyncClient

from nexusai.services.project_synthesizer import project_synthesizer
from nexusai.services.demo_workflows import demo_workflows_registry
from nexusai.api.websocket_api import ws_manager
from nexusai.main import app


@pytest.mark.asyncio
async def test_end_to_end_production_project_synthesis():
    """Test full multi-file software synthesis and sandbox verification."""
    artifact = await project_synthesizer.synthesize_full_project(
        project_name="FastAPI Inventory Management System",
        goal_prompt="Build a FastAPI Inventory System with PostgreSQL schema and unit tests"
    )

    assert artifact.project_name == "FastAPI Inventory Management System"
    assert "main.py" in artifact.files
    assert "test_main.py" in artifact.files
    assert "requirements.txt" in artifact.files
    assert len(artifact.dockerfile) > 0
    assert len(artifact.docker_compose_yml) > 0
    assert artifact.quality_score >= 0.95


@pytest.mark.asyncio
async def test_built_in_demo_workflows_engine():
    """Test demo workflow listing and execution."""
    demos = demo_workflows_registry.list_demo_workflows()
    assert len(demos) == 5

    inventory_demo = demos[0]
    artifact = await demo_workflows_registry.execute_demo_workflow(inventory_demo.demo_id)
    assert artifact.project_name == inventory_demo.title
    assert "main.py" in artifact.files


@pytest.mark.asyncio
async def test_websocket_telemetry_manager():
    """Test WebSocket connection manager broadcast capabilities."""
    # Verify manager initialization
    assert hasattr(ws_manager, "broadcast")
    await ws_manager.broadcast({"event_type": "TEST_EVENT", "status": "OK"})


@pytest.mark.asyncio
async def test_v0_4_0_production_rest_apis():
    """Test FastAPI production endpoints."""
    async with AsyncClient(transport=ASGITransport(app=app), base_url="http://test") as client:
        # 1. Health check
        health_res = await client.get("/health")
        assert health_res.status_code == 200
        assert health_res.json()["version"] == "0.4.0"

        # 2. List demo workflows
        demo_res = await client.get("/api/v1/demo/workflows")
        assert demo_res.status_code == 200
        assert demo_res.json()["count"] == 5

        # 3. Execute demo workflow API
        exec_res = await client.post("/api/v1/demo/execute/demo_inventory_system")
        assert exec_res.status_code == 200
        assert "files" in exec_res.json()
