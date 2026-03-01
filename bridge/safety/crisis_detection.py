"""DEPRECATED: Legacy Crisis Detection.

This module is deprecated as of v0.1.1 (2026-02-28).
It has been replaced by core.safety.crisis_detector to resolve threshold conflicts.

Please update your imports:
    OLD: from bridge.safety.crisis_detection import CrisisDetector
    NEW: from core.safety.crisis_detector import CrisisDetector

This file will be removed in v0.2.0.
"""

import warnings
from dataclasses import dataclass
from enum import Enum

# Re-export from canonical location
from core.safety.crisis_detector import (
    CrisisDetector,
    CrisisAlert,
)

warnings.warn(
    "bridge.safety.crisis_detection is deprecated. Use core.safety.crisis_detector instead. "
    "This module will be removed in v0.2.0.",
    DeprecationWarning,
    stacklevel=2,
)

# Legacy dataclasses for backward compatibility (stubs only)
@dataclass
class CrisisEvent:
    """DEPRECATED: Use core.safety.crisis_detector.CrisisAlert instead."""
    level: str
    timestamp: str
    
    def __post_init__(self):
        warnings.warn(
            "CrisisEvent is deprecated. Use CrisisAlert from core.safety.crisis_detector.",
            DeprecationWarning,
            stacklevel=2,
        )


class CrisisLevel(Enum):
    """DEPRECATED: Use core.constants.CrisisLevel instead."""
    CRITICAL = "critical"
    WARNING = "warning"
    
    def __init__(self, *args, **kwargs):
        warnings.warn(
            "bridge.safety.crisis_detection.CrisisLevel is deprecated. "
            "Use core.constants.CrisisLevel instead.",
            DeprecationWarning,
            stacklevel=2,
        )


__all__ = [
    "CrisisDetector",
    "CrisisAlert",
    "CrisisEvent",  # Deprecated
    "CrisisLevel",  # Deprecated
]
