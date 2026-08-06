"""
Explainable Executive Intelligence Test Suite (NexusAI OS v0.3.3).
Verifies Executive Decision Explainability, Metric Classification, Project Digital Twins, What-If Simulations, Timelines, Risk Register, ADRs, Quality Gates, and REST APIs.
"""
import pytest
from httpx import ASGITransport, AsyncClient

from nexusai.services.executive_explainability import executive_explainability
from nexusai.services.prediction_classifier import metric_classifier, MetricCategory
from nexusai.services.digital_twin import digital_twin_engine
from nexusai.services.scenario_simulation import what_if_simulation_engine
from nexusai.services.executive_timeline import executive_timeline_engine
from nexusai.services.risk_register import risk_register
from nexusai.services.adr_generator import adr_generator
from nexusai.services.quality_gates import quality_gates_service
from nexusai.main import app


@pytest.mark.asyncio
async def test_executive_decision_explainability_and_classifier():
    """Test explainable recommendations and metric categorization."""
    rec = await executive_explainability.create_explainable_recommendation("Adopt Microservice Architecture", "Build enterprise SaaS")
    assert rec.decision == "Adopt Microservice Architecture"
    assert len(rec.supporting_evidence) > 0
    assert len(rec.assumptions) > 0
    assert len(rec.alternative_options_considered) > 0

    metric = metric_classifier.classify("CPU Usage", 35.0, MetricCategory.OBSERVED, "Empirical reading")
    assert metric.category == MetricCategory.OBSERVED


@pytest.mark.asyncio
async def test_digital_twin_and_what_if_simulations():
    """Test Project Digital Twin graph generation and 4-scenario What-If simulation."""
    twin = await digital_twin_engine.generate_digital_twin("Build FastAPI Microservice")
    assert twin.project_name == "TwinProject"
    assert len(twin.virtual_tasks) > 0
    assert len(twin.risk_graph_edges) > 0

    what_if = await what_if_simulation_engine.run_what_if_analysis("Build FastAPI Microservice")
    assert len(what_if.scenarios) == 4
    assert what_if.recommended_scenario_id == "scenario_b_extra_specialist"


@pytest.mark.asyncio
async def test_timeline_risk_register_adrs_and_quality_gates():
    """Test executive timeline, risk register, ADR generation, and quality gates."""
    timeline = await executive_timeline_engine.generate_timeline("Build Microservice")
    assert timeline.total_estimated_sec > 0
    assert len(timeline.critical_path_nodes) > 0

    risks = risk_register.list_risks()
    assert len(risks) >= 2

    adr = await adr_generator.generate_adr("Use PostgreSQL", "Storage requirement", "Use PostgreSQL", ["MySQL"], ["Schema stability"], "Best ACID support")
    assert adr.adr_id.startswith("ADR-")

    q_report = await quality_gates_service.verify_pre_execution_gates()
    assert q_report.all_gates_passed is True
    assert len(q_report.checks) == 7


@pytest.mark.asyncio
async def test_explainability_rest_apis():
    """Test FastAPI REST endpoints for explainability, digital twin, what-if, timeline, risks, adrs, quality gates."""
    async with AsyncClient(transport=ASGITransport(app=app), base_url="http://test") as client:
        # 1. Explain
        exp_res = await client.post("/api/v1/executive/explain", json={"decision": "Adopt Microservices", "goal_prompt": "Build SaaS"})
        assert exp_res.status_code == 200
        assert "supporting_evidence" in exp_res.json()

        # 2. Digital Twin
        twin_res = await client.post("/api/v1/executive/digital-twin", json={"goal_prompt": "Build SaaS"})
        assert twin_res.status_code == 200
        assert "virtual_tasks" in twin_res.json()

        # 3. What-If
        wif_res = await client.post("/api/v1/executive/what-if", json={"goal_prompt": "Build SaaS"})
        assert wif_res.status_code == 200
        assert len(wif_res.json()["scenarios"]) == 4

        # 4. Timeline
        time_res = await client.get("/api/v1/executive/timeline")
        assert time_res.status_code == 200
        assert "critical_path_nodes" in time_res.json()

        # 5. Quality Gates
        q_res = await client.post("/api/v1/executive/quality-gates")
        assert q_res.status_code == 200
        assert q_res.json()["all_gates_passed"] is True
