"""
WebSocket Server for real-time GAIA Core ↔ Desktop communication.
Three-plane architecture: Core (8080), Bridge (8081), Overlay (8082)

Factor 11 (Order): Typed message contracts, deterministic routing
Factor 10 (Chaos): Asynchronous event-driven architecture
Factor 12 (Balance): Equilibrium-aware message throttling
Factor 13 (Heart): Crisis detection never throttled
"""

import asyncio
import json
import logging
from typing import Dict, Set, Optional
from dataclasses import dataclass, asdict
import websockets
from datetime import datetime

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)


@dataclass
class GAIAMessage:
    """Standard message format across all planes."""
    type: str  # zscore, crisis, avatar_response, equilibrium, etc.
    plane: str  # core, bridge, overlay
    timestamp: str
    data: dict
    reality_label: str = "NONFICTION"  # E0-E5 evidence grading
    
    def to_json(self) -> str:
        return json.dumps(asdict(self))


class GAIAWebSocketServer:
    """
    WebSocket server managing real-time updates from GAIA backend.
    Supports Three-Plane architecture with separate channels.
    """
    
    def __init__(self, host='localhost', core_port=8765, bridge_port=8766, overlay_port=8767, env='development'):
        """Initialize WebSocket server.
        
        Args:
            host: Server hostname
            core_port: Port for Core plane WebSocket
            bridge_port: Port for Bridge plane WebSocket
            overlay_port: Port for Overlay plane WebSocket
            env: Environment ('development' or 'production')
        """
        self.host = host
        self.core_port = core_port
        self.bridge_port = bridge_port
        self.overlay_port = overlay_port
        self.env = env
        
        self.core_clients: Set[websockets.WebSocketServerProtocol] = set()
        self.bridge_clients: Set[websockets.WebSocketServerProtocol] = set()
        self.overlay_clients: Set[websockets.WebSocketServerProtocol] = set()
        
        # Simulated backend state (replace with actual GAIA Core integration)
        self.current_z_score: float = 5.5
        self.avatar_state: Dict = {"mood": "attentive", "autonomy": 0.3}
        self.equilibrium: Dict = {"capacity": 85, "state": "healthy"}
    
    async def register_client(self, websocket, plane: str):
        """Register client to specific plane channel."""
        if plane == "core":
            self.core_clients.add(websocket)
            logger.info(f"Core client connected: {websocket.remote_address}")
        elif plane == "bridge":
            self.bridge_clients.add(websocket)
            logger.info(f"Bridge client connected: {websocket.remote_address}")
        elif plane == "overlay":
            self.overlay_clients.add(websocket)
            logger.info(f"Overlay client connected: {websocket.remote_address}")
        
        # Send initial state
        await self.send_initial_state(websocket, plane)
    
    async def unregister_client(self, websocket, plane: str):
        """Remove client from plane channel."""
        if plane == "core":
            self.core_clients.discard(websocket)
        elif plane == "bridge":
            self.bridge_clients.discard(websocket)
        elif plane == "overlay":
            self.overlay_clients.discard(websocket)
        logger.info(f"Client disconnected from {plane}")
    
    async def send_initial_state(self, websocket, plane: str):
        """Send current state snapshot to newly connected client."""
        messages = [
            GAIAMessage(
                type="zscore",
                plane=plane,
                timestamp=datetime.utcnow().isoformat(),
                data={"value": self.current_z_score, "trend": "stable"},
                reality_label="E2"
            ),
            GAIAMessage(
                type="equilibrium",
                plane=plane,
                timestamp=datetime.utcnow().isoformat(),
                data=self.equilibrium,
                reality_label="E3"
            ),
            GAIAMessage(
                type="avatar_state",
                plane=plane,
                timestamp=datetime.utcnow().isoformat(),
                data=self.avatar_state,
                reality_label="E1"
            )
        ]
        
        for msg in messages:
            await websocket.send(msg.to_json())
    
    async def broadcast_to_plane(self, message: GAIAMessage, plane: str):
        """Broadcast message to all clients on specific plane."""
        clients = {
            "core": self.core_clients,
            "bridge": self.bridge_clients,
            "overlay": self.overlay_clients
        }.get(plane, set())
        
        if clients:
            await asyncio.gather(
                *[client.send(message.to_json()) for client in clients],
                return_exceptions=True
            )
    
    async def handle_client_message(self, websocket, message: str, plane: str):
        """Process incoming messages from desktop client."""
        try:
            data = json.loads(message)
            msg_type = data.get("type")
            
            if msg_type == "user_input":
                # Process user message through Avatar
                response = await self.process_user_input(data.get("content", ""))
                reply = GAIAMessage(
                    type="avatar_response",
                    plane="overlay",
                    timestamp=datetime.utcnow().isoformat(),
                    data=response,
                    reality_label="E1"
                )
                await websocket.send(reply.to_json())
            
            elif msg_type == "request_zscore":
                # Calculate/retrieve Z score
                z_msg = GAIAMessage(
                    type="zscore",
                    plane="core",
                    timestamp=datetime.utcnow().isoformat(),
                    data={"value": self.current_z_score, "breakdown": {
                        "order": 0.6, "freedom": 0.4, "balance": 0.8
                    }},
                    reality_label="E2"
                )
                await websocket.send(z_msg.to_json())
            
            elif msg_type == "crisis_alert":
                # Trigger crisis protocol
                await self.handle_crisis(data, websocket)
        
        except json.JSONDecodeError:
            logger.error(f"Invalid JSON from client: {message}")
        except Exception as e:
            logger.error(f"Error handling message: {e}")
    
    async def process_user_input(self, user_message: str) -> Dict:
        """
        Process user input through Avatar system.
        TODO: Integrate with actual overlay/avatar/personality.py
        """
        # Placeholder - replace with actual Avatar inference
        return {
            "response": f"Avatar received: '{user_message}'",
            "emotion": "attentive",
            "equilibrium_impact": 0.05
        }
    
    async def handle_crisis(self, data: Dict, websocket):
        """Crisis detection protocol - Factor 13 protection."""
        crisis_msg = GAIAMessage(
            type="crisis",
            plane="core",
            timestamp=datetime.utcnow().isoformat(),
            data={
                "level": "CRITICAL",
                "resources": [
                    "988 - Suicide & Crisis Lifeline",
                    "Text HOME to 741741 - Crisis Text Line"
                ],
                "avatar_message": "I see you. You're not alone. Please reach out NOW."
            },
            reality_label="NONFICTION"
        )
        
        # Broadcast to all planes - this is life-critical
        await self.broadcast_to_plane(crisis_msg, "core")
        await self.broadcast_to_plane(crisis_msg, "bridge")
        await self.broadcast_to_plane(crisis_msg, "overlay")
        
        logger.critical(f"CRISIS PROTOCOL ACTIVATED: {data}")
    
    async def connection_handler(self, websocket, path: str):
        """Main WebSocket connection handler."""
        # Determine plane from path: /core, /bridge, /overlay
        plane = path.strip("/") or "overlay"
        
        await self.register_client(websocket, plane)
        
        try:
            async for message in websocket:
                await self.handle_client_message(websocket, message, plane)
        except websockets.exceptions.ConnectionClosed:
            logger.info(f"Connection closed normally: {plane}")
        finally:
            await self.unregister_client(websocket, plane)
    
    async def heartbeat_loop(self):
        """
        Periodic updates - Z score recalculation, equilibrium checks.
        This simulates GAIA Core's real-time monitoring.
        """
        while True:
            await asyncio.sleep(5)  # Update every 5 seconds
            
            # Simulate Z score fluctuation (replace with actual calculation)
            if self.env == 'development':
                # Placeholder for testing
                import random
                self.current_z_score = max(0, min(12, self.current_z_score + random.uniform(-0.2, 0.2)))
            else:
                # TODO: Replace with actual ZScoreCalculator
                # from core.zscore.calculator import ZScoreCalculator
                # self.current_z_score = ZScoreCalculator().calculate(...)
                raise NotImplementedError("Production Z score calculation not implemented. See Issue #3.")
            
            z_update = GAIAMessage(
                type="zscore_update",
                plane="core",
                timestamp=datetime.utcnow().isoformat(),
                data={"value": round(self.current_z_score, 2)},
                reality_label="E2"
            )
            
            await self.broadcast_to_plane(z_update, "core")
            await self.broadcast_to_plane(z_update, "overlay")
    
    async def start(self, host=None, core_port=None, bridge_port=None, overlay_port=None):
        """Start WebSocket servers for all three planes.
        
        Args:
            host: Override instance host
            core_port: Override instance core_port
            bridge_port: Override instance bridge_port
            overlay_port: Override instance overlay_port
        """
        # Use instance variables if not overridden
        host = host or self.host
        core_port = core_port or self.core_port
        bridge_port = bridge_port or self.bridge_port
        overlay_port = overlay_port or self.overlay_port
        
        async def core_handler(ws, path):
            await self.connection_handler(ws, "/core")
        
        async def bridge_handler(ws, path):
            await self.connection_handler(ws, "/bridge")
        
        async def overlay_handler(ws, path):
            await self.connection_handler(ws, "/overlay")
        
        core_server = await websockets.serve(core_handler, host, core_port)
        bridge_server = await websockets.serve(bridge_handler, host, bridge_port)
        overlay_server = await websockets.serve(overlay_handler, host, overlay_port)
        
        logger.info(f"Core Plane WebSocket: ws://{host}:{core_port}")
        logger.info(f"Bridge Plane WebSocket: ws://{host}:{bridge_port}")
        logger.info(f"Overlay Plane WebSocket: ws://{host}:{overlay_port}")
        
        # Start heartbeat
        asyncio.create_task(self.heartbeat_loop())
        
        await asyncio.gather(
            core_server.wait_closed(),
            bridge_server.wait_closed(),
            overlay_server.wait_closed()
        )


async def main():
    server = GAIAWebSocketServer()
    await server.start()


if __name__ == "__main__":
    asyncio.run(main())
