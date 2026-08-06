"""
Asynchronous Agent Event Bus for NexusAI OS.
Implements Pub/Sub architecture, correlation IDs, event replay, retries, and Dead Letter Queue (DLQ).
Agents communicate EXCLUSIVELY via events on this bus.
"""
import asyncio
from datetime import datetime, timezone
import logging
import uuid
from typing import Any, Callable, Coroutine, Dict, List, Optional
from pydantic import BaseModel, Field

logger = logging.getLogger("nexusai.event_bus")


class AgentEvent(BaseModel):
    """Standardized event wrapper for inter-agent asynchronous communication."""
    event_id: str = Field(default_factory=lambda: str(uuid.uuid4()))
    event_type: str = Field(..., description="e.g. PROJECT_CREATED, SPRINT_PLANNED, CODE_SYNTHESIZED")
    correlation_id: str = Field(..., description="Unique workflow/transaction execution trace ID")
    sender_agent: str = Field(..., description="Name of publisher agent persona")
    payload: Dict[str, Any] = Field(default_factory=dict)
    timestamp: str = Field(default_factory=lambda: datetime.now(timezone.utc).isoformat())
    retry_count: int = Field(default=0)
    max_retries: int = Field(default=3)


SubscriberCallback = Callable[[AgentEvent], Coroutine[Any, Any, None]]


class AgentEventBus:
    """Central Asynchronous Event Bus with Pub/Sub, DLQ, and Replay capabilities."""

    def __init__(self):
        self.subscribers: Dict[str, List[SubscriberCallback]] = {}
        self.event_history: List[AgentEvent] = []
        self.dead_letter_queue: List[AgentEvent] = []
        self._lock = asyncio.Lock()

    def subscribe(self, event_type: str, callback: SubscriberCallback) -> None:
        """Subscribes an agent callback function to a specific event type."""
        if event_type not in self.subscribers:
            self.subscribers[event_type] = []
        self.subscribers[event_type].append(callback)
        logger.info(f"Subscribed callback to event type '{event_type}'")

    async def publish(self, event: AgentEvent) -> None:
        """Publishes an event to all subscribed listeners asynchronously."""
        async with self._lock:
            self.event_history.append(event)

        logger.info(f"Publishing event [{event.event_type}] from '{event.sender_agent}' (CorrID: {event.correlation_id})")
        callbacks = self.subscribers.get(event.event_type, [])

        if not callbacks:
            logger.warning(f"No subscribers registered for event type '{event.event_type}'")
            return

        for callback in callbacks:
            asyncio.create_task(self._safe_execute_subscriber(callback, event))

    async def _safe_execute_subscriber(self, callback: SubscriberCallback, event: AgentEvent) -> None:
        """Executes subscriber callback with automatic retries and DLQ routing."""
        try:
            await callback(event)
        except Exception as exc:
            logger.error(f"Error executing subscriber for event '{event.event_type}': {exc}")
            if event.retry_count < event.max_retries:
                event.retry_count += 1
                logger.info(f"Retrying event '{event.event_id}' (Attempt {event.retry_count}/{event.max_retries})...")
                await asyncio.sleep(0.5 * event.retry_count)
                await self._safe_execute_subscriber(callback, event)
            else:
                logger.critical(f"Event '{event.event_id}' exceeded max retries. Moving to Dead Letter Queue (DLQ).")
                async with self._lock:
                    self.dead_letter_queue.append(event)

    async def replay_events(self, correlation_id: str) -> List[AgentEvent]:
        """Replays historical events matching a correlation ID in chronological order."""
        async with self._lock:
            matched = [e for e in self.event_history if e.correlation_id == correlation_id]
            logger.info(f"Replaying {len(matched)} events for correlation ID: {correlation_id}")
            return matched

    async def get_dlq_events(self) -> List[AgentEvent]:
        """Returns current events sitting in the Dead Letter Queue."""
        async with self._lock:
            return list(self.dead_letter_queue)


# Singleton Event Bus instance
event_bus = AgentEventBus()
