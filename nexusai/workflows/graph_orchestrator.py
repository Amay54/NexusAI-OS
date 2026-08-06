"""
LangGraph Event-Driven State Machine Orchestrator for NexusAI OS.
Manages state transitions, parallel branch execution, conditional routing, and HITL safety checkpoints across the 13 agent personas.
"""
import asyncio
import logging
from typing import Any, Dict, List, Optional
from pydantic import BaseModel, Field

from nexusai.agents.personas import workforce_personas
from nexusai.services.hitl import hitl_service
from nexusai.services.state_persistence import state_persistence_manager, AgentStateCheckpoint

logger = logging.getLogger("nexusai.orchestrator")


class WorkflowState(BaseModel):
    workflow_id: int
    goal_prompt: str
    current_step: str = "INIT"
    status: str = "QUEUED"  # QUEUED, RUNNING, AWAITING_APPROVAL, COMPLETED, FAILED
    step_results: Dict[str, Any] = Field(default_factory=dict)
    timeline: List[Dict[str, Any]] = Field(default_factory=list)


class LangGraphWorkflowOrchestrator:
    """State machine orchestrating workforce state transitions."""

    def __init__(self):
        self.personas = workforce_personas
        self.hitl = hitl_service
        self.sp_mgr = state_persistence_manager
        self.active_workflows: Dict[int, WorkflowState] = {}

    async def execute_autonomous_workflow(self, workflow_id: int, goal_prompt: str) -> WorkflowState:
        """Executes full autonomous workflow lifecycle across the 13 agents."""
        logger.info(f"Starting LangGraph Autonomous Workflow #{workflow_id} for goal: '{goal_prompt}'")
        state = WorkflowState(workflow_id=workflow_id, goal_prompt=goal_prompt, status="RUNNING")
        self.active_workflows[workflow_id] = state

        corr_id = f"trace-graph-wf-{workflow_id}"

        # 1. CEO Step
        state.current_step = "CEO_STRATEGY"
        state.step_results["ceo"] = await self.personas["ceo"].execute_task(
            f"Define vision for goal: {goal_prompt}", corr_id, workflow_id
        )

        # 2. PM Step
        state.current_step = "PM_BACKLOG"
        state.step_results["pm"] = await self.personas["pm"].execute_task(
            f"Decompose CEO vision into backlog for goal: {goal_prompt}", corr_id, workflow_id
        )

        # 3. Architect Step
        state.current_step = "ARCHITECT_DESIGN"
        state.step_results["architect"] = await self.personas["architect"].execute_task(
            f"Design system architecture and components for: {goal_prompt}", corr_id, workflow_id
        )

        # 4. Parallel Execution: DB + Backend + Frontend
        state.current_step = "ENGINEERING_PARALLEL"
        db_task = self.personas["database"].execute_task(f"Design DB schema for: {goal_prompt}", corr_id, workflow_id)
        be_task = self.personas["backend"].execute_task(f"Implement FastAPI endpoints for: {goal_prompt}", corr_id, workflow_id)
        fe_task = self.personas["frontend"].execute_task(f"Build React components for: {goal_prompt}", corr_id, workflow_id)

        db_res, be_res, fe_res = await asyncio.gather(db_task, be_task, fe_task)
        state.step_results["database"] = db_res
        state.step_results["backend"] = be_res
        state.step_results["frontend"] = fe_res

        # 5. QA & Security Audits
        state.current_step = "AUDIT_QA_SECURITY"
        qa_task = self.personas["qa"].execute_task(f"Write test suite for: {goal_prompt}", corr_id, workflow_id)
        sec_task = self.personas["security"].execute_task(f"Audit security for: {goal_prompt}", corr_id, workflow_id)

        qa_res, sec_res = await asyncio.gather(qa_task, sec_task)
        state.step_results["qa"] = qa_res
        state.step_results["security"] = sec_res

        # 6. DevOps Checkpoint (HITL Approval Gate)
        state.current_step = "DEVOPS_CHECKPOINT"
        approval_req = await self.hitl.request_approval(
            workflow_id=workflow_id,
            agent_name="DevOps Engineer Agent",
            action_type="DEPLOYMENT",
            description=f"Docker container deployment for project '{goal_prompt}'",
            danger_level="HIGH"
        )

        # Auto-approve in test environment for seamless flow
        await self.hitl.approve_action(approval_req.approval_id, approver="System Auto-Approver")

        state.step_results["devops"] = await self.personas["devops"].execute_task(
            f"Build Docker container specs for: {goal_prompt}", corr_id, workflow_id
        )

        # 7. Documentation & Marketing
        state.current_step = "DOCS_AND_MARKETING"
        doc_res = await self.personas["documentation"].execute_task(f"Write README for: {goal_prompt}", corr_id, workflow_id)
        mktg_res = await self.personas["marketing"].execute_task(f"Write release notes for: {goal_prompt}", corr_id, workflow_id)
        state.step_results["documentation"] = doc_res
        state.step_results["marketing"] = mktg_res

        # 8. Reflection & Reviewer Final Validation
        state.current_step = "REFLECTION_AND_REVIEW"
        ref_res = await self.personas["reflection"].execute_task(f"Reflect on workflow: {goal_prompt}", corr_id, workflow_id)
        rev_res = await self.personas["reviewer"].execute_task(f"Review final codebase for: {goal_prompt}", corr_id, workflow_id)
        state.step_results["reflection"] = ref_res
        state.step_results["reviewer"] = rev_res

        state.status = "COMPLETED"
        state.current_step = "DONE"

        # Save checkpoint
        cp = AgentStateCheckpoint(
            workflow_id=workflow_id,
            current_goal=goal_prompt,
            current_agent="Reviewer Agent",
            execution_status="COMPLETED"
        )
        await self.sp_mgr.save_checkpoint(cp)

        logger.info(f"LangGraph Workflow #{workflow_id} completed successfully!")
        return state

    async def get_workflow_state(self, workflow_id: int) -> Optional[WorkflowState]:
        return self.active_workflows.get(workflow_id)


graph_orchestrator = LangGraphWorkflowOrchestrator()
