# NexusAI OS — Enterprise Autonomous AI Operating System (v0.4.0)

[![Python 3.11+](https://img.shields.io/badge/python-3.11+-blue.svg)](https://www.python.org/downloads/)
[![FastAPI](https://img.shields.io/badge/FastAPI-0.110+-green.svg)](https://fastapi.tiangolo.com/)
[![React 18](https://img.shields.io/badge/React-18-cyan.svg)](https://reactjs.org/)
[![License: MIT](https://img.shields.io/badge/License-MIT-yellow.svg)](https://opensource.org/licenses/MIT)
[![Build Status](https://img.shields.io/badge/tests-40%20passed-success.svg)](#testing)

**NexusAI OS** is an open-source **Enterprise Autonomous AI Operating System** designed to manage software engineering operations end-to-end. It coordinates an autonomous multi-agent workforce (13 personas), adaptive MCP tool intelligence, multi-layer memory engines, explainable executive decision-making, and pre-execution digital twin simulations.

---

## 🌟 Key Capabilities (v0.4.0 Release)

- **13 Autonomous Agent Personas**: CEO, PM, Architect, Backend, Frontend, DB, QA, Security, DevOps, Documentation, Marketing, Reflection, and Reviewer.
- **Dynamic AI Organization**: Ephemeral specialist spawner (`OAuth Specialist`, `Docker Specialist`, `React Specialist`, `Kubernetes Specialist`), CPU/Memory resource manager, and skill profile tracking.
- **Explainable Executive Intelligence**: CTO & Engineering Director decision explainability, Project Health Scoring (0-100), Engineering KPIs, 4-scenario What-If simulations, live Risk Register, automatic ADR generation, and pre-flight Quality Gates.
- **Adaptive MCP Ecosystem**: Dynamic discovery, vector tool embeddings, tool self-healing failover, and multi-tool execution planner (Single, Parallel, Sequential, Conditional).
- **Multi-Layer Memory Engine**: Provider-agnostic engine supporting Redis (short-term TTL), PostgreSQL (working memory), and Qdrant (long-term vector memory) with versioning and importance scoring.
- **Real-Time WebSockets Telemetry**: Live stream of agent execution logs, tool telemetry, workflow progress, and metric updates to the React OS Dashboard.
- **Built-In Demo Workflows**: 5 pre-configured demonstration workflows (Inventory System, Blog API, CRM Backend, Auth Microservice, REST API).
- **Production Container Stack**: Complete `docker-compose.yml` environment with FastAPI, PostgreSQL, Redis, Qdrant, Prometheus, and Grafana.

---

## 🚀 Quick Start

### 1. Local Python Setup
```bash
# Clone Repository
git clone https://github.com/Amay54/NexusAI-OS.git
cd nexusai-os

# Create Virtual Environment
python -m venv .venv
source .venv/bin/activate  # On Windows: .venv\Scripts\activate

# Install Dependencies
pip install -r requirements.txt

# Run Tests
pytest tests/ -v
```

### 2. Start FastAPI Control Plane
```bash
uvicorn nexusai.main:app --reload --port 8000
```
- Open Interactive OpenAPI Docs: `http://localhost:8000/docs`
- Access Health Status: `http://localhost:8000/health`

### 3. Docker Compose Production Deployment
```bash
docker-compose up -d --build
```

---

## 📊 Performance & Test Metrics

- **Unit, Integration, & Benchmark Tests**: `40 passed in 10.45s` (100% Pass Rate).
- **Context Retrieval Latency**: `< 15.0 ms`
- **Vector Search Latency**: `< 22.0 ms`
- **Knowledge Graph Query Latency**: `< 12.0 ms`
- **Cache Hit Ratio**: `> 95.0%`

---

## 📜 License
MIT License. Free and Open-Source software.
