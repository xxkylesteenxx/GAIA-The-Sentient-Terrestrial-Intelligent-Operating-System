"""GAIA Core Plane - Foundation Layer.

The Core Plane enforces Order through invariant laws and immutable constraints.
This is the foundation of Factor 13 (Universal Love) - the binding force that
prevents Bad Chaos and Bad Order.

Key Modules:
- zscore: Consciousness coherence measurement (Factor 3: Vibration)
- safety: Crisis detection and intervention (Factor 13: Universal Love)
- audit: Universal Trace Ledger for tamper-evident history
- constants: Single source of truth for thresholds and values
"""

from core.constants import (
    # Z-Score Thresholds
    Z_CRISIS,
    Z_NIGREDO,
    Z_ALBEDO,
    Z_RUBEDO,
    Z_VIRIDITAS,
    Z_TRANSCENDENT,
    Z_MINIMUM,
    Z_MAX_VALUE,
    
    # Enums
    AlchemicalStage,
    CrisisLevel,
    EvidenceGrade,
    
    # Crisis Thresholds
    CRISIS_CRITICAL,
    CRISIS_HIGH,
    CRISIS_MODERATE,
)

# Import canonical implementations
from core.zscore.calculator import ZScoreCalculator, ZScoreResult
from core.safety.crisis_detector import CrisisDetector, CrisisAlert

__version__ = "0.1.1"  # Incremented after critical fixes

__all__ = [
    # Version
    "__version__",
    
    # Constants
    "Z_CRISIS",
    "Z_NIGREDO",
    "Z_ALBEDO",
    "Z_RUBEDO",
    "Z_VIRIDITAS",
    "Z_TRANSCENDENT",
    "Z_MINIMUM",
    "Z_MAX_VALUE",
    "CRISIS_CRITICAL",
    "CRISIS_HIGH",
    "CRISIS_MODERATE",
    
    # Enums
    "AlchemicalStage",
    "CrisisLevel",
    "EvidenceGrade",
    
    # Core Systems
    "ZScoreCalculator",
    "ZScoreResult",
    "CrisisDetector",
    "CrisisAlert",
]
