# Changelog - NexusAI OS

All notable changes to the NexusAI OS platform will be documented in this file.

The format is based on [Keep a Changelog](https://keepachangelog.com/en/1.0.0/),
and this project adheres to [Semantic Versioning](https://semver.org/spec/v2.0.0.html).

## [v0.3.3] - Explainable Executive Intelligence & Digital Twin Release - 2026-08-06

### Added
- **Executive Decision Explainability (`nexusai/services/executive_explainability.py`)**: `ExplainableRecommendation` model requiring confidence scores, supporting evidence, assumptions, reasoning summaries, data sources used, and alternative options considered for every recommendation.
- **Prediction Engine Metric Classifier (`nexusai/services/prediction_classifier.py`)**: Classifies all metrics into `OBSERVED`, `ESTIMATED`, `MODEL_PREDICTION`, `USER_ASSUMPTION`, and `UNKNOWN` to avoid presenting estimates as facts.
- **Project Digital Twin Engine (`nexusai/services/digital_twin.py`)**: Virtual graph representation (`ProjectDigitalTwin`) storing Project Structure, Tasks, Dependencies, Agent Assignments, Tools, Timelines, and Risk Graph.
- **What-If Scenario Simulation Engine (`nexusai/services/scenario_simulation.py`)**: Executes 4-scenario simulation matrix (Base Team vs Extra Specialist vs Alt LLM vs Alt Toolchain) to evaluate trade-offs in duration, risk, and success probability.
- **Executive Timeline & Critical Path Generator (`nexusai/services/executive_timeline.py`)**: Generates Gantt-style executive timeline across 8 phases, highlighting critical path nodes and bottleneck risks.
- **Live Risk Register (`nexusai/services/risk_register.py`)**: Continuous Risk Register (`RiskItem`) tracking Probability, Impact, Severity, Mitigation Strategy, Owner, and Status.
- **Automatic ADR Generator (`nexusai/services/adr_generator.py`)**: Automatically generates markdown Architecture Decision Records (ADRs) storing Context, Decision, Alternatives, Consequences, and Reasoning.
- **Pre-Execution Quality Gates (`nexusai/services/quality_gates.py`)**: Pre-flight verification checking Architecture, Security, Dependencies, Memory, Tools, LLM, and Knowledge Graph health before execution begins.
- **Explainability REST APIs (`nexusai/api/executive_explainability_api.py`)**: Endpoints for Explainability, Digital Twins, What-If Simulations, Timelines, Risk Register, ADRs, and Quality Gates (`/api/v1/executive/*`).
- **Explainability Test Suite (`tests/test_executive_explainability.py`)**: 4 new automated integration tests with 100% pass rate.

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
