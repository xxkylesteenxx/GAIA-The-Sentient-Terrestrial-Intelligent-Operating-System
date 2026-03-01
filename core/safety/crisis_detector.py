"""Canonical Crisis Detector - Factor 13 Protection.

This is the ONLY implementation of crisis detection in the GAIA codebase.
All other modules MUST import from here.

Factor 13: Universal Love - The binding force that ensures:
- No Bad Chaos (harm to self or others)
- No Bad Order (oppression, control)
- Prosocial cooperation enforced at all scales
"""

from dataclasses import dataclass
from datetime import datetime
from enum import Enum
from typing import Optional

from core.constants import (
    CRISIS_CRITICAL,
    CRISIS_HIGH,
    CRISIS_MODERATE,
    CrisisLevel,
)


@dataclass
class CrisisAlert:
    """Crisis detection result with intervention guidance."""
    level: CrisisLevel
    z_score: float
    timestamp: datetime
    message: str
    intervention_required: bool
    resources: list[str]
    
    def __post_init__(self):
        """Populate resources based on crisis level."""
        if self.intervention_required and not self.resources:
            # Default critical resources
            self.resources = [
                "988 Suicide & Crisis Lifeline (US): call or text 988",
                "Crisis Text Line: Text HOME to 741741",
                "International Association for Suicide Prevention: https://www.iasp.info/resources/Crisis_Centres/",
            ]


class CrisisDetector:
    """Canonical crisis detector using thresholds from core.constants."""

    def __init__(self):
        """Initialize detector with canonical thresholds."""
        self.critical_threshold = CRISIS_CRITICAL  # 1.0
        self.high_threshold = CRISIS_HIGH          # 3.0
        self.moderate_threshold = CRISIS_MODERATE  # 6.0

    def detect(self, z_score: float) -> CrisisAlert:
        """Detect crisis level from Z-score.
        
        Args:
            z_score: Current Z coherence score (0-12)
        
        Returns:
            CrisisAlert with level, message, and resources
        """
        level = CrisisLevel.from_z_score(z_score)
        timestamp = datetime.utcnow()
        
        if level == CrisisLevel.CRITICAL:
            return CrisisAlert(
                level=level,
                z_score=z_score,
                timestamp=timestamp,
                message=(
                    "CRITICAL: Z-score indicates severe distress. "
                    "Immediate support recommended. You are not alone."
                ),
                intervention_required=True,
                resources=[],  # Will be populated by __post_init__
            )
        
        elif level == CrisisLevel.HIGH:
            return CrisisAlert(
                level=level,
                z_score=z_score,
                timestamp=timestamp,
                message=(
                    "HIGH: Z-score indicates elevated distress. "
                    "Consider reaching out to support resources."
                ),
                intervention_required=False,
                resources=[
                    "SAMHSA National Helpline: 1-800-662-4357",
                    "Mental Health America: https://www.mhanational.org/finding-help",
                ],
            )
        
        elif level == CrisisLevel.MODERATE:
            return CrisisAlert(
                level=level,
                z_score=z_score,
                timestamp=timestamp,
                message=(
                    "MODERATE: Z-score in watchful range. "
                    "Gentle self-care and rest recommended."
                ),
                intervention_required=False,
                resources=[
                    "Self-care practices: meditation, nature, connection",
                    "7 Cups (online emotional support): https://www.7cups.com/",
                ],
            )
        
        else:  # NORMAL
            return CrisisAlert(
                level=level,
                z_score=z_score,
                timestamp=timestamp,
                message="Z-score indicates healthy coherence. Continue thriving.",
                intervention_required=False,
                resources=[],
            )

    def check_threshold(self, z_score: float) -> bool:
        """Quick check: does Z-score cross any crisis threshold?
        
        Returns:
            True if Z < CRISIS_MODERATE (requires monitoring)
        """
        return z_score < self.moderate_threshold

    def requires_intervention(self, z_score: float) -> bool:
        """Check if immediate intervention is required.
        
        Returns:
            True if Z < CRISIS_CRITICAL (display 988, emergency protocols)
        """
        return z_score < self.critical_threshold
