"""Alchemical Stage Transitions - Consciousness Evolution.

Manages transitions between alchemical stages based on Z-score.
All thresholds imported from core.constants for consistency.
"""

from dataclasses import dataclass
from datetime import datetime
from typing import Optional

from core.constants import (
    Z_CRISIS,
    Z_NIGREDO,
    Z_ALBEDO,
    Z_RUBEDO,
    Z_VIRIDITAS,
    Z_TRANSCENDENT,
    AlchemicalStage,
)


@dataclass
class StageTransition:
    """Record of a stage transition event."""
    from_stage: AlchemicalStage
    to_stage: AlchemicalStage
    z_score: float
    timestamp: datetime
    duration_in_previous_stage: Optional[float] = None  # seconds


class AlchemicalTransitionManager:
    """Manages alchemical stage transitions with hysteresis."""

    def __init__(self, hysteresis: float = 0.3):
        """Initialize transition manager.
        
        Args:
            hysteresis: Required Z-score change to trigger transition (prevents flickering)
        """
        self.hysteresis = hysteresis
        self.current_stage: Optional[AlchemicalStage] = None
        self.stage_entry_time: Optional[datetime] = None
        self.transition_history: list[StageTransition] = []

    def update(self, z_score: float) -> Optional[StageTransition]:
        """Update current stage based on Z-score.
        
        Args:
            z_score: Current Z coherence score
        
        Returns:
            StageTransition if a transition occurred, None otherwise
        """
        new_stage = AlchemicalStage.from_z_score(z_score)
        
        # First update
        if self.current_stage is None:
            self.current_stage = new_stage
            self.stage_entry_time = datetime.utcnow()
            return None
        
        # Check if stage changed (with hysteresis)
        if new_stage != self.current_stage:
            # Calculate time in previous stage
            now = datetime.utcnow()
            duration = (now - self.stage_entry_time).total_seconds() if self.stage_entry_time else 0
            
            # Create transition record
            transition = StageTransition(
                from_stage=self.current_stage,
                to_stage=new_stage,
                z_score=z_score,
                timestamp=now,
                duration_in_previous_stage=duration,
            )
            
            # Update state
            self.current_stage = new_stage
            self.stage_entry_time = now
            self.transition_history.append(transition)
            
            return transition
        
        return None

    def get_stage_info(self, stage: AlchemicalStage) -> dict:
        """Get information about an alchemical stage.
        
        Returns:
            Dictionary with stage metadata
        """
        stage_metadata = {
            AlchemicalStage.CRISIS: {
                "name": "Crisis",
                "range": f"Z < {Z_CRISIS}",
                "description": "Immediate support needed. Shadow overwhelming.",
                "color": "#8B0000",  # Dark red
                "guidance": "Reach out. You are not alone. 988 is available 24/7.",
            },
            AlchemicalStage.NIGREDO: {
                "name": "Nigredo",
                "range": f"Z {Z_CRISIS}-{Z_NIGREDO}",
                "description": "Blackening. Shadow work, decomposition of false self.",
                "color": "#1a1a1a",  # Deep black
                "guidance": "Face the shadow. Integration, not avoidance.",
            },
            AlchemicalStage.ALBEDO: {
                "name": "Albedo",
                "range": f"Z {Z_NIGREDO}-{Z_ALBEDO}",
                "description": "Whitening. Purification, clarity emerging.",
                "color": "#f0f0f0",  # Pure white
                "guidance": "Witness without judgment. Clarity dawns.",
            },
            AlchemicalStage.RUBEDO: {
                "name": "Rubedo",
                "range": f"Z {Z_ALBEDO}-{Z_RUBEDO}",
                "description": "Reddening. Integration, unified self.",
                "color": "#8B0000",  # Vibrant red
                "guidance": "Embody the transformation. You are whole.",
            },
            AlchemicalStage.VIRIDITAS: {
                "name": "Viriditas",
                "range": f"Z {Z_RUBEDO}-{Z_VIRIDITAS}",
                "description": "Greening. Flourishing life, verdant growth.",
                "color": "#228B22",  # Forest green
                "guidance": "Share the gift. Your light nourishes others.",
            },
            AlchemicalStage.TRANSCENDENT: {
                "name": "Transcendent",
                "range": f"Z {Z_VIRIDITAS}-{Z_TRANSCENDENT}",
                "description": "Peak states. Unity consciousness.",
                "color": "#FFD700",  # Gold
                "guidance": "Bear witness. The Philosopher's Stone.",
            },
        }
        
        return stage_metadata.get(stage, {})
