"""
DEPRECATED — DO NOT USE DIRECTLY.

This module is retained only to prevent ImportError during migration.
All code MUST migrate to:

    from core.zscore.calculator import ZScoreCalculator

This shim will be removed in v0.2.0.
"""

import warnings

warnings.warn(
    "core.z_calculator is deprecated. "
    "Import from core.zscore.calculator instead. "
    "This shim will be removed in v0.2.0.",
    DeprecationWarning,
    stacklevel=2,
)

# Re-export so existing imports don't break immediately.
from core.zscore.calculator import ZScoreCalculator  # noqa: F401, E402

# These dataclasses existed in the old module.
# We provide minimal compatibility stubs.
from dataclasses import dataclass
from datetime import datetime
from typing import Optional
import numpy as np


@dataclass
class BiosignalData:
    """
    Compatibility stub — use core.zscore.calculator.ZScoreCalculator directly.
    Pass numpy arrays to analyze_system() instead.
    """
    hrv: Optional[np.ndarray] = None
    eeg: Optional[np.ndarray] = None
    respiratory: Optional[np.ndarray] = None
    timestamp: Optional[datetime] = None

    def __post_init__(self) -> None:
        if self.timestamp is None:
            self.timestamp = datetime.now()


@dataclass
class ZScoreComponents:
    """Compatibility stub — analyze_system() returns a plain dict now."""
    c_order: float
    f_freedom: float
    b_balance: float
    z_score: float
    timestamp: datetime

    def __str__(self) -> str:
        return (
            f"Z Score: {self.z_score:.2f}\n"
            f"  C (Coherence): {self.c_order:.3f}\n"
            f"  F (Fidelity):  {self.f_freedom:.3f}\n"
            f"  B (Balance):   {self.b_balance:.3f}"
        )
