"""
Dynamic Tool Knowledge Base & Registry for NexusAI OS.
Stores discovered MCP tools, metadata, permissions, embeddings, and real-time health/reliability metrics.
"""
from enum import Enum
from datetime import datetime, timezone
import uuid
from typing import Any, Dict, List, Optional
from pydantic import BaseModel, Field


class RiskLevel(str, Enum):
    LOW = "LOW"
    MEDIUM = "MEDIUM"
    HIGH = "HIGH"
    CRITICAL = "CRITICAL"


class ToolMetadata(BaseModel):
    """Schema for discovered MCP tools."""
    tool_id: str = Field(..., description="Unique tool identifier")
    tool_name: str = Field(..., description="Human-readable tool name")
    provider: str = Field(default="core", description="MCP provider/plugin package name")
    version: str = Field(default="1.0.0")
    description: str = Field(..., description="Capability description")
    parameters: Dict[str, Any] = Field(default_factory=dict)
    permissions: List[str] = Field(default_factory=list)
    supported_agents: List[str] = Field(default_factory=list)
    risk_level: RiskLevel = Field(default=RiskLevel.LOW)
    examples: List[str] = Field(default_factory=list)
    embedding: List[float] = Field(default_factory=list)
    health_status: str = Field(default="HEALTHY")
    reliability_score: float = Field(default=1.0, ge=0.0, le=1.0)
    total_calls: int = Field(default=0)
    success_count: int = Field(default=0)
    failure_count: int = Field(default=0)
    avg_latency_ms: float = Field(default=0.0)
    created_at: str = Field(default_factory=lambda: datetime.now(timezone.utc).isoformat())


class ToolRegistry:
    """Central Tool Knowledge Base managing discovered tools."""

    def __init__(self):
        self.tools: Dict[str, ToolMetadata] = {}

    def register_tool(self, tool: ToolMetadata) -> None:
        """Registers or updates a discovered tool in the registry."""
        self.tools[tool.tool_id] = tool

    def get_tool(self, tool_id: str) -> Optional[ToolMetadata]:
        return self.tools.get(tool_id)

    def list_tools(self, category: Optional[str] = None) -> List[ToolMetadata]:
        return list(self.tools.values())

    def update_tool_telemetry(self, tool_id: str, success: bool, latency_ms: float) -> None:
        """Updates tool usage counts, latency, and reliability scores dynamically."""
        tool = self.tools.get(tool_id)
        if not tool:
            return

        tool.total_calls += 1
        if success:
            tool.success_count += 1
        else:
            tool.failure_count += 1

        tool.reliability_score = round(tool.success_count / max(tool.total_calls, 1), 3)
        tool.avg_latency_ms = round(
            ((tool.avg_latency_ms * (tool.total_calls - 1)) + latency_ms) / tool.total_calls, 2
        )
        if tool.reliability_score < 0.6:
            tool.health_status = "DEGRADED"


tool_registry = ToolRegistry()
