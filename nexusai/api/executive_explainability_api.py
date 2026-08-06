"""
Explainable Executive Intelligence REST API Routers for NexusAI OS (v0.3.3).
Provides endpoints for Decision Explainability, Digital Twins, What-If Simulations, Timelines, Risk Register, ADRs, and Quality Gates.
"""
from typing import Any, Dict, List, Optional
from fastapi import APIRouter, HTTPException, Query, Body
from pydantic import BaseModel, Field

from nexusai.services.executive_explainability import executive_explainability
from nexusai.services.digital_twin import digital_twin_engine
from nexusai.services.scenario_simulation import what_if_simulation_engine
from nexusai.services.executive_timeline import executive_timeline_engine
from nexusai.services.risk_register import risk_register, RiskItem
from nexusai.services.adr_generator import adr_generator
from nexusai.services.quality_gates import quality_gates_service

explainability_router = APIRouter(prefix="/executive", tags=["Explainable Executive Intelligence"])


class ExplainRequest(BaseModel):
    decision: str
    goal_prompt: str


class GoalPromptRequest(BaseModel):
    goal_prompt: str
    project_name: str = "TwinProject"


@explainability_router.post("/explain")
async def get_explainable_recommendation(payload: ExplainRequest):
    """Generates evidence-backed explainable recommendation details for a decision."""
    rec = await executive_explainability.create_explainable_recommendation(payload.decision, payload.goal_prompt)
    return rec.model_dump()


@explainability_router.post("/digital-twin")
async def generate_project_digital_twin(payload: GoalPromptRequest):
    """Generates virtual Project Digital Twin graph."""
    twin = await digital_twin_engine.generate_digital_twin(payload.goal_prompt, payload.project_name)
    return twin.model_dump()


@explainability_router.post("/what-if")
async def run_what_if_simulation(payload: GoalPromptRequest):
    """Executes 4-scenario What-If simulation matrix (Base vs Extra Agent vs Alt LLM vs Alt Toolchain)."""
    report = await what_if_simulation_engine.run_what_if_analysis(payload.goal_prompt)
    return report.model_dump()


@explainability_router.get("/timeline")
async def get_executive_timeline(goal_prompt: str = Query("Build microservice")):
    """Generates executive timeline across 8 phases highlighting critical path nodes."""
    report = await executive_timeline_engine.generate_timeline(goal_prompt)
    return report.model_dump()


@explainability_router.get("/risk-register")
async def get_live_risk_register():
    """Lists live Risk Register items with Probability, Impact, Severity, Mitigation, and Status."""
    risks = risk_register.list_risks()
    return {"count": len(risks), "risk_register": [r.model_dump() for r in risks]}


@explainability_router.get("/adrs")
async def get_architecture_decision_records():
    """Lists generated Architecture Decision Records (ADRs)."""
    adrs = adr_generator.list_adrs()
    return {"count": len(adrs), "adrs": [a.model_dump() for a in adrs]}


@explainability_router.post("/quality-gates")
async def verify_pre_execution_quality_gates():
    """Verifies pre-flight quality gates (Architecture, Security, Dependencies, Memory, Tools, LLM, Knowledge Graph)."""
    report = await quality_gates_service.verify_pre_execution_gates()
    return report.model_dump()
