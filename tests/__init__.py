"""
GAIA Test Suite

Test structure:
- tests/core/        → Core Plane tests (Z-score, crisis detection)
- tests/bridge/      → Bridge Plane tests (alchemy, patterns)
- tests/overlay/     → Overlay Plane tests (avatar, memory)
- tests/integration/ → Full system integration tests

Run:
    pytest                    # All tests
    pytest tests/core/        # Core tests only
    pytest -m unit            # Unit tests only
    pytest -m "not slow"      # Skip slow tests
    pytest --cov=core         # With coverage
"""
