"""
Architecture Decision Record (ADR) Generator for NexusAI OS.
Automatically generates markdown ADRs whenever the Executive Layer makes key architectural decisions.
"""
from datetime import datetime, timezone
from typing import Any, Dict, List
from pydantic import BaseModel, Field


class ArchitectureDecisionRecord(BaseModel):
    adr_id: str
    title: str
    context: str
    decision: str
    alternatives_considered: List[str]
    consequences: List[str]
    reasoning: str
    status: str = "ACCEPTED"
    created_at: str = Field(default_factory=lambda: datetime.now(timezone.utc).isoformat())


class ADRGeneratorService:
    """Generates markdown Architecture Decision Records."""

    def __init__(self):
        self.adrs: List[ArchitectureDecisionRecord] = []

    async def generate_adr(
        self,
        title: str,
        context: str,
        decision: str,
        alternatives: List[str],
        consequences: List[str],
        reasoning: str
    ) -> ArchitectureDecisionRecord:
        adr_num = len(self.adrs) + 1
        adr = ArchitectureDecisionRecord(
            adr_id=f"ADR-{adr_num:03d}",
            title=title,
            context=context,
            decision=decision,
            alternatives_considered=alternatives,
            consequences=consequences,
            reasoning=reasoning
        )
        self.adrs.append(adr)
        return adr

    def list_adrs(self) -> List[ArchitectureDecisionRecord]:
        return self.adrs


adr_generator = ADRGeneratorService()
