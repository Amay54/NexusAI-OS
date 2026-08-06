# NexusAI OS Demonstration & Presentation Guide

## 1. Executive Presentation Overview
NexusAI OS represents the next paradigm shift in AI engineering—transitioning from simple chatbots and RAG apps into an **Autonomous AI Operating System** that manages software engineering end-to-end.

---

## 2. Recommended Demonstration Flow

### Step 1: Launch Production Dashboard & Telemetry
```bash
uvicorn nexusai.main:app --reload --port 8000
```
- Open `http://localhost:8000/docs` to show FastAPI OpenAPI REST endpoints.
- Open WebSockets telemetry listener at `ws://localhost:8000/ws/telemetry`.

### Step 2: Run Built-In Demo Workflows
Navigate to Built-in Demos and trigger:
```http
POST /api/v1/demo/execute/demo_inventory_system
```

### Step 3: Demonstrate Pre-Execution Simulation & Explainability
Execute:
```http
POST /api/v1/executive/simulate
{
  "goal_prompt": "Build an enterprise FastAPI microservice with PostgreSQL and Docker",
  "project_name": "EnterpriseSaaS"
}
```
Show What-If scenario simulations, live Risk Register, and automatically generated Architecture Decision Records (ADRs).

---

## 3. Recommended Screenshots & Video Recording Keyframes
1. **Executive Dashboard & Risk Heatmap**: Displays real-time Project Health Score (95.0), Delivery Confidence (92%), and Risk Heatmap.
2. **Organization Status Board**: Shows active 13 agent personas (`CEO`, `Architect`, `Backend`, `DevOps`) and dynamic specialist spawning.
3. **Artifact Explorer**: Displays synthesized Python code (`main.py`), test cases (`test_main.py`), `Dockerfile`, `docker-compose.yml`, and `README.md`.
