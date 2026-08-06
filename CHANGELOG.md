# Changelog - NexusAI OS

All notable changes to the NexusAI OS platform will be documented in this file.

The format is based on [Keep a Changelog](https://keepachangelog.com/en/1.0.0/),
and this project adheres to [Semantic Versioning](https://semver.org/spec/v2.0.0.html).

## [v0.2.0] - Phase 2 Intelligence & Persistence Layer - 2026-08-06

### Added
- **Multi-Layer Memory Engine (`nexusai/memory/`)**:
  - Provider-agnostic abstract interfaces for Short-Term, Working, and Long-Term Vector Memory.
  - Ephemeral Redis cache provider (`RedisShortTermMemory`) with TTL support.
  - Qdrant Vector memory provider (`QdrantLongTermMemory`) with token intersection search.
  - Unified Memory Manager (`MemoryManager`).
- **Context Retrieval & Compression Engine (`nexusai/memory/retrieval.py`)**:
  - Asynchronously aggregates conversation context, short-term state, long-term vector lessons, and knowledge graph relationships.
  - Implements character & token budget compression to prevent context overflow.
- **Provider-Agnostic Knowledge Graph Service (`nexusai/services/knowledge_graph.py`)**:
  - Abstract `BaseKnowledgeGraphProvider` allowing swapping graph backends (InMemory, Neo4j, NetworkX) cleanly.
  - Topological entity & relationship queries (`Projects` -> `Tasks` -> `Files` -> `APIs` -> `Deployments`).
- **Self-Reflection Engine (`nexusai/services/reflection.py`)**:
  - Post-workflow retrospective generator analyzing successes, failures, bottlenecks, slow agents, failed tools, and optimization suggestions.
  - Indexes lessons into long-term vector memory for searchable retrieval.
- **State Persistence & History Tracker (`nexusai/services/state_persistence.py`)**:
  - Checkpoints agent execution state to support restoring interrupted workflows.
  - Records detailed LLM metrics (latency ms, provider used) and tool invocations.
- **FastAPI Intelligence REST Routers (`nexusai/api/intelligence.py`)**:
  - `GET /api/v1/memory` & `GET /api/v1/memory/search`
  - `GET /api/v1/graph` & `GET /api/v1/graph/node/{id}`
  - `GET /api/v1/reflection` & `GET /api/v1/reflection/search`
  - `GET /api/v1/workflows/{id}/history` & `GET /api/v1/workflows/{id}/checkpoint`
- **Phase 2 Test Suite (`tests/test_phase2.py`)**:
  - Unit, integration, concurrency, state recovery, and REST API tests with 100% pass rate.

## [v0.1.0] - Phase 1 Core Architecture - 2026-08-06

### Added
- Repository initialization for `nexusai-os` platform.
- Core configuration manager (`nexusai/core/config.py`) using Pydantic v2 BaseSettings.
- Asynchronous Event Bus (`nexusai/core/event_bus.py`) with Pub/Sub, correlation trace IDs, Dead Letter Queue (DLQ), and event replay.
- Multi-LLM Provider Engine (`nexusai/core/llm_router.py`) supporting Gemini 2.5 Flash Free Tier, DeepSeek, Qwen 3, and local Ollama.
- Task-based Intelligent Router (`nexusai/core/intelligent_router.py`) with latency tracking and provider quality scoring.
- Isolated Code Execution Sandbox Engine (`nexusai/core/sandbox.py`) for Python, Node.js, and Shell scripts with timeout enforcement.
- Security utilities (`nexusai/core/security.py`) for direct bcrypt hashing and JWT token management.
