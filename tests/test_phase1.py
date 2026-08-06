"""
NexusAI OS Phase 1 Test Suite.
Verifies system configuration, Event Bus (Pub/Sub, Correlation IDs, Replay), Intelligent LLM Router, Code Sandbox, and Security modules.
"""
import pytest
from nexusai.core.config import settings
from nexusai.core.event_bus import AgentEventBus, AgentEvent
from nexusai.core.intelligent_router import IntelligentLLMRouter, TaskCategory
from nexusai.core.sandbox import CodeSandboxEngine
from nexusai.core.security import hash_password, verify_password, create_access_token, decode_access_token


def test_nexusai_configuration():
    """Verify system settings initialization."""
    assert settings.APP_NAME == "NexusAI OS"
    assert settings.DEFAULT_LLM_PROVIDER in ["gemini", "ollama", "deepseek", "qwen", "mock"]
    assert settings.ENABLE_HITL_APPROVAL is True


@pytest.mark.asyncio
async def test_nexusai_event_bus():
    """Test Pub/Sub agent event publishing and correlation ID replay."""
    bus = AgentEventBus()
    received = []

    async def listener(event: AgentEvent):
        received.append(event)

    bus.subscribe("SPRINT_PLANNED", listener)

    event = AgentEvent(
        event_type="SPRINT_PLANNED",
        correlation_id="trace-nexus-1",
        sender_agent="Project Manager Agent",
        payload={"sprint": 1, "tasks": ["Task A", "Task B"]}
    )

    await bus.publish(event)
    import asyncio
    await asyncio.sleep(0.1)

    assert len(received) == 1
    assert received[0].correlation_id == "trace-nexus-1"

    replayed = await bus.replay_events("trace-nexus-1")
    assert len(replayed) == 1
    assert replayed[0].event_id == event.event_id


@pytest.mark.asyncio
async def test_intelligent_router_classification():
    """Test prompt category intent classification."""
    router = IntelligentLLMRouter()

    cat_plan = router.determine_category("Analyze architecture strategy for NexusAI")
    assert cat_plan == TaskCategory.PLANNING

    cat_code = router.determine_category("Write a python function to query database")
    assert cat_code == TaskCategory.CODING

    res = await router.route_and_generate("Analyze system architecture")
    assert res["category"] == TaskCategory.PLANNING.value
    assert res["latency_ms"] >= 0


@pytest.mark.asyncio
async def test_code_sandbox_execution():
    """Test Python execution inside isolated sandbox."""
    sandbox = CodeSandboxEngine(timeout_seconds=5.0)

    res = await sandbox.execute_code("print('NexusAI OS Execution Sandbox Active')", language="python")
    assert res.success is True
    assert "NexusAI OS Execution Sandbox Active" in res.stdout


def test_security_hashing_and_jwt():
    """Test password hashing and JWT encoding/decoding."""
    password = "secretpassword123"
    hashed = hash_password(password)
    assert verify_password(password, hashed) is True

    token = create_access_token({"sub": "admin_user", "role": "architect"})
    decoded = decode_access_token(token)
    assert decoded["sub"] == "admin_user"
    assert decoded["role"] == "architect"
