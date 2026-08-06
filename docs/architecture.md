# NexusAI OS Architecture Documentation

## 1. System Overview
NexusAI OS is an Enterprise Autonomous AI Operating System. It manages software engineering operations using an event-driven multi-agent workforce, dynamic tool intelligence (MCP), multi-layer memory engines, and executive strategic intelligence.

```
                              +---------------------------------------+
                              |      FastAPI OS Control Plane & UI    |
                              +-------------------+-------------------+
                                                  |
                                                  v Pub/Sub Event Bus
                              +-------------------+-------------------+
                              | 13 Autonomous Agent Workforce Engine  |
                              |  (CEO, PM, Architect, DB, Backend,    |
                              |   Frontend, QA, Sec, DevOps, Doc, etc)|
                              +---------+-------------------+---------+
                                        |                   |
                                        v                   v
            +---------------------------+----+   +----------+--------------------+
            | Multi-Layer Memory Engine      |   | Adaptive MCP & Sandbox Engine     |
            | Redis (short), Postgres (work),|   | Filesystem, Terminal, Docker, DB,  |
            | Qdrant (long-term vectors)     |---| Code Sandbox Execution Engine     |
            +--------------------------------+   +-----------------------------------+
```

## 2. Key Subsystems
- **Asynchronous Event Bus (`nexusai/core/event_bus.py`)**: Pub/Sub event bus with correlation IDs, DLQ, and event replay.
- **Adaptive MCP Engine (`nexusai/mcp/`)**: Automatic discovery, tool reasoning, tool self-healing, and dynamic plugin marketplace.
- **Autonomous Workforce (`nexusai/agents/`, `nexusai/workflows/`)**: 13 specialized agent personas, LangGraph orchestrator, consensus voting, HITL checkpoints, and dynamic org planner.
- **Executive Intelligence Layer (`nexusai/services/executive_intelligence.py`)**: Decision explainability, project health scoring, engineering KPIs, digital twin graphs, what-if simulations, live risk registers, and quality gates.
