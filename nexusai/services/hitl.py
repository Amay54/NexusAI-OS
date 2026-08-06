"""
Human-in-the-Loop (HITL) Approval Gate Service for NexusAI OS.
Pauses execution before dangerous operations (deployments, migrations, deletions, force pushes).
"""
from datetime import datetime, timezone
import uuid
from typing import Any, Dict, List, Optional
from pydantic import BaseModel, Field


class ApprovalRequest(BaseModel):
    approval_id: str = Field(default_factory=lambda: str(uuid.uuid4()))
    workflow_id: int
    agent_name: str
    action_type: str  # DEPLOYMENT, DB_MIGRATION, TERMINAL_EXEC, REPO_DELETE
    description: str
    danger_level: str = "HIGH"
    status: str = "PENDING"  # PENDING, APPROVED, REJECTED
    requested_at: str = Field(default_factory=lambda: datetime.now(timezone.utc).isoformat())
    resolved_at: Optional[str] = None
    approver: Optional[str] = None


class HITLService:
    """Human-in-the-Loop Safety Checkpoint Manager."""

    def __init__(self):
        self.pending_approvals: Dict[str, ApprovalRequest] = {}
        self.workflow_approvals: Dict[int, List[ApprovalRequest]] = {}

    async def request_approval(
        self,
        workflow_id: int,
        agent_name: str,
        action_type: str,
        description: str,
        danger_level: str = "HIGH"
    ) -> ApprovalRequest:
        """Creates a pending HITL approval request."""
        req = ApprovalRequest(
            workflow_id=workflow_id,
            agent_name=agent_name,
            action_type=action_type,
            description=description,
            danger_level=danger_level
        )
        self.pending_approvals[req.approval_id] = req
        self.workflow_approvals.setdefault(workflow_id, []).append(req)
        return req

    async def approve_action(self, approval_id: str, approver: str = "Human Reviewer") -> ApprovalRequest:
        """Approves a pending HITL action request."""
        req = self.pending_approvals.get(approval_id)
        if not req:
            raise ValueError(f"Approval request #{approval_id} not found.")

        req.status = "APPROVED"
        req.resolved_at = datetime.now(timezone.utc).isoformat()
        req.approver = approver
        return req

    async def reject_action(self, approval_id: str, approver: str = "Human Reviewer") -> ApprovalRequest:
        """Rejects a pending HITL action request."""
        req = self.pending_approvals.get(approval_id)
        if not req:
            raise ValueError(f"Approval request #{approval_id} not found.")

        req.status = "REJECTED"
        req.resolved_at = datetime.now(timezone.utc).isoformat()
        req.approver = approver
        return req

    async def get_pending_approvals(self, workflow_id: Optional[int] = None) -> List[ApprovalRequest]:
        if workflow_id:
            return [r for r in self.workflow_approvals.get(workflow_id, []) if r.status == "PENDING"]
        return [r for r in self.pending_approvals.values() if r.status == "PENDING"]


hitl_service = HITLService()
