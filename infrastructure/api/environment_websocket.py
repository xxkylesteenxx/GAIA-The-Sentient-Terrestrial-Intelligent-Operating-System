"""
Living Environment WebSocket Server
Broadcasts EnvironmentState every 15 seconds to all connected clients.

Evidence Grade: E5 (network protocol)
"""

import asyncio
import json
import logging
import os
from datetime import datetime, timezone
from typing import Set

try:
    import websockets
    from websockets.server import WebSocketServerProtocol
except ImportError:
    print("ERROR: websockets not installed. Run: pip install websockets>=12.0")
    raise

from bridge.environment.engine import LivingEnvironmentEngine

logger = logging.getLogger(__name__)


class EnvironmentWebSocketServer:
    """
    WebSocket server broadcasting EnvironmentState updates.
    Listens on ws://localhost:8767/environment
    """
    
    def __init__(
        self,
        host: str = "0.0.0.0",
        port: int = 8767,
        latitude: float = 37.7749,
        longitude: float = -122.4194,
        openweather_api_key: str = None,
        broadcast_interval: int = 15
    ):
        self.host = host
        self.port = port
        self.broadcast_interval = broadcast_interval
        
        # Living Environment Engine
        self.engine = LivingEnvironmentEngine(
            latitude=latitude,
            longitude=longitude,
            openweather_api_key=openweather_api_key
        )
        
        # Connected clients
        self.clients: Set[WebSocketServerProtocol] = set()
        
        logger.info(f"EnvironmentWebSocketServer configured on {host}:{port}")
    
    async def register_client(self, websocket: WebSocketServerProtocol):
        """Register new client connection."""
        self.clients.add(websocket)
        logger.info(f"Client connected: {websocket.remote_address} (total: {len(self.clients)})")
        
        # Send immediate state on connection
        state = self.engine.get_state()
        await websocket.send(json.dumps({
            "type": "environment_state",
            "data": state.to_dict()
        }))
    
    async def unregister_client(self, websocket: WebSocketServerProtocol):
        """Unregister disconnected client."""
        self.clients.discard(websocket)
        logger.info(f"Client disconnected: {websocket.remote_address} (total: {len(self.clients)})")
    
    async def broadcast_state(self):
        """Broadcast current EnvironmentState to all clients."""
        if not self.clients:
            return
        
        state = self.engine.get_state()
        message = json.dumps({
            "type": "environment_state",
            "data": state.to_dict(),
            "timestamp": datetime.now(timezone.utc).isoformat()
        })
        
        # Broadcast to all clients
        disconnected = set()
        for client in self.clients:
            try:
                await client.send(message)
            except websockets.exceptions.ConnectionClosed:
                disconnected.add(client)
        
        # Clean up disconnected clients
        for client in disconnected:
            await self.unregister_client(client)
    
    async def broadcast_loop(self):
        """Background task: broadcast state every N seconds."""
        while True:
            try:
                await self.broadcast_state()
                await asyncio.sleep(self.broadcast_interval)
            except Exception as e:
                logger.error(f"Broadcast error: {e}", exc_info=True)
                await asyncio.sleep(5)
    
    async def handler(self, websocket: WebSocketServerProtocol, path: str):
        """WebSocket connection handler."""
        await self.register_client(websocket)
        
        try:
            async for message in websocket:
                try:
                    data = json.loads(message)
                    
                    if data.get("type") == "update_z_score":
                        z_score = float(data.get("z_score", 6.0))
                        self.engine.update_z_score(z_score)
                        logger.info(f"Z-score updated to {z_score:.2f} by client")
                    
                except json.JSONDecodeError:
                    logger.warning(f"Invalid JSON from client: {message}")
                except Exception as e:
                    logger.error(f"Handler error: {e}", exc_info=True)
        
        finally:
            await self.unregister_client(websocket)
    
    async def start(self):
        """Start WebSocket server and broadcast loop."""
        # Start broadcast loop
        asyncio.create_task(self.broadcast_loop())
        
        # Start WebSocket server
        async with websockets.serve(self.handler, self.host, self.port):
            logger.info(f"🌍 Environment WebSocket server running on ws://{self.host}:{self.port}")
            await asyncio.Future()


if __name__ == "__main__":
    logging.basicConfig(
        level=logging.INFO,
        format="%(asctime)s - %(name)s - %(levelname)s - %(message)s"
    )
    
    server = EnvironmentWebSocketServer(
        host="0.0.0.0",
        port=8767,
        latitude=float(os.getenv("GAIA_LATITUDE", "29.4241")),  # San Antonio default
        longitude=float(os.getenv("GAIA_LONGITUDE", "-98.4936")),
        openweather_api_key=os.getenv("OPENWEATHER_API_KEY"),
        broadcast_interval=15
    )
    
    asyncio.run(server.start())
