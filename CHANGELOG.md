# Changelog - NexusAI OS

All notable changes to the NexusAI OS platform will be documented in this file.

The format is based on [Keep a Changelog](https://keepachangelog.com/en/1.0.0/),
and this project adheres to [Semantic Versioning](https://semver.org/spec/v2.0.0.html).

## [v0.4.0] - Master Production Release - 2026-08-06

### Added
- **Production End-to-End Project Synthesizer (`nexusai/services/project_synthesizer.py`)**: Complete real multi-file codebase synthesizer (FastAPI, PostgreSQL schema, Pytest test suits, Dockerfile, docker-compose.yml, README, ADRs) verified inside execution sandbox.
- **Built-In Demo Workflows Engine (`nexusai/services/demo_workflows.py`)**: 5 pre-configured demonstration workflows (Inventory System, Blog API, CRM Backend, Auth Microservice, REST API).
- **Real-Time WebSocket Telemetry Bus (`nexusai/api/websocket_api.py`)**: `/ws/telemetry` endpoint streaming real-time agent execution logs, workflow progress, tool invocations, and artifact events to the dashboard.
- **Production React 18 OS Dashboard (`frontend/`)**: Modern UI featuring Executive Dashboard, Organization Board, Live Timeline, Tool Activity Feed, Memory & Knowledge Graph Visualizer, Digital Twin Viewer, and Artifact Explorer.
- **Docker Compose Stack & Observability (`docker-compose.yml`, `prometheus.yml`)**: Production containerization stack including FastAPI, PostgreSQL, Redis, Qdrant, Prometheus, and Grafana.
- **Production Documentation Suite (`docs/`)**: Architecture guide, Deployment guide, Developer guide, API documentation, Troubleshooting, and Contribution guidelines.
- **Production Test Suite (`tests/test_v0_4_0_production.py`)**: 4 new end-to-end integration tests verifying synthesis, demo execution, WebSockets, and control plane endpoints (40/40 tests passing).

## [v0.3.3] - Explainable Executive Intelligence & Digital Twin Release - 2026-08-06

### Added
- Decision Explainability Engine, Prediction Metric Classifier, Project Digital Twin Engine, What-If Scenario Simulation, Executive Timeline, Live Risk Register, ADR Generator, and Pre-Execution Quality Gates.

## [v0.3.2] - Executive Intelligence Layer & Pre-Execution Simulation - 2026-08-06

### Added
- Executive Intelligence Engine, Project Health Scoring, Engineering KPIs, and Pre-Execution Simulation Engine.

## [v0.3.1] - Adaptive AI Organization Upgrade - 2026-08-06

### Added
- Dynamic Organization Engine, Ephemeral Specialist Agent Spawner, Agent Resource Manager, Skill Profiles Engine, Cross-Agent Collaboration Engine, Negotiation & Debate Engine, Autonomous Replanning Engine, and Company Learning Loop.

## [v0.3.0] - Autonomous Multi-Agent Workforce Release - 2026-08-06

### Added
- Defined 13 Specialized Agent Personas, LangGraph State Machine, Consensus Voting Engine, HITL Safety Checkpoints, and End-to-End Project Synthesizer.

## [v0.2.2] - Adaptive MCP Ecosystem & Dynamic Tool Intelligence - 2026-08-06

### Added
- Dynamic Tool Knowledge Base, Adaptive Tool Discovery Engine, Tool Reasoning Engine, Tool Learning & Self-Healing Engine, Multi-Tool Planner, and Plugin Marketplace Loader.

## [v0.2.1] - Enterprise Intelligence Architecture Upgrade - 2026-08-06

### Added
- Memory Versioning, Importance Scoring, Context Budget Manager, Vector Embedding Abstraction, Knowledge Graph Metadata, Explainability Engine, Workflow Snapshots, Observability Metrics, and Performance Benchmarks.

## [v0.2.0] - Phase 2 Intelligence & Persistence Layer - 2026-08-06

### Added
- Multi-Layer Memory Engine, Context Retrieval & Compression Engine, Knowledge Graph Engine, Self-Reflection Engine, and REST Routers.

## [v0.1.0] - Phase 1 Core Architecture - 2026-08-06

### Added
- Initialized `nexusai-os` repository structure.
- Asynchronous Event Bus with Pub/Sub, correlation IDs, DLQ, and event replay.
- Task-based Intelligent Router supporting free LLMs (Gemini 2.5 Flash, DeepSeek, Qwen, Ollama).
- Isolated Code Sandbox Engine.
- Security JWT & bcrypt hashing modules.
