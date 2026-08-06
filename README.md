# NexusAI OS - Enterprise Autonomous AI Operating System

[![NexusAI OS CI/CD](https://github.com/nexusai-os/nexusai-os/actions/workflows/ci.yml/badge.svg)](https://github.com/nexusai-os/nexusai-os/actions)
[![License: MIT](https://img.shields.io/badge/License-MIT-yellow.svg)](https://opensource.org/licenses/MIT)
[![Python 3.11+](https://img.shields.io/badge/python-3.11+-blue.svg)](https://www.python.org/)
[![FastAPI](https://img.shields.io/badge/FastAPI-0.110+-009688.svg)](https://fastapi.tiangolo.com/)

**NexusAI OS** is an open-source **Enterprise Autonomous AI Operating System**. It acts as a collaborative team of 10 specialized AI employee personas capable of planning, coordinating, developing, testing, securing, documenting, containerizing, and maintaining software engineering projects autonomously.

```
                              +---------------------------------------+
                              |         NexusAI OS Operating System   |
                              | React 18 + Vite + Tailwind CSS UI     |
                              | (Workflow Builder, Playground, Canvas)|
                              +-------------------+-------------------+
                                                  |
                                                  v REST / WebSockets / Telemetry
                              +-------------------+-------------------+
                              |     NexusAI OS FastAPI Control Plane  |
                              |   (RBAC, JWT, Audit, OpenTelemetry)   |
                              +---------+-------------------+---------+
                                        |                   |
                                        v                   v
            +---------------------------+----+   +----------+--------------------+
            | Asynchronous Agent Event Bus   |   |   Plugin Marketplace & MCP Engine |
            | (Pub/Sub, DLQ, Replay, Tracing)|   | (FileSystem, Docker, GitHub, DB,  |
            | Correlation IDs & Retry Queues |---| Terminal, Jira, Slack, Notion,    |
            +---------------------------+----+   |  Playwright, Kubernetes, Git)     |
                                        |        +-----------------------------------+
                                        v
            +---------------------------+------------------------------------+
            |               Specialized Autonomous AI Employees              |
            |  CEO, PM, Dev, QA, Security, Database, DevOps, Doc, Mktg,         |
            |  + Dedicated Self-Reflection Agent                              |
            +---------------------------+------------------------------------+
                                        |
       +--------------------------------+--------------------------------+
       |                                |                                |
       v                                v                                v
+------+-----------------+    +---------+----------------+   +-----------+----------------+
| Multi-Layer Memory     |    | Knowledge Graph Engine   |   | Isolated Execution Sandbox |
| Short-Term: Redis      |    | Relational Topology    |   | Isolated Python, Node,     |
| Working: PostgreSQL    |    | Projects -> Tasks ->     |   | Shell Container Sandbox    |
| Long-Term: Qdrant      |    | Files -> Deployments     |   +----------------------------+
+------------------------+    +--------------------------+
```

## Key Architectural Principles

1. **100% Free & Open-Source LLM Stack**: Zero paid LLM APIs required. Dynamic task-based routing across **Gemini 2.5 Flash Free Tier**, **DeepSeek Coder**, **Qwen 3**, and local **Ollama** (Llama 3/Mistral/Phi).
2. **Event-Driven Agent Communication**: Agents communicate exclusively through an asynchronous Event Bus supporting Pub/Sub, correlation IDs, Dead Letter Queues (DLQ), and execution replay.
3. **Model Context Protocol (MCP) First**: Extensible plugin architecture supporting 14 integrations (Filesystem, Terminal, Docker, PostgreSQL, GitHub, Jira, Slack, Gmail, Google Calendar, Notion, Git, Playwright, Kubernetes).
4. **Multi-Layer Memory System**: Ephemeral Redis cache, PostgreSQL working memory, and Qdrant semantic long-term memory for experience retrieval.
5. **Knowledge Graph Topology Engine**: Queryable relational graph linking Projects -> Tasks -> Repositories -> Deployments -> APIs.
6. **Code Sandbox Engine**: Code execution isolated inside ephemeral sandbox containers with strict timeout and resource caps.
7. **Human-in-the-Loop (HITL) Checkpoints**: Safety engine tagging destructive terminal commands, migrations, or force pushes for human reviewer approval.

---

## Quick Setup Guide

### 1. Environment & Virtualenv
```bash
git clone https://github.com/nexusai-os/nexusai-os.git
cd nexusai-os

python -m venv .venv
source .venv/bin/activate  # On Windows: .venv\Scripts\activate
pip install -r requirements.txt
```

### 2. Run Test Verification Suite
```bash
pytest tests/ -v
```

---

## License & Contribution
Released under the MIT License. Contributions welcome!
