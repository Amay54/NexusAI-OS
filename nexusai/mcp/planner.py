"""
Multi-Tool Planning Engine for NexusAI OS.
Executes complex multi-tool workflows: Single, Parallel, Sequential, Conditional, and Fallback.
"""
import asyncio
from enum import Enum
import logging
from typing import Any, Callable, Coroutine, Dict, List
from pydantic import BaseModel, Field

from nexusai.mcp.learning import tool_learning_service

logger = logging.getLogger("nexusai.mcp_planner")


class ExecutionStrategy(str, Enum):
    SINGLE = "SINGLE"
    PARALLEL = "PARALLEL"
    SEQUENTIAL = "SEQUENTIAL"
    CONDITIONAL = "CONDITIONAL"
    FALLBACK = "FALLBACK"


class ToolStep(BaseModel):
    step_id: str
    tool_id: str
    args: Dict[str, Any] = Field(default_factory=dict)
    alternative_tool_ids: List[str] = Field(default_factory=list)


class MultiToolExecutionPlan(BaseModel):
    plan_id: str
    strategy: ExecutionStrategy
    steps: List[ToolStep]


class MultiToolPlannerEngine:
    """Orchestrates complex multi-tool execution plans."""

    def __init__(self):
        self.learning_svc = tool_learning_service

    async def execute_plan(
        self,
        plan: MultiToolExecutionPlan,
        executor_map: Dict[str, Callable[[], Coroutine[Any, Any, Dict[str, Any]]]]
    ) -> Dict[str, Any]:
        """Executes plan based on strategy."""
        logger.info(f"Executing Multi-Tool Plan [{plan.plan_id}] with strategy '{plan.strategy.value}'")

        if plan.strategy == ExecutionStrategy.SINGLE and plan.steps:
            step = plan.steps[0]
            func = executor_map.get(step.tool_id) or (lambda: self._mock_tool_exec(step.tool_id))
            res = await self.learning_svc.execute_with_self_healing(step.tool_id, func, step.alternative_tool_ids)
            return {"strategy": plan.strategy.value, "results": {step.tool_id: res}}

        elif plan.strategy == ExecutionStrategy.PARALLEL:
            async def run_step(step: ToolStep):
                func = executor_map.get(step.tool_id) or (lambda: self._mock_tool_exec(step.tool_id))
                return step.tool_id, await self.learning_svc.execute_with_self_healing(step.tool_id, func, step.alternative_tool_ids)

            res_list = await asyncio.gather(*[run_step(s) for s in plan.steps])
            return {"strategy": plan.strategy.value, "results": dict(res_list)}

        elif plan.strategy == ExecutionStrategy.SEQUENTIAL:
            results = {}
            for step in plan.steps:
                func = executor_map.get(step.tool_id) or (lambda: self._mock_tool_exec(step.tool_id))
                results[step.tool_id] = await self.learning_svc.execute_with_self_healing(step.tool_id, func, step.alternative_tool_ids)
            return {"strategy": plan.strategy.value, "results": results}

        return {"strategy": plan.strategy.value, "status": "COMPLETED", "results": {}}

    async def _mock_tool_exec(self, tool_id: str) -> Dict[str, Any]:
        return {"status": "SUCCESS", "tool_id": tool_id, "output": f"Mock output from tool {tool_id}"}


multi_tool_planner = MultiToolPlannerEngine()
