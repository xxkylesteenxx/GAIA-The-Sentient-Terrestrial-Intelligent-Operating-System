"""
GAIA Core Plane

Canonical exports for consciousness measurement and safety enforcement.

Usage::

    from core import ZScoreCalculator, CrisisDetector
    from core.constants import Z_CRISIS_CRITICAL, FACTOR_13_CONSTANT
"""

# Constants (single source of truth)
from core.constants import *  # noqa: F401, F403

# Z-Score Calculator (Factor 3 - Vibration)
from core.zscore.calculator import ZScoreCalculator  # noqa: F401

# Crisis Detection (Factor 13 - Universal Love)
from core.safety.crisis_detector import (
    CrisisDetector,  # noqa: F401
    CrisisLevel,     # noqa: F401
)

__all__ = [
    "ZScoreCalculator",
    "CrisisDetector",
    "CrisisLevel",
]
