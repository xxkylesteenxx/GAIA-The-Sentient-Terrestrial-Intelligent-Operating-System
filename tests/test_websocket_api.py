"""Tests for WebSocket API Server."""

import pytest
import asyncio
import websockets
import json
from infrastructure.api.websocket_server import GAIAWebSocketServer


class TestWebSocketAPI:
    """Test WebSocket server functionality."""
    
    @pytest.fixture
    async def server(self):
        """Create test server instance."""
        server = GAIAWebSocketServer(host='127.0.0.1', port=8765)
        # Start server in background
        server_task = asyncio.create_task(server.start())
        await asyncio.sleep(0.1)  # Let server start
        
        yield server
        
        # Cleanup
        server_task.cancel()
        try:
            await server_task
        except asyncio.CancelledError:
            pass
    
    @pytest.mark.asyncio
    async def test_connection(self, server):
        """Test WebSocket connection establishment."""
        async with websockets.connect('ws://127.0.0.1:8765') as ws:
            assert ws.open
    
    @pytest.mark.asyncio
    async def test_ping_pong(self, server):
        """Test ping/pong health check."""
        async with websockets.connect('ws://127.0.0.1:8765') as ws:
            await ws.send(json.dumps({'type': 'ping'}))
            response = await ws.recv()
            data = json.loads(response)
            assert data['type'] == 'pong'
    
    @pytest.mark.asyncio
    async def test_z_score_calculation(self, server):
        """Test Z-score calculation via WebSocket."""
        async with websockets.connect('ws://127.0.0.1:8765') as ws:
            message = {
                'type': 'calculate_z_score',
                'time_series': [0.5] * 100,
                'positive': 5.0,
                'negative': 1.0
            }
            await ws.send(json.dumps(message))
            response = await ws.recv()
            data = json.loads(response)
            
            assert data['type'] == 'z_score_result'
            assert 'z_score' in data
            assert 'state' in data
    
    @pytest.mark.asyncio
    async def test_crisis_detection(self, server):
        """Test crisis detection via WebSocket."""
        async with websockets.connect('ws://127.0.0.1:8765') as ws:
            message = {
                'type': 'check_crisis',
                'z_score': 2.0,
                'text': 'I feel hopeless'
            }
            await ws.send(json.dumps(message))
            response = await ws.recv()
            data = json.loads(response)
            
            assert data['type'] == 'crisis_alert'
            assert data['level'] in ['HIGH', 'MODERATE']
            assert data['requires_intervention'] is True
