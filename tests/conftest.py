"""
Pytest Configuration

Shared fixtures and test markers for all GAIA tests.

Markers:
- unit: Fast unit tests (<100ms)
- integration: Integration tests (require services)
- slow: Slow tests (>1s, WebSocket, network)
- wip: Work in progress (skip in CI)

Usage:
    # Fast tests only
    pytest -m "not slow"
    
    # Unit tests only
    pytest -m unit
    
    # Everything
    pytest
"""

import pytest


# ---------------------------------------------------------------------------
# Pytest Configuration
# ---------------------------------------------------------------------------


def pytest_configure(config):
    """Register custom markers."""
    config.addinivalue_line(
        "markers",
        "unit: Fast unit tests (pure functions, no I/O)"
    )
    config.addinivalue_line(
        "markers",
        "integration: Integration tests (require services, databases, network)"
    )
    config.addinivalue_line(
        "markers",
        "slow: Slow tests (>1 second, async, WebSocket)"
    )
    config.addinivalue_line(
        "markers",
        "wip: Work in progress (skip in CI)"
    )


def pytest_collection_modifyitems(config, items):
    """
    Auto-mark tests based on their characteristics.
    
    Rules:
    - Tests with 'asyncio' marker → mark as 'slow'
    - Tests in test_websocket_api.py → mark as 'integration' and 'slow'
    - Tests with 'websocket' in name → mark as 'slow'
    """
    for item in items:
        # Mark all asyncio tests as slow (WebSocket integration)
        if 'asyncio' in item.keywords:
            item.add_marker(pytest.mark.slow)
        
        # Mark WebSocket tests as integration + slow
        if 'test_websocket_api' in str(item.fspath):
            item.add_marker(pytest.mark.integration)
            item.add_marker(pytest.mark.slow)
        
        # Mark tests with 'websocket' in name as slow
        if 'websocket' in item.name.lower():
            item.add_marker(pytest.mark.slow)


# ---------------------------------------------------------------------------
# Asyncio Configuration
# ---------------------------------------------------------------------------

# pytest-asyncio configuration
pytest_plugins = ('pytest_asyncio',)


@pytest.fixture(scope="session")
def event_loop_policy():
    """Use default asyncio event loop policy."""
    import asyncio
    return asyncio.get_event_loop_policy()
