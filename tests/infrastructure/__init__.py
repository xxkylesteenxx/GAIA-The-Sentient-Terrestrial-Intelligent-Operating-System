"""
Infrastructure Tests

Tests for infrastructure layer:
- infrastructure/api/websocket_server.py (3-port WebSocket server)
- infrastructure/biosignals/           (real-time signal processing)
- infrastructure/storage/              (persistent data storage)

Note:
- WebSocket tests use offset ports (19765+) to avoid CI conflicts
- Development mode enables testing without real biosignals
- Async tests use pytest-asyncio
"""
