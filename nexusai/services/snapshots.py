"""
Workflow Snapshot & Rollback Engine for NexusAI OS.
Periodically creates immutable workflow state snapshots, allowing diff comparison, restoration, and rollbacks.
"""
from datetime import datetime, timezone
import uuid
from typing import Any, Dict, List, Optional
from pydantic import BaseModel, Field

from nexusai.services.state_persistence import AgentStateCheckpoint, state_persistence_manager


class WorkflowSnapshot(BaseModel):
    snapshot_id: str = Field(default_factory=lambda: str(uuid.uuid4()))
    workflow_id: int
    step_number: int
    checkpoint: AgentStateCheckpoint
    created_at: str = Field(default_factory=lambda: datetime.now(timezone.utc).isoformat())


class WorkflowSnapshotManager:
    """Snapshot manager facilitating diff comparison and workflow rollbacks."""

    def __init__(self):
        self.snapshots: Dict[str, WorkflowSnapshot] = {}
        self.workflow_snapshots: Dict[int, List[WorkflowSnapshot]] = {}

    async def create_snapshot(self, workflow_id: int, checkpoint: AgentStateCheckpoint) -> WorkflowSnapshot:
        """Creates an immutable snapshot of workflow execution state."""
        wf_snaps = self.workflow_snapshots.setdefault(workflow_id, [])
        step_number = len(wf_snaps) + 1

        snap = WorkflowSnapshot(
            workflow_id=workflow_id,
            step_number=step_number,
            checkpoint=checkpoint
        )
        self.snapshots[snap.snapshot_id] = snap
        wf_snaps.append(snap)
        return snap

    async def get_snapshots_for_workflow(self, workflow_id: int) -> List[WorkflowSnapshot]:
        return self.workflow_snapshots.get(workflow_id, [])

    async def compare_snapshots(self, snap_a_id: str, snap_b_id: str) -> Dict[str, Any]:
        """Compares two snapshots and returns state diff."""
        snap_a = self.snapshots.get(snap_a_id)
        snap_b = self.snapshots.get(snap_b_id)

        if not snap_a or not snap_b:
            raise ValueError("Invalid snapshot ID(s) provided for comparison.")

        diff = {
            "workflow_id": snap_a.workflow_id,
            "snap_a": {"id": snap_a.snapshot_id, "step": snap_a.step_number, "status": snap_a.checkpoint.execution_status},
            "snap_b": {"id": snap_b.snapshot_id, "step": snap_b.step_number, "status": snap_b.checkpoint.execution_status},
            "agent_changed": snap_a.checkpoint.current_agent != snap_b.checkpoint.current_agent,
            "status_changed": snap_a.checkpoint.execution_status != snap_b.checkpoint.execution_status
        }
        return diff

    async def rollback_to_snapshot(self, workflow_id: int, snapshot_id: str) -> AgentStateCheckpoint:
        """Rolls back workflow state to a specific snapshot."""
        snap = self.snapshots.get(snapshot_id)
        if not snap or snap.workflow_id != workflow_id:
            raise ValueError(f"Snapshot #{snapshot_id} not found for Workflow #{workflow_id}")

        await state_persistence_manager.save_checkpoint(snap.checkpoint)
        return snap.checkpoint


snapshot_manager = WorkflowSnapshotManager()
