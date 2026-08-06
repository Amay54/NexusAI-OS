"""
Agent Skill Profiles Engine for NexusAI OS.
Tracks domain experience, success rates, average execution times, preferred tools/LLMs, failure histories, and confidence scores.
"""
from typing import Any, Dict, List, Optional
from pydantic import BaseModel, Field


class AgentSkillProfile(BaseModel):
    agent_name: str
    domain_experience_level: str = "SENIOR"
    total_tasks_executed: int = 0
    successful_tasks: int = 0
    failed_tasks: int = 0
    success_rate: float = 1.0
    avg_execution_time_ms: float = 0.0
    confidence_score: float = 0.95
    preferred_tools: List[str] = Field(default_factory=list)
    preferred_llm_provider: str = "deepseek"
    failure_history: List[str] = Field(default_factory=list)


class AgentSkillRegistry:
    """Central Skill Profile Registry for dynamic task routing."""

    def __init__(self):
        self.profiles: Dict[str, AgentSkillProfile] = {}

    def get_profile(self, agent_name: str) -> AgentSkillProfile:
        if agent_name not in self.profiles:
            self.profiles[agent_name] = AgentSkillProfile(agent_name=agent_name)
        return self.profiles[agent_name]

    def record_task_outcome(self, agent_name: str, success: bool, execution_time_ms: float, error_msg: Optional[str] = None) -> None:
        prof = self.get_profile(agent_name)
        prof.total_tasks_executed += 1
        if success:
            prof.successful_tasks += 1
        else:
            prof.failed_tasks += 1
            if error_msg:
                prof.failure_history.append(error_msg)

        prof.success_rate = round(prof.successful_tasks / max(prof.total_tasks_executed, 1), 3)
        prof.avg_execution_time_ms = round(
            ((prof.avg_execution_time_ms * (prof.total_tasks_executed - 1)) + execution_time_ms) / prof.total_tasks_executed, 2
        )
        prof.confidence_score = round((0.7 * prof.success_rate) + (0.3 * (1.0 if prof.failed_tasks == 0 else 0.8)), 3)

    def list_skill_profiles(self) -> List[Dict[str, Any]]:
        return [p.model_dump() for p in self.profiles.values()]


agent_skill_registry = AgentSkillRegistry()
