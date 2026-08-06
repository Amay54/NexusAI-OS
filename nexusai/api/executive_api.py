"""
Executive Intelligence REST API Routers for NexusAI OS (v0.3.3).
Provides endpoints for Strategic Analysis, Pre-Execution Simulation, Executive Dashboard, and Project Health Metrics.
"""
from typing import Any, Dict, List, Optional
from fastapi import APIRouter, HTTPException, Query, Body
from pydantic import BaseModel, Field

from nexusai.services.executive_intelligence import executive_intelligence
from nexusai.services.project_health import project_health_service
from nexusai.core.kpis import kpi_tracker
from nexusai.services.simulation import pre_execution_simulator

executive_router = APIRouter(prefix="/executive", tags=["Executive Intelligence Layer"])


class StrategicAnalysisRequest(BaseModel):
    goal_prompt: str
    project_name: str = "StrategyProject"


@executive_router.post("/analyze")
async def analyze_project_strategy(payload: StrategicAnalysisRequest):
    """Performs executive strategic analysis (Business Impact, Technical Risk, ROI, Cost)."""
    report = await executive_intelligence.analyze_project_strategy(payload.goal_prompt, payload.project_name)
    return report.model_dump()


@executive_router.post("/simulate")
async def run_pre_execution_simulation(payload: StrategicAnalysisRequest):
    """Simulates workflow execution before code runs to predict failures, duration, and success probability."""
    res = await pre_execution_simulator.simulate_workflow_execution(payload.goal_prompt, payload.project_name)
    return res.model_dump()


@executive_router.get("/health")
async def get_project_health():
    """Returns real-time project health scores, delivery confidence, bug risk, and security risk metrics."""
    health = await project_health_service.compute_health_metrics()
    return health.model_dump()


@executive_router.get("/dashboard")
async def get_executive_dashboard():
    """Returns comprehensive Executive Dashboard metrics including KPIs, Health, and Risk Heatmap."""
    health = await project_health_service.compute_health_metrics()
    kpis = kpi_tracker.get_kpi_summary()

    return {
        "company_overview": {
            "status": "OPERATIONAL",
            "active_projects": 4,
            "total_agents_online": 13,
            "overall_health_score": health.project_health_score
        },
        "health_metrics": health.model_dump(),
        "engineering_kpis": kpis.model_dump(),
        "risk_heatmap": [
            {"category": "Container Port Conflicts", "risk_level": "LOW", "probability": 0.05},
            {"category": "Database Lock Contention", "risk_level": "MEDIUM", "probability": 0.12},
            {"category": "API Rate Limits", "risk_level": "LOW", "probability": 0.02}
        ]
    }
