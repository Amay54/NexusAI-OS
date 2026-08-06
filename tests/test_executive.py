"""
Executive Intelligence & Simulation Test Suite (NexusAI OS v0.3.2).
Verifies Executive Analysis, Project Health Metrics, Engineering KPIs, Pre-Execution Simulation, and Dashboard REST APIs.
"""
import pytest
from httpx import ASGITransport, AsyncClient

from nexusai.services.executive_intelligence import executive_intelligence
from nexusai.services.project_health import project_health_service
from nexusai.core.kpis import kpi_tracker
from nexusai.services.simulation import pre_execution_simulator
from nexusai.main import app


@pytest.mark.asyncio
async def test_executive_strategic_analysis():
    """Test executive analysis calculations for simple vs enterprise prompts."""
    report_ent = await executive_intelligence.analyze_project_strategy("Build enterprise microservices SaaS")
    assert report_ent.business_impact == "CRITICAL"
    assert report_ent.technical_risk_score > 0
    assert report_ent.estimated_roi_multiplier > 1.0

    report_sim = await executive_intelligence.analyze_project_strategy("Build simple CLI script")
    assert report_sim.business_impact == "LOW"
    assert report_sim.estimated_duration_sec < report_ent.estimated_duration_sec


@pytest.mark.asyncio
async def test_project_health_metrics_and_kpis():
    """Test Project Health Scoring and Engineering KPI trackers."""
    health = await project_health_service.compute_health_metrics()
    assert health.project_health_score >= 90.0
    assert health.delivery_confidence > 0.8
    assert health.bug_risk < 0.2

    kpis = kpi_tracker.get_kpi_summary()
    assert kpis.agent_productivity_score > 90.0
    assert kpis.workflow_success_rate_percent > 90.0


@pytest.mark.asyncio
async def test_pre_execution_simulation_engine():
    """Test pre-execution simulation prediction results."""
    sim = await pre_execution_simulator.simulate_workflow_execution("Build a FastAPI microservice with Docker and PostgreSQL")
    assert sim.simulation_passed is True
    assert sim.expected_success_probability >= 0.80
    assert len(sim.predicted_failures) > 0
    assert sim.predicted_cpu_load_percent > 0.0


@pytest.mark.asyncio
async def test_executive_dashboard_rest_apis():
    """Test FastAPI endpoints for executive analysis, simulation, health, and dashboard."""
    async with AsyncClient(transport=ASGITransport(app=app), base_url="http://test") as client:
        # 1. Analyze
        an_res = await client.post("/api/v1/executive/analyze", json={"goal_prompt": "Build microservice platform"})
        assert an_res.status_code == 200
        assert "business_impact" in an_res.json()

        # 2. Simulate
        sim_res = await client.post("/api/v1/executive/simulate", json={"goal_prompt": "Build microservice platform"})
        assert sim_res.status_code == 200
        assert sim_res.json()["simulation_passed"] is True

        # 3. Health
        h_res = await client.get("/api/v1/executive/health")
        assert h_res.status_code == 200
        assert "project_health_score" in h_res.json()

        # 4. Dashboard
        dash_res = await client.get("/api/v1/executive/dashboard")
        assert dash_res.status_code == 200
        assert "company_overview" in dash_res.json()
        assert "risk_heatmap" in dash_res.json()
