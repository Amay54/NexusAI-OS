# Changelog - NexusAI OS

All notable changes to the NexusAI OS platform will be documented in this file.

The format is based on [Keep a Changelog](https://keepachangelog.com/en/1.0.0/),
and this project adheres to [Semantic Versioning](https://semver.org/spec/v2.0.0.html).

## [v0.2.1] - Enterprise Intelligence Architecture Upgrade - 2026-08-06

### Added
- **Memory Versioning (`nexusai/memory/base.py`)**: `MemoryItem` version sequence tracking (`version`, `created_at`, `updated_at`, `source_agent`, `workflow_id`, `confidence_score`, `embedding_provider`, `tags`).
- **Memory Importance Scoring (`nexusai/memory/base.py`)**: `ImportanceLevel` enum (`CRITICAL`, `HIGH`, `MEDIUM`, `LOW`) and importance score weighting (`0.0` to `1.0`).
- **Context Budget Manager (`nexusai/memory/context_budget.py`)**: Intelligent ranking formula $(0.4 \times \text{relevance}) + (0.3 \times \text{importance}) + (0.3 \times \text{recency})$, de-duplication, memory merging, and token budget packing.
- **Vector Embedding Abstraction (`nexusai/memory/embeddings.py`)**: `BaseEmbeddingProvider` interface supporting Gemini Embeddings, SentenceTransformers, Ollama Embeddings, and Mock Embeddings via configuration.
- **Knowledge Graph Metadata (`nexusai/services/knowledge_graph.py`)**: Metadata on nodes (`node_type`, `created_at`, `owner`, `confidence`, `tags`) and relationships (`created_by`, `workflow_id`, `confidence`, `timestamp`).
- **Memory Retrieval Explainability (`nexusai/memory/explainability.py`)**: Logged selection rationale (`similarity_score`, `importance_score`, `recency_score`, `relationship_score`) exposed via `GET /api/v1/memory/explain`.
- **Workflow Snapshots & Rollback (`nexusai/services/snapshots.py`)**: Periodic state snapshotting (`WorkflowSnapshot`), snapshot diff comparison (`compare_snapshots`), and snapshot rollbacks (`POST /api/v1/snapshots/{id}/rollback`).
- **Observability Metrics (`nexusai/core/observability.py`)**: Metrics collector measuring retrieval latency, cache hit ratio, vector search latency, compression time, and graph query latency (`GET /api/v1/observability/metrics`).
- **Benchmark Suite & Report (`tests/test_benchmarks.py`)**: Benchmark test suite generating markdown performance report at `docs/benchmarks/benchmark_report.md`.

## [v0.2.0] - Phase 2 Intelligence & Persistence Layer - 2026-08-06

### Added
- Multi-Layer Memory Engine (Redis Short-Term, PostgreSQL Working, Qdrant Long-Term Vector).
- Context Retrieval & Compression Engine.
- Provider-Agnostic Knowledge Graph Engine.
- Self-Reflection Engine.
- Agent State Persistence & History Tracker.
- Phase 2 REST Routers (`/memory`, `/graph`, `/reflection`, `/workflows`).

## [v0.1.0] - Phase 1 Core Architecture - 2026-08-06

### Added
- Initialized `nexusai-os` repository structure.
- Asynchronous Event Bus with Pub/Sub, correlation IDs, DLQ, and event replay.
- Task-based Intelligent Router supporting free LLMs (Gemini 2.5 Flash, DeepSeek, Qwen, Ollama).
- Isolated Code Sandbox Engine.
- Security JWT & bcrypt hashing modules.
