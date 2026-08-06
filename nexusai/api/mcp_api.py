"""
Adaptive MCP REST API Routers for NexusAI OS (v0.2.2).
Provides endpoints for MCP tool discovery, tool catalog, reasoning, metrics, and multi-tool execution.
"""
from typing import Any, Dict, List, Optional
from fastapi import APIRouter, HTTPException, Query

from nexusai.mcp.registry import tool_registry
from nexusai.mcp.engine import discovery_engine
from nexusai.mcp.reasoning import tool_reasoning_engine
from nexusai.mcp.planner import multi_tool_planner, MultiToolExecutionPlan, ExecutionStrategy, ToolStep

mcp_router = APIRouter(prefix="/mcp", tags=["Adaptive MCP Ecosystem"])


@mcp_router.get("/tools")
async def list_mcp_tools():
    """Lists all discovered MCP tools in the Tool Knowledge Base."""
    tools = tool_registry.list_tools()
    return {"count": len(tools), "tools": [t.model_dump() for t in tools]}


@mcp_router.get("/tools/{tool_id}")
async def get_mcp_tool_details(tool_id: str):
    """Gets detailed metadata, permissions, and reliability stats for a tool."""
    tool = tool_registry.get_tool(tool_id)
    if not tool:
        raise HTTPException(status_code=404, detail=f"MCP Tool #{tool_id} not found in Knowledge Base")
    return tool.model_dump()


@mcp_router.post("/tools/discover")
async def trigger_mcp_discovery():
    """Triggers automatic discovery, vector indexing, and registry update for all MCP tools."""
    discovered = await discovery_engine.discover_and_index_all_tools()
    return {"status": "SUCCESS", "discovered_count": len(discovered), "tools": [t.model_dump() for t in discovered]}


@mcp_router.get("/catalog")
async def get_mcp_tool_catalog():
    """Returns the tool catalog grouped by provider and capability."""
    all_tools = tool_registry.list_tools()
    catalog: Dict[str, List[Dict[str, Any]]] = {}

    for t in all_tools:
        prov_tools = catalog.setdefault(t.provider, [])
        prov_tools.append({
            "tool_id": t.tool_id,
            "tool_name": t.tool_name,
            "description": t.description,
            "risk_level": t.risk_level.value,
            "reliability_score": t.reliability_score
        })

    return {"provider_count": len(catalog), "catalog": catalog}


@mcp_router.post("/evaluate")
async def evaluate_task_tools(task_prompt: str, agent_name: str = "Developer Agent"):
    """Evaluates task prompt against Tool Knowledge Base to suggest optimal tools."""
    reasonings = await tool_reasoning_engine.evaluate_task_and_select_tools(task_prompt, agent_name)
    return {"task_prompt": task_prompt, "suggested_tools_count": len(reasonings), "reasonings": [r.model_dump() for r in reasonings]}


@mcp_router.get("/metrics")
async def get_mcp_tool_metrics():
    """Returns operational metrics: tool execution latency, success rates, reliability scores."""
    all_tools = tool_registry.list_tools()
    metrics = []

    for t in all_tools:
        metrics.append({
            "tool_id": t.tool_id,
            "tool_name": t.tool_name,
            "provider": t.provider,
            "total_calls": t.total_calls,
            "reliability_score": t.reliability_score,
            "health_status": t.health_status,
            "avg_latency_ms": t.avg_latency_ms
        })

    return {"total_registered_tools": len(all_tools), "tool_metrics": metrics}


@mcp_router.post("/execute")
async def execute_multi_tool_plan(plan: MultiToolExecutionPlan):
    """Executes a multi-tool execution plan (Single, Parallel, Sequential, Fallback)."""
    res = await multi_tool_planner.execute_plan(plan, executor_map={})
    return res
