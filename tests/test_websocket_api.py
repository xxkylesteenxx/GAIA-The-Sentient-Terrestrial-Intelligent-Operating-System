"""Test WebSocket API.

Validates fixes for:
- CRITICAL-3: WebSocket constructor mismatch
- MINOR-2: Heartbeat production mode
"""

import pytest
import asyncio
from infrastructure.api.websocket_server import GAIAWebSocketServer, HeartbeatMessage


class TestWebSocketConstructor:
    """Test WebSocket server initialization."""

    def test_constructor_accepts_parameters(self):
        """Constructor should accept host and port parameters."""
        server = GAIAWebSocketServer(
            host='127.0.0.1',
            core_port=19765,
            bridge_port=19766,
            overlay_port=19767,
            env='development',
        )
        
        assert server.host == '127.0.0.1'
        assert server.core_port == 19765
        assert server.bridge_port == 19766
        assert server.overlay_port == 19767
        assert server.env == 'development'

    def test_default_parameters(self):
        """Constructor should use sensible defaults."""
        server = GAIAWebSocketServer()
        
        assert server.host == 'localhost'
        assert server.core_port == 8765
        assert server.bridge_port == 8766
        assert server.overlay_port == 8767
        assert server.env == 'production'


class TestEnvironmentMode:
    """Test development vs production mode."""

    @pytest.mark.asyncio
    async def test_development_mode_synthetic_z(self):
        """Development mode should generate synthetic Z-scores."""
        server = GAIAWebSocketServer(env='development')
        
        heartbeat = await server._generate_heartbeat()
        assert heartbeat is not None
        assert heartbeat.synthetic is True
        assert 0 <= heartbeat.z_score <= 12

    @pytest.mark.asyncio
    async def test_production_mode_requires_injection(self):
        """Production mode should require Z-score injection."""
        server = GAIAWebSocketServer(env='production')
        
        # No Z-score injected yet
        heartbeat = await server._generate_heartbeat()
        assert heartbeat is None
        
        # Inject Z-score
        server.inject_z_score(7.5)
        heartbeat = await server._generate_heartbeat()
        assert heartbeat is not None
        assert heartbeat.z_score == 7.5
        assert heartbeat.synthetic is False

    def test_inject_z_score_validation(self):
        """inject_z_score should validate range [0, 12]."""
        server = GAIAWebSocketServer()
        
        # Valid
        server.inject_z_score(6.5)
        assert server.current_z_score == 6.5
        
        # Invalid: too low
        with pytest.raises(ValueError, match="outside valid range"):
            server.inject_z_score(-1.0)
        
        # Invalid: too high
        with pytest.raises(ValueError, match="outside valid range"):
            server.inject_z_score(15.0)


class TestClientManagement:
    """Test client connection management."""

    def test_client_sets_initialized(self):
        """Server should initialize empty client sets."""
        server = GAIAWebSocketServer()
        
        assert len(server.core_clients) == 0
        assert len(server.bridge_clients) == 0
        assert len(server.overlay_clients) == 0
