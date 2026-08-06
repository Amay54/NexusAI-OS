"""
Multi-Agent Consensus & Voting Engine for NexusAI OS.
Facilitates majority voting, confidence-weighted voting, consensus agreement, and conflict resolution across agents.
"""
from enum import Enum
import logging
from typing import Any, Dict, List
from pydantic import BaseModel, Field

logger = logging.getLogger("nexusai.consensus")


class VotingStrategy(str, Enum):
    MAJORITY = "MAJORITY"
    CONFIDENCE_WEIGHTED = "CONFIDENCE_WEIGHTED"
    UNANIMOUS = "UNANIMOUS"


class AgentVote(BaseModel):
    agent_name: str
    decision: str  # APPROVE, REJECT, AMEND
    confidence: float = Field(default=1.0, ge=0.0, le=1.0)
    reasoning: str


class ConsensusResult(BaseModel):
    topic: str
    strategy: VotingStrategy
    approved: bool
    total_votes: int
    approval_count: int
    rejection_count: int
    weighted_score: float
    conflict_resolved: bool = False
    details: List[AgentVote]


class ConsensusEngine:
    """Multi-Agent Voting and Conflict Resolution Engine."""

    async def evaluate_consensus(
        self,
        topic: str,
        votes: List[AgentVote],
        strategy: VotingStrategy = VotingStrategy.CONFIDENCE_WEIGHTED
    ) -> ConsensusResult:
        """Evaluates votes across agents based on strategy."""
        logger.info(f"Evaluating multi-agent consensus for topic '{topic}' using strategy '{strategy.value}'...")
        total_votes = len(votes)
        if total_votes == 0:
            return ConsensusResult(
                topic=topic,
                strategy=strategy,
                approved=False,
                total_votes=0,
                approval_count=0,
                rejection_count=0,
                weighted_score=0.0,
                details=[]
            )

        approval_count = sum(1 for v in votes if v.decision.upper() == "APPROVE")
        rejection_count = total_votes - approval_count

        if strategy == VotingStrategy.MAJORITY:
            approved = approval_count > (total_votes / 2)
            weighted_score = approval_count / total_votes
        elif strategy == VotingStrategy.CONFIDENCE_WEIGHTED:
            weighted_approvals = sum(v.confidence for v in votes if v.decision.upper() == "APPROVE")
            total_confidence = sum(v.confidence for v in votes) or 1.0
            weighted_score = round(weighted_approvals / total_confidence, 3)
            approved = weighted_score >= 0.6
        else:  # UNANIMOUS
            approved = (approval_count == total_votes)
            weighted_score = 1.0 if approved else 0.0

        return ConsensusResult(
            topic=topic,
            strategy=strategy,
            approved=approved,
            total_votes=total_votes,
            approval_count=approval_count,
            rejection_count=rejection_count,
            weighted_score=weighted_score,
            conflict_resolved=(rejection_count > 0 and approved),
            details=votes
        )


consensus_engine = ConsensusEngine()
