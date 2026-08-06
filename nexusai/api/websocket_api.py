"""
WebSocket Streaming Manager for NexusAI OS (v0.4.0).
Streams agent execution logs, workflow progress, tool telemetry, memory retrieval events, and executive decisions in real-time.
"""
import asyncio
import json
import logging
from typing import Any, Dict, List, Set
from fastapi import APIRouter, WebSocket, WebSocketDisconnect

logger = logging.getLogger("nexusai.websocket")

ws_router = APIRouter(tags=["WebSocket Real-Time Progress Stream"])


class ConnectionManager:
    """Manages active client WebSocket connections and broadcasts telemetry messages."""

    def __init__(self):
        self.active_connections: Set[WebSocket] = set()

    async def connect(self, websocket: WebSocket):
        await websocket.accept()
        self.active_connections.add(websocket)
        logger.info(f"Client connected via WebSocket. Active total: {len(self.active_connections)}")

    def disconnect(self, websocket: WebSocket):
        self.active_connections.discard(websocket)
        logger.info(f"Client disconnected from WebSocket. Active total: {len(self.active_connections)}")

    async def broadcast(self, message: Dict[str, Any]):
        """Broadcasts telemetry payload to all connected dashboard subscribers."""
        dead_sockets = set()
        for connection in self.active_connections:
            try:
                await connection.send_json(message)
            except Exception as e:
                logger.warning(f"Error broadcasting to socket: {e}")
                dead_sockets.add(connection)

        for dead in dead_sockets:
            self.disconnect(dead)


ws_manager = ConnectionManager()


@ws_router.websocket("/ws/telemetry")
async def websocket_telemetry_endpoint(websocket: WebSocket):
    """Real-time telemetry WebSocket streaming endpoint for the dashboard."""
    await ws_manager.connect(websocket)
    try:
        # Send initial welcome message
        await websocket.send_json({
            "event_type": "CONNECTED",
            "message": "Connected to NexusAI OS Telemetry Bus (v0.4.0)",
            "system_status": "OPERATIONAL"
        })
        while True:
            # Keep connection open and listen for client ping/messages
            data = await websocket.receive_text()
            await websocket.send_json({"event_type": "ACK", "client_message": data})
    except WebSocketDisconnect:
        ws_manager.disconnect(websocket)
    except Exception as e:
        logger.error(f"WebSocket error: {e}")
        ws_manager.disconnect(websocket)
