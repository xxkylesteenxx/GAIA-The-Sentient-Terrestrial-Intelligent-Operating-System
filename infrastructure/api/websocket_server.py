"""
GAIA WEBSOCKET API SERVER
Infrastructure Layer — Three-Port Architecture

Ports:
    Core port    (default 8765) — Z-score, safety, crisis events
    Bridge port  (default 8766) — Alchemical transitions, pattern state
    Overlay port (default 8767) — Avatar speech, memory events, UI updates

All real-time Z-score broadcasts come from an actual ZScoreCalculator.
The heartbeat loop broadcasts the most recently computed Z-score.
In development mode only, a random walk is used when no real
biosignal data is available — this is clearly labelled as synthetic.
"""

from __future__ import annotations

import asyncio
import json
import logging
import random
from datetime import datetime
from typing import Any, Dict, Optional, Set

import websockets
from websockets.server import WebSocketServerProtocol

from core.zscore.calculator import ZScoreCalculator
from core.safety.crisis_detector import CrisisDetector, CrisisLevel
from core.constants import Z_CRISIS_CRITICAL, Z_CRISIS_HIGH

logger = logging.getLogger(__name__)


# ---------------------------------------------------------------------------
# Message types
# ---------------------------------------------------------------------------

MESSAGE_TYPES = {
    "Z_UPDATE": "z_score_update",
    "CRISIS_ALERT": "crisis_alert",
    "STAGE_TRANSITION": "stage_transition",
    "AVATAR_SPEECH": "avatar_speech",
    "SYSTEM_STATUS": "system_status",
    "HEARTBEAT": "heartbeat",
    "ERROR": "error",
}


# ---------------------------------------------------------------------------
# WebSocket server
# ---------------------------------------------------------------------------


class GAIAWebSocketServer:
    """
    Real-time WebSocket server broadcasting GAIA state.

    Args:
        host:            Bind address (default 'localhost').
        core_port:       Port for Core plane events (default 8765).
        bridge_port:     Port for Bridge plane events (default 8766).
        overlay_port:    Port for Overlay plane events (default 8767).
        env:             'development' | 'production'. In development mode
                         the heartbeat uses a synthetic random-walk Z-score
                         when no real biosignal data is available.
                         In production the heartbeat only broadcasts when
                         real data is present.

    Usage::

        server = GAIAWebSocketServer(host='0.0.0.0', core_port=8765)
        await server.start()
    """

    def __init__(
        self,
        host: str = "localhost",
        core_port: int = 8765,
        bridge_port: int = 8766,
        overlay_port: int = 8767,
        env: str = "production",
    ) -> None:
        self.host = host
        self.core_port = core_port
        self.bridge_port = bridge_port
        self.overlay_port = overlay_port
        self.env = env

        # Connected clients per plane
        self.core_clients: Set[WebSocketServerProtocol] = set()
        self.bridge_clients: Set[WebSocketServerProtocol] = set()
        self.overlay_clients: Set[WebSocketServerProtocol] = set()

        # Shared state
        self.current_z_score: float = 6.0   # Start at mid-range (Albedo)
        self.last_real_z: Optional[float] = None  # Set by inject_z_score()

        # Systems
        self.z_calculator = ZScoreCalculator()
        self.crisis_detector = CrisisDetector()

        self.running = False

        logger.info(
            "GAIAWebSocketServer configured — host=%s core=%d bridge=%d overlay=%d env=%s",
            host, core_port, bridge_port, overlay_port, env,
        )

    # ------------------------------------------------------------------ #
    # Public API                                                           #
    # ------------------------------------------------------------------ #

    def inject_z_score(self, z_score: float) -> None:
        """
        Inject a real Z-score from the biosignal pipeline.

        Call this whenever new biosignal data is processed.
        Once a real score is injected the heartbeat will use it instead
        of the synthetic random walk (even in development mode).
        """
        self.last_real_z = z_score
        self.current_z_score = z_score

    async def start(self) -> None:
        """Start all three WebSocket servers and the heartbeat loop."""
        self.running = True
        logger.info("Starting GAIA WebSocket servers…")

        await asyncio.gather(
            websockets.serve(self._core_handler, self.host, self.core_port),
            websockets.serve(self._bridge_handler, self.host, self.bridge_port),
            websockets.serve(self._overlay_handler, self.host, self.overlay_port),
            self._heartbeat_loop(),
        )

    async def stop(self) -> None:
        """Gracefully stop the server."""
        self.running = False
        for clients in (self.core_clients, self.bridge_clients, self.overlay_clients):
            for ws in list(clients):
                await ws.close()

    # ------------------------------------------------------------------ #
    # Connection handlers                                                  #
    # ------------------------------------------------------------------ #

    async def _core_handler(
        self, websocket: WebSocketServerProtocol, path: str
    ) -> None:
        self.core_clients.add(websocket)
        logger.info("Core client connected: %s", websocket.remote_address)

        try:
            await websocket.send(self._encode({
                "type": MESSAGE_TYPES["SYSTEM_STATUS"],
                "plane": "core",
                "z_score": self.current_z_score,
                "timestamp": _now(),
            }))

            async for raw in websocket:
                await self._handle_core_message(websocket, raw)

        except websockets.exceptions.ConnectionClosed:
            logger.info("Core client disconnected: %s", websocket.remote_address)
        finally:
            self.core_clients.discard(websocket)

    async def _bridge_handler(
        self, websocket: WebSocketServerProtocol, path: str
    ) -> None:
        self.bridge_clients.add(websocket)
        logger.info("Bridge client connected: %s", websocket.remote_address)

        try:
            await websocket.send(self._encode({
                "type": MESSAGE_TYPES["SYSTEM_STATUS"],
                "plane": "bridge",
                "z_score": self.current_z_score,
                "timestamp": _now(),
            }))

            async for raw in websocket:
                await self._handle_bridge_message(websocket, raw)

        except websockets.exceptions.ConnectionClosed:
            logger.info("Bridge client disconnected: %s", websocket.remote_address)
        finally:
            self.bridge_clients.discard(websocket)

    async def _overlay_handler(
        self, websocket: WebSocketServerProtocol, path: str
    ) -> None:
        self.overlay_clients.add(websocket)
        logger.info("Overlay client connected: %s", websocket.remote_address)

        try:
            await websocket.send(self._encode({
                "type": MESSAGE_TYPES["SYSTEM_STATUS"],
                "plane": "overlay",
                "z_score": self.current_z_score,
                "timestamp": _now(),
            }))

            async for raw in websocket:
                await self._handle_overlay_message(websocket, raw)

        except websockets.exceptions.ConnectionClosed:
            logger.info("Overlay client disconnected: %s", websocket.remote_address)
        finally:
            self.overlay_clients.discard(websocket)

    # ------------------------------------------------------------------ #
    # Message handlers                                                     #
    # ------------------------------------------------------------------ #

    async def _handle_core_message(
        self, websocket: WebSocketServerProtocol, raw: str
    ) -> None:
        try:
            msg = json.loads(raw)
        except json.JSONDecodeError:
            await websocket.send(self._encode({
                "type": MESSAGE_TYPES["ERROR"],
                "message": "Invalid JSON",
                "timestamp": _now(),
            }))
            return

        msg_type = msg.get("type", "")

        if msg_type == "biosignal_update":
            z_data = msg.get("z_score")
            if z_data and isinstance(z_data, (int, float)):
                self.inject_z_score(float(z_data))
                await self._broadcast_z_update()

        elif msg_type == "text_input":
            text = msg.get("text", "")
            z_result = self.z_calculator.estimate_from_text(text)
            self.inject_z_score(z_result["z_score"])

            crisis_report = self.crisis_detector.detect_comprehensive(
                z_score=z_result["z_score"],
                text=text,
            )

            await websocket.send(self._encode({
                "type": MESSAGE_TYPES["Z_UPDATE"],
                "z_score": z_result["z_score"],
                "components": {
                    "coherence": z_result["coherence"],
                    "fidelity": z_result["fidelity"],
                    "balance": z_result["balance"],
                },
                "stage": z_result["stage"],
                "crisis_report": crisis_report,
                "timestamp": _now(),
            }))

            if crisis_report["requires_emergency"]:
                await self._broadcast_crisis_alert(crisis_report)

    async def _handle_bridge_message(
        self, websocket: WebSocketServerProtocol, raw: str
    ) -> None:
        # Bridge plane handles pattern / alchemy queries
        try:
            msg = json.loads(raw)
        except json.JSONDecodeError:
            await websocket.send(self._encode({
                "type": MESSAGE_TYPES["ERROR"],
                "message": "Invalid JSON",
                "timestamp": _now(),
            }))
            return

        await websocket.send(self._encode({
            "type": MESSAGE_TYPES["SYSTEM_STATUS"],
            "received": msg,
            "z_score": self.current_z_score,
            "timestamp": _now(),
        }))

    async def _handle_overlay_message(
        self, websocket: WebSocketServerProtocol, raw: str
    ) -> None:
        # Overlay plane handles avatar speech / UI updates
        try:
            msg = json.loads(raw)
        except json.JSONDecodeError:
            await websocket.send(self._encode({
                "type": MESSAGE_TYPES["ERROR"],
                "message": "Invalid JSON",
                "timestamp": _now(),
            }))
            return

        await websocket.send(self._encode({
            "type": MESSAGE_TYPES["SYSTEM_STATUS"],
            "received": msg,
            "z_score": self.current_z_score,
            "timestamp": _now(),
        }))

    # ------------------------------------------------------------------ #
    # Broadcast helpers                                                    #
    # ------------------------------------------------------------------ #

    async def _broadcast_z_update(self) -> None:
        z = self.current_z_score
        classification = self.z_calculator.interpret_z_score(z)

        payload = self._encode({
            "type": MESSAGE_TYPES["Z_UPDATE"],
            "z_score": z,
            "stage": classification["stage"],
            "state": classification["state"],
            "color": classification["color"],
            "description": classification["description"],
            "timestamp": _now(),
        })

        await self._broadcast_to(self.core_clients, payload)
        await self._broadcast_to(self.bridge_clients, payload)

    async def _broadcast_crisis_alert(self, crisis_report: Dict) -> None:
        payload = self._encode({
            "type": MESSAGE_TYPES["CRISIS_ALERT"],
            "level": crisis_report["level"],
            "severity": crisis_report["severity"],
            "requires_emergency": crisis_report["requires_emergency"],
            "resources": [
                "Call or text 988 (Suicide & Crisis Lifeline)",
                "Text HELLO to 741741 (Crisis Text Line)",
            ],
            "timestamp": _now(),
        })

        # Crisis alerts go to ALL planes simultaneously
        for clients in (self.core_clients, self.bridge_clients, self.overlay_clients):
            await self._broadcast_to(clients, payload)

        logger.warning(
            "CRISIS ALERT broadcast — level=%s severity=%d",
            crisis_report["level"],
            crisis_report["severity"],
        )

    @staticmethod
    async def _broadcast_to(
        clients: Set[WebSocketServerProtocol], payload: str
    ) -> None:
        disconnected: Set[WebSocketServerProtocol] = set()
        for ws in list(clients):
            try:
                await ws.send(payload)
            except websockets.exceptions.ConnectionClosed:
                disconnected.add(ws)
        clients -= disconnected

    # ------------------------------------------------------------------ #
    # Heartbeat                                                            #
    # ------------------------------------------------------------------ #

    async def _heartbeat_loop(self) -> None:
        """
        Broadcast system status every 5 seconds.

        Z-score source (in priority order):
            1. last_real_z — injected from biosignal pipeline (always used if set)
            2. Development synthetic random walk (env='development' only)
               — clearly labelled as SYNTHETIC in the payload

        Production mode: heartbeat skips Z update if no real data is available.
        """
        while self.running:
            await asyncio.sleep(5)

            synthetic = False

            if self.last_real_z is not None:
                # Real data — use it
                self.current_z_score = self.last_real_z

            elif self.env == "development":
                # TODO(phase-2): Replace with real biosignal pipeline.
                # SYNTHETIC DATA — development only — never use in production.
                self.current_z_score = max(
                    0.0,
                    min(
                        12.0,
                        self.current_z_score + random.uniform(-0.2, 0.2),
                    ),
                )
                synthetic = True
                logger.debug(
                    "HEARTBEAT (SYNTHETIC Z=%.2f) — development mode only",
                    self.current_z_score,
                )
            else:
                # Production, no real data yet — skip Z broadcast
                continue

            payload = self._encode({
                "type": MESSAGE_TYPES["HEARTBEAT"],
                "z_score": self.current_z_score,
                "synthetic": synthetic,
                "client_counts": {
                    "core": len(self.core_clients),
                    "bridge": len(self.bridge_clients),
                    "overlay": len(self.overlay_clients),
                },
                "timestamp": _now(),
            })

            for clients in (
                self.core_clients, self.bridge_clients, self.overlay_clients
            ):
                await self._broadcast_to(clients, payload)

    # ------------------------------------------------------------------ #
    # Utilities                                                            #
    # ------------------------------------------------------------------ #

    @staticmethod
    def _encode(data: Dict[str, Any]) -> str:
        return json.dumps(data, default=str)


def _now() -> str:
    return datetime.now().isoformat()
