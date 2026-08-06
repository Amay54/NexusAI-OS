# Changelog - NexusAI OS

All notable changes to the NexusAI OS platform will be documented in this file.

The format is based on [Keep a Changelog](https://keepachangelog.com/en/1.0.0/),
and this project adheres to [Semantic Versioning](https://semver.org/spec/v2.0.0.html).

## [v0.2.2] - Adaptive MCP Ecosystem & Dynamic Tool Intelligence - 2026-08-06

### Added
- **Dynamic Tool Knowledge Base (`nexusai/mcp/registry.py`)**: `ToolMetadata` storing tool IDs, descriptions, parameters, permissions, risk levels, vector embeddings, and real-time reliability scores.
- **Adaptive Tool Discovery Engine (`nexusai/mcp/engine.py`)**: Automatically scans MCP servers and plugin manifests, generates embeddings via `embedding_service`, and registers capabilities into ToolRegistry without manual code edits.
- **Tool Reasoning Engine (`nexusai/mcp/reasoning.py`)**: Evaluates agent prompts against Tool KB using semantic vector matching, agent support checks, and reliability scores.
- **Tool Learning & Self-Healing Engine (`nexusai/mcp/learning.py`)**: Tracks invocation latency and success/failure rates, dynamically updates reliability scores, and executes automated retries and provider failovers.
- **Multi-Tool Planning Engine (`nexusai/mcp/planner.py`)**: Orchestrates Single, Parallel (`asyncio.gather`), Sequential, Conditional, and Fallback tool execution plans.
- **Dynamic Plugin Marketplace Loader (`nexusai/mcp/plugins.py`)**: Automatically discovers plugins dropped into `plugins/` folder.
- **Adaptive MCP REST APIs (`nexusai/api/mcp_api.py`)**: Endpoints for tool listing, details, discovery, catalog, task evaluation, metrics, and multi-tool plan execution.
- **Adaptive MCP Test Suite (`tests/test_mcp_adaptive.py`)**: 5 new automated tests with 100% pass rate.
- **Tool Catalog Documentation (`docs/mcp/tool_catalog.md`)**: Automatically generated catalog and capability matrix.

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
