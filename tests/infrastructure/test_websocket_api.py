"""
WebSocket API Tests
Tests for infrastructure/api/websocket_server.py

Constructor fix applied:
    OLD (broken): GAIAWebSocketServer()  — no params, TypeError on host/port
    NEW (correct): GAIAWebSocketServer(host='127.0.0.1', core_port=8765)

All tests use development mode so the heartbeat random walk is active
without requiring real biosignal data.
"""

from __future__ import annotations

import asyncio
import json
import pytest
import websockets

from infrastructure.api.websocket_server import GAIAWebSocketServer


# ---------------------------------------------------------------------------
# Fixtures
# ---------------------------------------------------------------------------

TEST_HOST = "127.0.0.1"
TEST_CORE_PORT = 19765       # Offset from defaults to avoid port conflicts in CI
TEST_BRIDGE_PORT = 19766
TEST_OVERLAY_PORT = 19767


@pytest.fixture
def server() -> GAIAWebSocketServer:
    """Return a configured test server (not started)."""
    return GAIAWebSocketServer(
        host=TEST_HOST,
        core_port=TEST_CORE_PORT,
        bridge_port=TEST_BRIDGE_PORT,
        overlay_port=TEST_OVERLAY_PORT,
        env="development",   # Enable synthetic Z-score for tests
    )


@pytest.fixture
async def running_server(server: GAIAWebSocketServer):
    """Start the server, yield it, then stop it."""
    task = asyncio.create_task(server.start())
    await asyncio.sleep(0.1)   # Let the server bind before tests run

    yield server

    server.running = False
    task.cancel()
    try:
        await task
    except asyncio.CancelledError:
        pass


# ---------------------------------------------------------------------------
# Constructor tests (the original failure point)
# ---------------------------------------------------------------------------


class TestConstructor:
    def test_constructor_defaults(self) -> None:
        """Constructor must work with no arguments."""
        s = GAIAWebSocketServer()
        assert s.host == "localhost"
        assert s.core_port == 8765
        assert s.bridge_port == 8766
        assert s.overlay_port == 8767
        assert s.env == "production"

    def test_constructor_custom_host_and_port(self) -> None:
        """Constructor must accept host and port kwargs."""
        s = GAIAWebSocketServer(host="127.0.0.1", core_port=TEST_CORE_PORT)
        assert s.host == "127.0.0.1"
        assert s.core_port == TEST_CORE_PORT

    def test_constructor_all_ports(self) -> None:
        s = GAIAWebSocketServer(
            host=TEST_HOST,
            core_port=TEST_CORE_PORT,
            bridge_port=TEST_BRIDGE_PORT,
            overlay_port=TEST_OVERLAY_PORT,
        )
        assert s.bridge_port == TEST_BRIDGE_PORT
        assert s.overlay_port == TEST_OVERLAY_PORT

    def test_constructor_env_development(self) -> None:
        s = GAIAWebSocketServer(env="development")
        assert s.env == "development"

    def test_initial_state(self) -> None:
        s = GAIAWebSocketServer()
        assert s.current_z_score == 6.0       # Albedo — neutral start
        assert s.last_real_z is None
        assert not s.running


# ---------------------------------------------------------------------------
# inject_z_score tests
# ---------------------------------------------------------------------------


class TestInjectZScore:
    def test_inject_sets_current_z(self, server: GAIAWebSocketServer) -> None:
        server.inject_z_score(8.5)
        assert server.current_z_score == 8.5
        assert server.last_real_z == 8.5

    def test_inject_clamps_not_enforced_here(self, server: GAIAWebSocketServer) -> None:
        """inject_z_score trusts its caller; clamping is in ZScoreCalculator."""
        server.inject_z_score(11.999)
        assert server.current_z_score == 11.999

    def test_inject_overwrites_previous(self, server: GAIAWebSocketServer) -> None:
        server.inject_z_score(3.0)
        server.inject_z_score(9.5)
        assert server.current_z_score == 9.5


# ---------------------------------------------------------------------------
# WebSocket connection tests (integration — requires running server)
# ---------------------------------------------------------------------------


@pytest.mark.asyncio
class TestCoreConnection:
    async def test_core_sends_status_on_connect(
        self, running_server: GAIAWebSocketServer
    ) -> None:
        uri = f"ws://{TEST_HOST}:{TEST_CORE_PORT}"
        async with websockets.connect(uri) as ws:
            raw = await asyncio.wait_for(ws.recv(), timeout=2.0)
            msg = json.loads(raw)

        assert msg["type"] == "system_status"
        assert msg["plane"] == "core"
        assert "z_score" in msg
        assert "timestamp" in msg

    async def test_core_registers_client(
        self, running_server: GAIAWebSocketServer
    ) -> None:
        uri = f"ws://{TEST_HOST}:{TEST_CORE_PORT}"
        async with websockets.connect(uri) as ws:
            await asyncio.wait_for(ws.recv(), timeout=2.0)
            assert len(running_server.core_clients) == 1
        # After disconnect
        await asyncio.sleep(0.05)
        assert len(running_server.core_clients) == 0

    async def test_text_input_returns_z_update(
        self, running_server: GAIAWebSocketServer
    ) -> None:
        uri = f"ws://{TEST_HOST}:{TEST_CORE_PORT}"
        async with websockets.connect(uri) as ws:
            # Consume welcome message
            await asyncio.wait_for(ws.recv(), timeout=2.0)

            await ws.send(json.dumps({
                "type": "text_input",
                "text": "I feel amazing and grateful today!",
            }))
            raw = await asyncio.wait_for(ws.recv(), timeout=2.0)
            msg = json.loads(raw)

        assert msg["type"] == "z_score_update"
        assert "z_score" in msg
        assert 0.0 <= msg["z_score"] <= 12.0
        assert "stage" in msg
        assert "components" in msg

    async def test_invalid_json_returns_error(
        self, running_server: GAIAWebSocketServer
    ) -> None:
        uri = f"ws://{TEST_HOST}:{TEST_CORE_PORT}"
        async with websockets.connect(uri) as ws:
            await asyncio.wait_for(ws.recv(), timeout=2.0)

            await ws.send("this is not json {{{")
            raw = await asyncio.wait_for(ws.recv(), timeout=2.0)
            msg = json.loads(raw)

        assert msg["type"] == "error"


@pytest.mark.asyncio
class TestBridgeConnection:
    async def test_bridge_sends_status_on_connect(
        self, running_server: GAIAWebSocketServer
    ) -> None:
        uri = f"ws://{TEST_HOST}:{TEST_BRIDGE_PORT}"
        async with websockets.connect(uri) as ws:
            raw = await asyncio.wait_for(ws.recv(), timeout=2.0)
            msg = json.loads(raw)

        assert msg["type"] == "system_status"
        assert msg["plane"] == "bridge"


@pytest.mark.asyncio
class TestOverlayConnection:
    async def test_overlay_sends_status_on_connect(
        self, running_server: GAIAWebSocketServer
    ) -> None:
        uri = f"ws://{TEST_HOST}:{TEST_OVERLAY_PORT}"
        async with websockets.connect(uri) as ws:
            raw = await asyncio.wait_for(ws.recv(), timeout=2.0)
            msg = json.loads(raw)

        assert msg["type"] == "system_status"
        assert msg["plane"] == "overlay"


# ---------------------------------------------------------------------------
# Crisis alert tests
# ---------------------------------------------------------------------------


@pytest.mark.asyncio
class TestCrisisAlerts:
    async def test_crisis_keywords_trigger_alert(
        self, running_server: GAIAWebSocketServer
    ) -> None:
        uri = f"ws://{TEST_HOST}:{TEST_CORE_PORT}"
        async with websockets.connect(uri) as ws:
            await asyncio.wait_for(ws.recv(), timeout=2.0)  # welcome

            await ws.send(json.dumps({
                "type": "text_input",
                "text": "I want to kill myself and end my life.",
            }))

            # First message is the Z update
            z_msg_raw = await asyncio.wait_for(ws.recv(), timeout=2.0)
            z_msg = json.loads(z_msg_raw)
            assert z_msg["type"] == "z_score_update"

            # Second message should be crisis alert
            alert_raw = await asyncio.wait_for(ws.recv(), timeout=2.0)
            alert = json.loads(alert_raw)

        assert alert["type"] == "crisis_alert"
        assert alert["requires_emergency"] is True
        assert "988" in str(alert["resources"])

    async def test_non_crisis_text_no_alert(
        self, running_server: GAIAWebSocketServer
    ) -> None:
        uri = f"ws://{TEST_HOST}:{TEST_CORE_PORT}"
        async with websockets.connect(uri) as ws:
            await asyncio.wait_for(ws.recv(), timeout=2.0)

            await ws.send(json.dumps({
                "type": "text_input",
                "text": "I feel great today! Really energised.",
            }))

            raw = await asyncio.wait_for(ws.recv(), timeout=2.0)
            msg = json.loads(raw)

        # Should be Z update, not crisis alert
        assert msg["type"] == "z_score_update"


# ---------------------------------------------------------------------------
# Heartbeat tests
# ---------------------------------------------------------------------------


@pytest.mark.asyncio
class TestHeartbeat:
    async def test_heartbeat_fires_in_development_mode(
        self, running_server: GAIAWebSocketServer
    ) -> None:
        """Development mode heartbeat should broadcast within 6 seconds."""
        uri = f"ws://{TEST_HOST}:{TEST_CORE_PORT}"
        async with websockets.connect(uri) as ws:
            # Consume welcome
            await asyncio.wait_for(ws.recv(), timeout=2.0)

            # Wait for heartbeat (fires every 5s)
            raw = await asyncio.wait_for(ws.recv(), timeout=7.0)
            msg = json.loads(raw)

        assert msg["type"] == "heartbeat"
        assert "z_score" in msg
        assert msg["synthetic"] is True   # development mode → synthetic

    async def test_heartbeat_uses_real_z_when_injected(
        self, running_server: GAIAWebSocketServer
    ) -> None:
        running_server.inject_z_score(9.5)

        uri = f"ws://{TEST_HOST}:{TEST_CORE_PORT}"
        async with websockets.connect(uri) as ws:
            await asyncio.wait_for(ws.recv(), timeout=2.0)

            raw = await asyncio.wait_for(ws.recv(), timeout=7.0)
            msg = json.loads(raw)

        assert msg["type"] == "heartbeat"
        # Real Z was injected; should not be marked synthetic
        assert msg["synthetic"] is False
        # Z should be close to 9.5 (heartbeat reads last_real_z)
        assert abs(msg["z_score"] - 9.5) < 0.5
