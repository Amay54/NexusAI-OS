"""
Adaptive MCP Ecosystem & Dynamic Tool Intelligence Test Suite (v0.2.2).
Verifies Tool Discovery, Knowledge Base, Reasoning Engine, Learning/Self-Healing, Multi-Tool Planning, and REST APIs.
"""
import pytest
from httpx import ASGITransport, AsyncClient

from nexusai.mcp.registry import tool_registry, ToolMetadata, RiskLevel
from nexusai.mcp.engine import discovery_engine
from nexusai.mcp.reasoning import tool_reasoning_engine
from nexusai.mcp.learning import tool_learning_service
from nexusai.mcp.planner import multi_tool_planner, MultiToolExecutionPlan, ExecutionStrategy, ToolStep
from nexusai.main import app


@pytest.mark.asyncio
async def test_adaptive_tool_discovery_and_indexing():
    """Test automatic discovery and vector embedding indexing of MCP tools."""
    discovered = await discovery_engine.discover_and_index_all_tools()

    assert len(discovered) >= 6
    filesystem_tool = tool_registry.get_tool("mcp_filesystem_read")
    assert filesystem_tool is not None
    assert filesystem_tool.provider == "mcp-filesystem"
    assert len(filesystem_tool.embedding) > 0


@pytest.mark.asyncio
async def test_tool_reasoning_engine():
    """Test tool reasoning evaluation for task prompts."""
    await discovery_engine.discover_and_index_all_tools()

    reasonings = await tool_reasoning_engine.evaluate_task_and_select_tools(
        task_prompt="Read contents of local python script script.py",
        agent_name="Developer Agent"
    )

    assert len(reasonings) > 0
    top_tool = reasonings[0].selected_tool
    assert top_tool.tool_id == "mcp_filesystem_read"
    assert reasonings[0].fit_score > 0.0


@pytest.mark.asyncio
async def test_tool_learning_and_self_healing():
    """Test execution with automatic retries and self-healing failover."""
    await discovery_engine.discover_and_index_all_tools()

    call_count = 0

    async def flaky_tool_exec():
        nonlocal call_count
        call_count += 1
        if call_count < 2:
            raise RuntimeError("Temporary network timeout")
        return {"status": "SUCCESS", "output": "Flaky tool recovered"}

    # Execute with self-healing retry
    res = await tool_learning_service.execute_with_self_healing(
        tool_id="mcp_terminal_exec",
        executor_func=flaky_tool_exec,
        max_retries=2
    )

    assert res["status"] == "SUCCESS"
    tool_meta = tool_registry.get_tool("mcp_terminal_exec")
    assert tool_meta.total_calls > 0


@pytest.mark.asyncio
async def test_multi_tool_planning_execution():
    """Test parallel and sequential multi-tool plan execution."""
    plan = MultiToolExecutionPlan(
        plan_id="plan-test-1",
        strategy=ExecutionStrategy.PARALLEL,
        steps=[
            ToolStep(step_id="s1", tool_id="mcp_filesystem_read"),
            ToolStep(step_id="s2", tool_id="mcp_postgres_query")
        ]
    )

    res = await multi_tool_planner.execute_plan(plan, executor_map={})

    assert res["strategy"] == ExecutionStrategy.PARALLEL.value
    assert "mcp_filesystem_read" in res["results"]
    assert "mcp_postgres_query" in res["results"]


@pytest.mark.asyncio
async def test_adaptive_mcp_rest_apis():
    """Test FastAPI endpoints for MCP catalog, discovery, metrics, and reasoning."""
    async with AsyncClient(transport=ASGITransport(app=app), base_url="http://test") as client:
        # 1. Discover
        disc_res = await client.post("/api/v1/mcp/tools/discover")
        assert disc_res.status_code == 200
        assert disc_res.json()["discovered_count"] >= 6

        # 2. List tools
        tools_res = await client.get("/api/v1/mcp/tools")
        assert tools_res.status_code == 200
        assert tools_res.json()["count"] >= 6

        # 3. Catalog
        cat_res = await client.get("/api/v1/mcp/catalog")
        assert cat_res.status_code == 200
        assert "catalog" in cat_res.json()

        # 4. Metrics
        met_res = await client.get("/api/v1/mcp/metrics")
        assert met_res.status_code == 200
        assert met_res.json()["total_registered_tools"] >= 6
