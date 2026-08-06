"""
Negotiation & Debate Engine for NexusAI OS.
Executes structured multi-agent debates, confidence-weighted voting, conflict resolution, and HITL fallback.
"""
from typing import Any, Dict, List, Optional
from pydantic import BaseModel, Field

from nexusai.services.consensus import consensus_engine, AgentVote, VotingStrategy
from nexusai.services.hitl import hitl_service


class DebateStatement(BaseModel):
    agent_name: str
    argument: str
    confidence: float


class DebateSession(BaseModel):
    topic: str
    statements: List[DebateStatement]
    resolved: bool
    final_consensus: str
    escalated_to_hitl: bool = False


class NegotiationEngine:
    """Manages structured agent debate and conflict escalation."""

    async def execute_agent_debate(
        self,
        topic: str,
        statements: List[DebateStatement],
        workflow_id: int = 1
    ) -> DebateSession:
        """Runs structured multi-agent debate and voting resolution."""
        votes = [
            AgentVote(
                agent_name=s.agent_name,
                decision="APPROVE" if s.confidence >= 0.6 else "REJECT",
                confidence=s.confidence,
                reasoning=s.argument
            )
            for s in statements
        ]

        consensus_res = await consensus_engine.evaluate_consensus(
            topic=topic,
            votes=votes,
            strategy=VotingStrategy.CONFIDENCE_WEIGHTED
        )

        escalated = False
        if not consensus_res.approved and consensus_res.conflict_resolved is False:
            # Escalate conflict to HITL
            await hitl_service.request_approval(
                workflow_id=workflow_id,
                agent_name="Debate Engine",
                action_type="CONFLICT_RESOLUTION",
                description=f"Agent disagreement on topic '{topic}'. Human approval required.",
                danger_level="HIGH"
            )
            escalated = True

        return DebateSession(
            topic=topic,
            statements=statements,
            resolved=consensus_res.approved,
            final_consensus="APPROVED" if consensus_res.approved else "REJECTED",
            escalated_to_hitl=escalated
        )


negotiation_engine = NegotiationEngine()
