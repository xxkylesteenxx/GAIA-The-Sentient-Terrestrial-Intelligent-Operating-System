"""Canonical Z-Score Calculator - Single Source of Truth.

This is the ONLY implementation of the Z-score formula in the GAIA codebase.
All other modules MUST import from here.

Formula: Z₀ = 12 × √(C × F × B)

Where:
- C (Order): Shannon entropy normalized to [0, 1]
- F (Freedom): Lyapunov exponent normalized to [0, 1]
- B (Balance): Symmetry index normalized to [0, 1]

Geometric mean is used to ensure balanced development across all three components.
"""

import math
from dataclasses import dataclass
from typing import Optional

from core.constants import (
    Z_MAX_VALUE,
    Z_MINIMUM,
    Z_COMPONENT_MIN,
    Z_COMPONENT_MAX,
    AlchemicalStage,
    CrisisLevel,
)


@dataclass
class BiosignalInput:
    """Raw biosignal data for Z-score calculation.
    
    This is a placeholder structure. In Phase 2, this will include:
    - HRV data (ECG/PPG)
    - EEG power bands
    - Respiratory rate and variability
    - GSR (galvanic skin response)
    """
    # Text-based inference (Phase 1)
    text: Optional[str] = None
    
    # Biosignal data (Phase 2+)
    hrv_data: Optional[list[float]] = None
    eeg_data: Optional[dict[str, list[float]]] = None
    respiratory_data: Optional[list[float]] = None


@dataclass
class ZScoreResult:
    """Result of Z-score calculation with diagnostic information."""
    z_score: float
    order: float      # C component (0-1)
    freedom: float    # F component (0-1)
    balance: float    # B component (0-1)
    stage: AlchemicalStage
    crisis_level: CrisisLevel
    confidence: float = 1.0  # Confidence in measurement (0-1)
    source: str = "calculated"  # 'calculated', 'inferred', 'synthetic'

    def __post_init__(self):
        """Validate components are in valid range."""
        for component in [self.order, self.freedom, self.balance]:
            if not (Z_COMPONENT_MIN <= component <= Z_COMPONENT_MAX):
                raise ValueError(
                    f"Component {component} outside valid range [{Z_COMPONENT_MIN}, {Z_COMPONENT_MAX}]"
                )
        
        if not (Z_MINIMUM <= self.z_score <= Z_MAX_VALUE):
            raise ValueError(
                f"Z-score {self.z_score} outside valid range [{Z_MINIMUM}, {Z_MAX_VALUE}]"
            )


class ZScoreCalculator:
    """Canonical Z-Score calculator using geometric mean formula."""

    def __init__(self):
        """Initialize calculator."""
        self.formula = "geometric_mean"  # Z = 12 × √(C × F × B)

    def calculate(self, order: float, freedom: float, balance: float) -> ZScoreResult:
        """Calculate Z-score from three components.
        
        Args:
            order: Order component (Shannon entropy), 0-1
            freedom: Freedom component (Lyapunov), 0-1
            balance: Balance component (Symmetry), 0-1
        
        Returns:
            ZScoreResult with Z-score and diagnostic information
        
        Raises:
            ValueError: If any component is outside [0, 1]
        """
        # Validate inputs
        for name, value in [("order", order), ("freedom", freedom), ("balance", balance)]:
            if not (Z_COMPONENT_MIN <= value <= Z_COMPONENT_MAX):
                raise ValueError(
                    f"{name} component {value} outside valid range [{Z_COMPONENT_MIN}, {Z_COMPONENT_MAX}]"
                )
        
        # Geometric mean formula: Z = 12 × √(C × F × B)
        product = order * freedom * balance
        
        # Avoid domain error for sqrt of negative (shouldn't happen with validated inputs)
        if product < 0:
            product = 0
        
        geometric_mean = math.sqrt(product)
        z_score = Z_MAX_VALUE * geometric_mean
        
        # Clamp to valid range (defensive programming)
        z_score = max(Z_MINIMUM, min(Z_MAX_VALUE, z_score))
        
        # Determine stage and crisis level
        stage = AlchemicalStage.from_z_score(z_score)
        crisis_level = CrisisLevel.from_z_score(z_score)
        
        return ZScoreResult(
            z_score=z_score,
            order=order,
            freedom=freedom,
            balance=balance,
            stage=stage,
            crisis_level=crisis_level,
            confidence=1.0,
            source="calculated",
        )

    def calculate_from_biosignals(self, biosignals: BiosignalInput) -> ZScoreResult:
        """Calculate Z-score from raw biosignal data.
        
        Phase 1: Text-based inference (placeholder)
        Phase 2+: Real biosignal processing
        
        Args:
            biosignals: Raw biosignal data
        
        Returns:
            ZScoreResult
        """
        # Phase 1: Simple text-based inference
        if biosignals.text:
            return self._infer_from_text(biosignals.text)
        
        # Phase 2+: Real biosignal processing
        # TODO: Implement Shannon entropy from HRV
        # TODO: Implement Lyapunov from EEG
        # TODO: Implement symmetry from respiratory
        
        # Fallback: neutral state
        return self.calculate(
            order=0.6,
            freedom=0.6,
            balance=0.6,
        )

    def _infer_from_text(self, text: str) -> ZScoreResult:
        """Infer Z-score from text content (Phase 1 placeholder).
        
        This is a simplified heuristic. Real implementation in Phase 2 will use:
        - Sentiment analysis
        - Linguistic complexity metrics
        - Semantic coherence measures
        """
        text_lower = text.lower()
        
        # Crisis keywords
        crisis_keywords = ["suicide", "kill myself", "end it all", "can't go on", "hopeless"]
        if any(kw in text_lower for kw in crisis_keywords):
            return self.calculate(order=0.3, freedom=0.2, balance=0.2)
        
        # Distress keywords
        distress_keywords = ["anxious", "depressed", "overwhelmed", "stressed", "worried"]
        if any(kw in text_lower for kw in distress_keywords):
            return self.calculate(order=0.5, freedom=0.4, balance=0.5)
        
        # Positive keywords
        positive_keywords = ["grateful", "peaceful", "joyful", "centered", "flow", "clear"]
        if any(kw in text_lower for kw in positive_keywords):
            return self.calculate(order=0.8, freedom=0.7, balance=0.8)
        
        # Neutral
        result = self.calculate(order=0.6, freedom=0.6, balance=0.6)
        result.confidence = 0.5  # Low confidence for text inference
        result.source = "inferred"
        return result


# Convenience function for quick calculations
def calculate_z_score(order: float, freedom: float, balance: float) -> float:
    """Calculate Z-score from components (returns float only)."""
    calculator = ZScoreCalculator()
    result = calculator.calculate(order, freedom, balance)
    return result.z_score
