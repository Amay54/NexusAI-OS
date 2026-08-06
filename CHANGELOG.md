# Changelog - NexusAI OS

All notable changes to the NexusAI OS platform will be documented in this file.

The format is based on [Keep a Changelog](https://keepachangelog.com/en/1.0.0/),
and this project adheres to [Semantic Versioning](https://semver.org/spec/v2.0.0.html).

## [v1.0.0-phase1] - 2026-08-06

### Added
- Repository initialization for `nexusai-os` platform.
- Core configuration manager (`nexusai/core/config.py`) using Pydantic v2 BaseSettings.
- Asynchronous Event Bus (`nexusai/core/event_bus.py`) with Pub/Sub, correlation trace IDs, Dead Letter Queue (DLQ), and event replay.
- Multi-LLM Provider Engine (`nexusai/core/llm_router.py`) supporting Gemini 2.5 Flash Free Tier, DeepSeek, Qwen 3, and local Ollama.
- Task-based Intelligent Router (`nexusai/core/intelligent_router.py`) with latency tracking and provider quality scoring.
- Isolated Code Execution Sandbox Engine (`nexusai/core/sandbox.py`) for Python, Node.js, and Shell scripts with timeout enforcement.
- Security utilities (`nexusai/core/security.py`) for direct bcrypt hashing and JWT token management.
- Unit test suite (`tests/test_phase1.py`) with 100% pass rate across core systems.
