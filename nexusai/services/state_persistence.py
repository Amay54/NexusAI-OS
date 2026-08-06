"""
Agent State Persistence & Workflow History Manager for NexusAI OS.
Checkpoints agent execution state to support restoring interrupted workflows,
and tracks complete execution metrics (LLM latency, provider used, memory retrieved, tools used).
"""
from datetime import datetime, timezone
import logging
from typing import Any, Dict, List, Optional
from pydantic import BaseModel, Field

logger = logging.getLogger("nexusai.state_persistence")


class AgentStateCheckpoint(BaseModel):
    workflow_id: int
    current_goal: str
    current_plan: Optional[str] = None
    current_task: Optional[str] = None
    current_agent: str = "SYSTEM"
    current_tool: Optional[str] = None
    execution_status: str = "QUEUED"  # QUEUED, RUNNING, AWAITING_APPROVAL, COMPLETED, FAILED
    retry_count: int = 0
    last_update: str = Field(default_factory=lambda: datetime.now(timezone.utc).isoformat())
    context_snapshot: Dict[str, Any] = Field(default_factory=dict)


class WorkflowExecutionRecord(BaseModel):
    workflow_id: int
    trace_id: str
    timeline: List[Dict[str, Any]] = Field(default_factory=list)
    llm_metrics: List[Dict[str, Any]] = Field(default_factory=list)
    tool_invocations: List[Dict[str, Any]] = Field(default_factory=list)
    approvals: List[Dict[str, Any]] = Field(default_factory=list)


class StatePersistenceManager:
    """State Checkpoint and Workflow Execution History Tracker."""

    def __init__(self):
        self.checkpoints: Dict[int, AgentStateCheckpoint] = {}
        self.history_records: Dict[int, WorkflowExecutionRecord] = {}

    async def save_checkpoint(self, checkpoint: AgentStateCheckpoint) -> None:
        """Saves current agent state checkpoint."""
        checkpoint.last_update = datetime.now(timezone.utc).isoformat()
        self.checkpoints[checkpoint.workflow_id] = checkpoint
        logger.info(f"Saved state checkpoint for Workflow #{checkpoint.workflow_id} (Status: {checkpoint.execution_status})")

    async def get_checkpoint(self, workflow_id: int) -> Optional[AgentStateCheckpoint]:
        """Retrieves checkpoint to restore an interrupted workflow."""
        return self.checkpoints.get(workflow_id)

    async def record_llm_call(
        self,
        workflow_id: int,
        agent_name: str,
        provider: str,
        latency_ms: float,
        prompt_snippet: str
    ) -> None:
        """Records detailed LLM metrics for execution history."""
        rec = self.history_records.setdefault(
            workflow_id,
            WorkflowExecutionRecord(workflow_id=workflow_id, trace_id=f"trace-wf-{workflow_id}")
        )
        rec.llm_metrics.append({
            "timestamp": datetime.now(timezone.utc).isoformat(),
            "agent_name": agent_name,
            "provider": provider,
            "latency_ms": latency_ms,
            "prompt_snippet": prompt_snippet[:100]
        })

    async def record_tool_invocation(
        self,
        workflow_id: int,
        agent_name: str,
        tool_name: str,
        args: Dict[str, Any],
        success: bool
    ) -> None:
        """Records MCP tool invocations."""
        rec = self.history_records.setdefault(
            workflow_id,
            WorkflowExecutionRecord(workflow_id=workflow_id, trace_id=f"trace-wf-{workflow_id}")
        )
        rec.tool_invocations.append({
            "timestamp": datetime.now(timezone.utc).isoformat(),
            "agent_name": agent_name,
            "tool_name": tool_name,
            "args": args,
            "success": success
        })

    async def get_workflow_history(self, workflow_id: int) -> Optional[WorkflowExecutionRecord]:
        return self.history_records.get(workflow_id)


state_persistence_manager = StatePersistenceManager()
