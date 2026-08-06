# Changelog - NexusAI OS

All notable changes to the NexusAI OS platform will be documented in this file.

The format is based on [Keep a Changelog](https://keepachangelog.com/en/1.0.0/),
and this project adheres to [Semantic Versioning](https://semver.org/spec/v2.0.0.html).

## [v0.3.1] - Adaptive AI Organization Upgrade - 2026-08-06

### Added
- **Dynamic Organization Engine (`nexusai/workflows/dynamic_org.py`)**: CEO Agent dynamically determines required agents, parallel execution branches, skipped unnecessary roles, and required specialists based on goal complexity (Simple TODO vs Enterprise SaaS).
- **Ephemeral Specialist Agent Spawner (`nexusai/agents/spawner.py`)**: Dynamically spawns temporary specialist personas (`OAuth Specialist`, `Docker Specialist`, `React Specialist`, `PostgreSQL Specialist`, `Kubernetes Specialist`) and auto-terminates them upon task completion.
- **Agent Resource Manager (`nexusai/agents/resource_manager.py`)**: Tracks CPU/Memory utilization, task queue size, workload, and Busy/Idle states to optimize task assignment.
- **Agent Skill Profiles & Metrics (`nexusai/agents/skill_profiles.py`)**: Tracks domain experience, success rates, average execution times, preferred tools/LLMs, failure histories, and confidence scores.
- **Cross-Agent Collaboration Engine (`nexusai/agents/collaboration.py`)**: Facilitates peer reviews, pair programming, mentor agent consultations, and help requests.
- **Negotiation & Debate Engine (`nexusai/services/negotiation.py`)**: Coordinates multi-agent debates, confidence-weighted voting, conflict resolution, and automatic HITL escalation.
- **Autonomous Replanning Engine (`nexusai/workflows/replanning.py`)**: Catches agent failures, spawns specialist recovery agents, switches tools/LLMs, and retries workflows dynamically.
- **Company Learning Loop (`nexusai/services/company_learning.py`)**: Updates tool/agent rankings, planning quality estimates, and failure prediction metrics after every workflow run.
- **Adaptive Org REST APIs (`nexusai/api/dynamic_org_api.py`)**: Endpoints for dynamic org planning, resource metrics, skill profiles, specialist spawning, agent debates, and failure replanning (`/api/v1/org/*`).
- **Dynamic Org Test Suite (`tests/test_dynamic_org.py`)**: 5 new automated integration tests with 100% pass rate.

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
