"""GAIA WebSocket Server - Three-Plane Architecture.

Provides real-time bidirectional communication for:
- Core Plane: Foundation data (Z-scores, crisis alerts)
- Bridge Plane: Transformation events (alchemical transitions)
- Overlay Plane: Meaning layer (Avatar messages, guidance)

CORRECTED:
- Constructor now accepts host, port parameters (fixes test TypeError)
- Added environment detection (development vs production)
- Production mode requires real Z-score injection via inject_z_score()
"""

import asyncio
import json
import random
import websockets
from dataclasses import dataclass, asdict
from datetime import datetime
from typing import Set, Optional
import logging

logger = logging.getLogger(__name__)


@dataclass
class HeartbeatMessage:
    """Heartbeat message with current Z-score and system state."""
    type: str = "heartbeat"
    z_score: float = 0.0
    timestamp: str = ""
    plane: str = "core"
    synthetic: bool = False  # True if using random walk (development mode)


class GAIAWebSocketServer:
    """WebSocket server for GAIA three-plane architecture."""

    def __init__(
        self,
        host: str = 'localhost',
        core_port: int = 8765,
        bridge_port: int = 8766,
        overlay_port: int = 8767,
        env: str = 'production',
    ):
        """Initialize WebSocket server.
        
        Args:
            host: Host to bind to
            core_port: Port for Core Plane WebSocket
            bridge_port: Port for Bridge Plane WebSocket
            overlay_port: Port for Overlay Plane WebSocket
            env: Environment mode ('development' or 'production')
        """
        self.host = host
        self.core_port = core_port
        self.bridge_port = bridge_port
        self.overlay_port = overlay_port
        self.env = env
        
        # Connected clients per plane
        self.core_clients: Set[websockets.WebSocketServerProtocol] = set()
        self.bridge_clients: Set[websockets.WebSocketServerProtocol] = set()
        self.overlay_clients: Set[websockets.WebSocketServerProtocol] = set()
        
        # Current Z-score (injected or synthetic)
        self.current_z_score: Optional[float] = None
        
        # Heartbeat task
        self.heartbeat_task: Optional[asyncio.Task] = None

    def inject_z_score(self, z_score: float):
        """Inject real Z-score from biosignal pipeline.
        
        Call this method when new Z-score is calculated from actual data.
        
        Args:
            z_score: Calculated Z-score (0-12)
        """
        if not (0 <= z_score <= 12):
            raise ValueError(f"Z-score {z_score} outside valid range [0, 12]")
        
        self.current_z_score = z_score
        logger.info(f"Injected real Z-score: {z_score:.2f}")

    async def _generate_heartbeat(self) -> HeartbeatMessage:
        """Generate heartbeat message with Z-score.
        
        In development mode: uses random walk for testing
        In production mode: requires real Z-score injection
        """
        synthetic = False
        
        if self.env == 'development':
            # Development: Random walk for testing
            if self.current_z_score is None:
                self.current_z_score = 6.0  # Start at neutral
            
            # Random walk with bounds
            self.current_z_score = max(0, min(12, 
                self.current_z_score + random.uniform(-0.2, 0.2)
            ))
            synthetic = True
        
        # Production: Only broadcast if real Z-score injected
        if self.current_z_score is None:
            # No data yet, skip heartbeat
            return None
        
        return HeartbeatMessage(
            z_score=self.current_z_score,
            timestamp=datetime.utcnow().isoformat(),
            synthetic=synthetic,
        )

    async def _heartbeat_loop(self, interval: float = 1.0):
        """Broadcast heartbeat to all connected clients.
        
        Args:
            interval: Seconds between heartbeats
        """
        while True:
            try:
                heartbeat = await self._generate_heartbeat()
                
                if heartbeat:
                    message = json.dumps(asdict(heartbeat))
                    
                    # Broadcast to all planes
                    await self._broadcast(self.core_clients, message)
                    await self._broadcast(self.bridge_clients, message)
                    await self._broadcast(self.overlay_clients, message)
                
                await asyncio.sleep(interval)
            except Exception as e:
                logger.error(f"Heartbeat error: {e}")
                await asyncio.sleep(interval)

    async def _broadcast(self, clients: Set, message: str):
        """Broadcast message to all clients in a set."""
        if clients:
            await asyncio.gather(
                *[client.send(message) for client in clients],
                return_exceptions=True,
            )

    async def _core_plane_handler(self, websocket, path):
        """Handle Core Plane WebSocket connections."""
        self.core_clients.add(websocket)
        logger.info(f"Core Plane client connected: {websocket.remote_address}")
        
        try:
            async for message in websocket:
                # Handle incoming Core Plane messages
                data = json.loads(message)
                logger.debug(f"Core Plane received: {data}")
                
                # Echo for now (Phase 1)
                await websocket.send(json.dumps({
                    "type": "echo",
                    "data": data,
                    "plane": "core",
                }))
        except websockets.exceptions.ConnectionClosed:
            pass
        finally:
            self.core_clients.remove(websocket)
            logger.info(f"Core Plane client disconnected")

    async def _bridge_plane_handler(self, websocket, path):
        """Handle Bridge Plane WebSocket connections."""
        self.bridge_clients.add(websocket)
        logger.info(f"Bridge Plane client connected: {websocket.remote_address}")
        
        try:
            async for message in websocket:
                data = json.loads(message)
                logger.debug(f"Bridge Plane received: {data}")
                
                await websocket.send(json.dumps({
                    "type": "echo",
                    "data": data,
                    "plane": "bridge",
                }))
        except websockets.exceptions.ConnectionClosed:
            pass
        finally:
            self.bridge_clients.remove(websocket)
            logger.info(f"Bridge Plane client disconnected")

    async def _overlay_plane_handler(self, websocket, path):
        """Handle Overlay Plane WebSocket connections."""
        self.overlay_clients.add(websocket)
        logger.info(f"Overlay Plane client connected: {websocket.remote_address}")
        
        try:
            async for message in websocket:
                data = json.loads(message)
                logger.debug(f"Overlay Plane received: {data}")
                
                await websocket.send(json.dumps({
                    "type": "echo",
                    "data": data,
                    "plane": "overlay",
                }))
        except websockets.exceptions.ConnectionClosed:
            pass
        finally:
            self.overlay_clients.remove(websocket)
            logger.info(f"Overlay Plane client disconnected")

    async def start(self):
        """Start all three WebSocket servers."""
        logger.info(f"Starting GAIA WebSocket servers in {self.env} mode...")
        
        # Start servers
        core_server = await websockets.serve(
            self._core_plane_handler,
            self.host,
            self.core_port,
        )
        logger.info(f"Core Plane: ws://{self.host}:{self.core_port}")
        
        bridge_server = await websockets.serve(
            self._bridge_plane_handler,
            self.host,
            self.bridge_port,
        )
        logger.info(f"Bridge Plane: ws://{self.host}:{self.bridge_port}")
        
        overlay_server = await websockets.serve(
            self._overlay_plane_handler,
            self.host,
            self.overlay_port,
        )
        logger.info(f"Overlay Plane: ws://{self.host}:{self.overlay_port}")
        
        # Start heartbeat
        self.heartbeat_task = asyncio.create_task(self._heartbeat_loop())
        
        logger.info("All WebSocket servers running")
        
        # Keep servers running
        await asyncio.Future()  # Run forever


if __name__ == "__main__":
    # Development server for testing
    logging.basicConfig(level=logging.INFO)
    server = GAIAWebSocketServer(
        host='0.0.0.0',
        env='development',  # Use synthetic Z-scores
    )
    asyncio.run(server.start())
