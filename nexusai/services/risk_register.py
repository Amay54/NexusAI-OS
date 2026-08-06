"""
Live Risk Register Manager for NexusAI OS.
Maintains continuous risk items with Probability, Impact, Severity, Mitigation Strategy, Owner, and Status.
"""
from typing import Any, Dict, List, Optional
from pydantic import BaseModel, Field


class RiskItem(BaseModel):
    risk_id: str
    description: str
    probability: float = Field(ge=0.0, le=1.0)
    impact: str  # HIGH, MEDIUM, LOW
    severity_score: float = Field(ge=0.0, le=100.0)
    mitigation_strategy: str
    owner: str
    current_status: str = "OPEN"  # OPEN, MITIGATED, CLOSED


class RiskRegisterManager:
    """Manages executive Risk Register."""

    def __init__(self):
        self.risks: List[RiskItem] = [
            RiskItem(
                risk_id="RISK-001",
                description="Container port collision on concurrent devops runs",
                probability=0.10,
                impact="MEDIUM",
                severity_score=25.0,
                mitigation_strategy="Use dynamic ephemeral port allocation in Docker sandbox",
                owner="DevOps Engineer Agent",
                current_status="MITIGATED"
            ),
            RiskItem(
                risk_id="RISK-002",
                description="LLM provider rate limit timeout on peak planning loads",
                probability=0.05,
                impact="HIGH",
                severity_score=30.0,
                mitigation_strategy="Automatic failover to local Ollama fallback provider",
                owner="Intelligent Router",
                current_status="MITIGATED"
            )
        ]

    def list_risks(self) -> List[RiskItem]:
        return self.risks

    def add_risk(self, risk: RiskItem) -> None:
        self.risks.append(risk)


risk_register = RiskRegisterManager()
