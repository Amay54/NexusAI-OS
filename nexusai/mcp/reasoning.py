"""
Tool Reasoning Engine for NexusAI OS.
Evaluates agent prompts against Tool Knowledge Base to dynamically determine optimal tools, permissions, and execution strategy.
"""
import re
from typing import Any, Dict, List, Optional
from pydantic import BaseModel, Field

from nexusai.mcp.registry import ToolMetadata, tool_registry
from nexusai.memory.embeddings import embedding_service


class ToolSelectionReasoning(BaseModel):
    selected_tool: ToolMetadata
    fit_score: float
    reasoning_text: str
    required_permissions: List[str]
    combination_suggested: bool = False
    alternative_tools: List[str] = Field(default_factory=list)


class ToolReasoningEngine:
    """Evaluates task context and determines optimal tools and execution strategy."""

    def __init__(self):
        self.registry = tool_registry
        self.embed_svc = embedding_service

    async def evaluate_task_and_select_tools(
        self,
        task_prompt: str,
        agent_name: str,
        top_k: int = 3
    ) -> List[ToolSelectionReasoning]:
        """Evaluates tools using semantic similarity, agent support, and reliability scores."""
        all_tools = self.registry.list_tools()
        if not all_tools:
            return []

        prompt_vec = await self.embed_svc.embed_text(task_prompt)
        prompt_words = set(re.findall(r"\w+", task_prompt.lower()))

        scored_tools = []
        for t in all_tools:
            t_words = set(re.findall(r"\w+", (t.tool_name + " " + t.description).lower()))
            intersection = prompt_words.intersection(t_words)

            similarity = len(intersection) / max(len(prompt_words), 1)
            agent_bonus = 0.2 if agent_name in t.supported_agents else 0.0
            composite_score = (0.5 * similarity) + (0.3 * t.reliability_score) + (0.2 * agent_bonus)

            if composite_score > 0.05:
                scored_tools.append((composite_score, t))

        scored_tools.sort(key=lambda x: x[0], reverse=True)
        selected = scored_tools[:top_k]

        reasonings = []
        for score, tool in selected:
            reasoning = ToolSelectionReasoning(
                selected_tool=tool,
                fit_score=round(score, 3),
                reasoning_text=(
                    f"Selected tool '{tool.tool_name}' ({tool.tool_id}) for agent '{agent_name}'. "
                    f"Fit Score: {round(score, 3)}, Reliability: {tool.reliability_score}."
                ),
                required_permissions=tool.permissions,
                combination_suggested=(len(selected) > 1),
                alternative_tools=[t.tool_id for s, t in selected if t.tool_id != tool.tool_id]
            )
            reasonings.append(reasoning)

        return reasonings


tool_reasoning_engine = ToolReasoningEngine()
