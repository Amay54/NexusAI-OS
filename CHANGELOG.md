# Changelog - NexusAI OS

All notable changes to the NexusAI OS platform will be documented in this file.

The format is based on [Keep a Changelog](https://keepachangelog.com/en/1.0.0/),
and this project adheres to [Semantic Versioning](https://semver.org/spec/v2.0.0.html).

## [v0.7.0] - AI-Powered Multi-Framework Code Synthesizer Release - 2026-08-06

### Fixed
- **Single-Template Bug Fix (`nexusai/services/project_synthesizer.py`)**: Fixed critical issue where synthesizer returned a fixed FastAPI template regardless of prompt parameters.

### Added
- **Multi-Framework AI Code Synthesizer (`nexusai/services/project_synthesizer.py`)**: Parses goal prompt to detect requested framework (`Flask`, `React`, `Django`, `FastAPI`, `Express`), database (`SQLite`, `PostgreSQL`, `MongoDB`, `MySQL`), domain (`Weather`, `Todo`, `CRM`, `Blog`), and language (`Python`, `JavaScript`).
- **Framework-Matching Quality Gate (`nexusai/services/project_synthesizer.py`)**: Asserts that synthesized project files match requested framework rules, raising `ValueError` if a mismatch is detected.
- **Multi-Framework Synthesis Test Suite (`tests/test_multi_framework_synthesis.py`)**: 5 new test cases verifying Flask Weather API + SQLite, React Todo App + Vite, FastAPI CRM Backend + PostgreSQL, and Django Blog synthesis.

## [v0.6.0] - 100% Dynamic Backend-Driven Frontend & Artifact Service Release - 2026-08-06

### Added
- **100% Backend-Driven React OS Dashboard (`frontend/src/App.tsx`)**: Completely eliminated all static demonstration arrays and code snippets. File explorer trees and file contents are dynamically fetched from the backend API.
- **Workflow & Artifact Store Service (`nexusai/services/workflow_store.py`)**: Stores dynamically synthesized project artifacts and summaries keyed by unique `workflow_id`.
- **Dynamic Workflow Execution REST APIs (`nexusai/api/workflow_execution_api.py`)**:
  - `POST /api/v1/workflow/create`: Starts workflow for prompt, returns `workflow_id`.
  - `GET /api/v1/workflow/{id}`: Returns workflow status and active agent states.
  - `GET /api/v1/workflow/{id}/files`: Returns dynamic file list tree.
  - `GET /api/v1/workflow/{id}/file/{path:path}`: Returns exact raw content of requested file path on-demand.
  - `GET /api/v1/workflow/{id}/summary`: Returns real execution summary metrics.
  - `GET /api/v1/workflow/{id}/artifacts`: Returns documentation & Docker artifacts.
  - `GET /api/v1/workflow/{id}/download`: Serves ZIP archive of the specific workflow files.

## [v0.5.1] - Results Workspace & Project File Explorer Release - 2026-08-06

### Added
- **Generated Project Results Workspace (`frontend/src/App.tsx`)**: Auto-switches to the `Generated Project` tab upon workflow completion, providing a VS Code / Cursor-style file explorer and code viewer.
- **Project Download ZIP REST API (`nexusai/api/project_download_api.py`)**: `GET /api/v1/projects/download/{project_id}` streaming an in-memory `.zip` archive containing synthesized Python code, Docker files, and docs.

## [v0.5.0] - Official Public Release - 2026-08-06

### Added
- Production Audit & Security Policy, Open Source Governance Suite (MIT License, CODE_OF_CONDUCT, CONTRIBUTING), CI/CD pipeline, and demonstration guide.

## [v0.4.0] - Master Production Release - 2026-08-06

### Added
- Real multi-file codebase synthesizer, 5 built-in demo workflows, real-time WebSockets telemetry bus (`/ws/telemetry`), React 18 OS Dashboard template, Docker Compose stack, and comprehensive documentation suite.

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
