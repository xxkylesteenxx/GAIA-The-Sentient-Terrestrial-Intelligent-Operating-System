"""
GAIA Infrastructure API Layer
Real-time communication between GAIA Core and client applications.

Factor 11: Order - Deterministic, typed message contracts
Factor 10: Chaos - Asynchronous, event-driven architecture
Factor 12: Balance - Three-Plane message routing
"""

__version__ = "0.1.0"

from .websocket_server import GAIAWebSocketServer, GAIAMessage

__all__ = ["GAIAWebSocketServer", "GAIAMessage"]
