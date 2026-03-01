"""DEPRECATED: Legacy Z-Score Calculator.

This module is deprecated as of v0.1.1 (2026-02-28).
It has been replaced by core.zscore.calculator to resolve the Z formula split identity issue.

Please update your imports:
    OLD: from core.z_calculator import ZScoreCalculator
    NEW: from core.zscore.calculator import ZScoreCalculator

This file will be removed in v0.2.0.
"""

import warnings

# Re-export from canonical location with deprecation warning
from core.zscore.calculator import (
    ZScoreCalculator,
    ZScoreResult,
    calculate_z_score,
    BiosignalInput,
)

warnings.warn(
    "core.z_calculator is deprecated. Use core.zscore.calculator instead. "
    "This module will be removed in v0.2.0.",
    DeprecationWarning,
    stacklevel=2,
)

__all__ = [
    "ZScoreCalculator",
    "ZScoreResult",
    "calculate_z_score",
    "BiosignalInput",
]
