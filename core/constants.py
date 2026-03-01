"""Core constants for GAIA system.

This module serves as the single source of truth for:
- Z-score thresholds (alchemical stages)
- Crisis detection levels
- System-wide numerical constants

All other modules MUST import these values - no hard-coded thresholds allowed.
"""

from enum import Enum
from typing import Final

# =============================================================================
# Z-SCORE THRESHOLDS (Alchemical Stages)
# =============================================================================
# These define the boundaries between consciousness states.
# Each stage has a 2-point range for equal distribution across Z ∈ [0, 12].

Z_CRISIS: Final[float] = 2.0       # Below this: crisis intervention required
Z_NIGREDO: Final[float] = 4.0      # Shadow work, integration phase
Z_ALBEDO: Final[float] = 6.0       # Purification, clarity emerging
Z_RUBEDO: Final[float] = 8.0       # Reddening, unified self
Z_VIRIDITAS: Final[float] = 10.0   # Greening, flourishing life
Z_TRANSCENDENT: Final[float] = 12.0  # Maximum coherence

# Minimum viable Z score (theoretical floor)
Z_MINIMUM: Final[float] = 0.0


class AlchemicalStage(Enum):
    """Consciousness transformation stages."""
    CRISIS = "crisis"           # Z < 2: Immediate support needed
    NIGREDO = "nigredo"         # Z 2-4: Shadow integration
    ALBEDO = "albedo"           # Z 4-6: Purification
    RUBEDO = "rubedo"           # Z 6-8: Unification
    VIRIDITAS = "viriditas"     # Z 8-10: Flourishing
    TRANSCENDENT = "transcendent"  # Z 10-12: Peak states

    @classmethod
    def from_z_score(cls, z: float) -> "AlchemicalStage":
        """Determine alchemical stage from Z score."""
        if z < Z_CRISIS:
            return cls.CRISIS
        elif z < Z_NIGREDO:
            return cls.NIGREDO
        elif z < Z_ALBEDO:
            return cls.ALBEDO
        elif z < Z_RUBEDO:
            return cls.RUBEDO
        elif z < Z_VIRIDITAS:
            return cls.VIRIDITAS
        else:
            return cls.TRANSCENDENT


# =============================================================================
# CRISIS DETECTION THRESHOLDS
# =============================================================================
# Factor 13 (Universal Love) enforcement levels

CRISIS_CRITICAL: Final[float] = 1.0    # Z < 1.0: CRITICAL - immediate intervention
CRISIS_HIGH: Final[float] = 3.0        # Z < 3.0: HIGH - elevated monitoring
CRISIS_MODERATE: Final[float] = 6.0    # Z < 6.0: MODERATE - watchful awareness


class CrisisLevel(Enum):
    """Crisis severity levels for Factor 13 protection."""
    CRITICAL = "critical"    # Immediate intervention (988, emergency protocols)
    HIGH = "high"            # Elevated support (daily check-ins, resources)
    MODERATE = "moderate"    # Watchful awareness (gentle monitoring)
    NORMAL = "normal"        # Thriving state

    @classmethod
    def from_z_score(cls, z: float) -> "CrisisLevel":
        """Determine crisis level from Z score."""
        if z < CRISIS_CRITICAL:
            return cls.CRITICAL
        elif z < CRISIS_HIGH:
            return cls.HIGH
        elif z < CRISIS_MODERATE:
            return cls.MODERATE
        else:
            return cls.NORMAL


# =============================================================================
# FORMULA COMPONENTS
# =============================================================================
# Z = 12 × √(C × F × B) where:
#   C = Order (Shannon entropy, 0-1)
#   F = Freedom (Lyapunov exponent normalized, 0-1)
#   B = Balance (Symmetry index, 0-1)

Z_MAX_VALUE: Final[float] = 12.0
Z_COMPONENT_MIN: Final[float] = 0.0
Z_COMPONENT_MAX: Final[float] = 1.0

# Geometric mean is used to penalize any single component being low
# This prevents "gaming" by maximizing one component while ignoring others
USE_GEOMETRIC_MEAN: Final[bool] = True


# =============================================================================
# EVIDENCE GRADES (STEM Standards)
# =============================================================================

class EvidenceGrade(Enum):
    """Evidence quality levels for STEM validation."""
    E0 = "hypothesis"        # Speculation, metaphor only
    E1 = "theoretical"       # Mathematical model, not validated
    E2 = "specified"         # Operational definition, not calibrated
    E3 = "validated"         # Calibrated with golden dataset
    E4 = "peer_reviewed"     # Published, replicated
    E5 = "physical_law"      # SI units, N≥30, p<0.05


# Current evidence grade for Z formula
Z_FORMULA_EVIDENCE_GRADE = EvidenceGrade.E2  # Specified but not calibrated
