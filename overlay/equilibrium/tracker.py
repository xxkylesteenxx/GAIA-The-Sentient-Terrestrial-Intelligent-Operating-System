"""Equilibrium Tracker for GAIA Capacity Budgeting.

Monitors system resources and user capacity across three dimensions:
- Cognitive: Mental load, attention, processing
- Emotional: Stress, affect, regulation
- Physical: Energy, health, rest

Implements equilibrium budgets to prevent overload.
"""

from typing import Dict, List
from dataclasses import dataclass, field
from datetime import datetime, timedelta
import logging

logger = logging.getLogger(__name__)


@dataclass
class EquilibriumState:
    """Current equilibrium state snapshot."""
    timestamp: datetime
    cognitive_load: float  # [0,1]
    emotional_load: float  # [0,1]
    physical_load: float   # [0,1]
    z_score: float
    available_capacity: float  # [0,1]
    

class EquilibriumTracker:
    """Track and manage user equilibrium state."""
    
    # Capacity thresholds
    CAPACITY_CRITICAL = 0.1   # 10% remaining
    CAPACITY_LOW = 0.3        # 30% remaining
    CAPACITY_MODERATE = 0.6   # 60% remaining
    CAPACITY_HEALTHY = 0.8    # 80% remaining
    
    def __init__(self, history_window: int = 24):
        """Initialize tracker.
        
        Args:
            history_window: Hours of history to maintain
        """
        self.history_window = timedelta(hours=history_window)
        self.history: List[EquilibriumState] = []
        self.current_state = None
    
    def update_state(self, cognitive: float, emotional: float, 
                     physical: float, z_score: float) -> EquilibriumState:
        """Update current equilibrium state.
        
        Args:
            cognitive: Cognitive load [0,1]
            emotional: Emotional load [0,1]
            physical: Physical load [0,1]
            z_score: Current Z-score
            
        Returns:
            New equilibrium state
        """
        # Calculate available capacity (inverse of average load)
        avg_load = (cognitive + emotional + physical) / 3
        capacity = 1.0 - avg_load
        
        # Z-score influences effective capacity
        z_normalized = z_score / 12.0  # Normalize to [0,1]
        effective_capacity = capacity * z_normalized
        
        state = EquilibriumState(
            timestamp=datetime.now(),
            cognitive_load=cognitive,
            emotional_load=emotional,
            physical_load=physical,
            z_score=z_score,
            available_capacity=effective_capacity
        )
        
        self.current_state = state
        self.history.append(state)
        self._prune_history()
        
        logger.info(f"Equilibrium updated: capacity={effective_capacity:.2f}, Z={z_score:.2f}")
        return state
    
    def get_capacity_level(self) -> str:
        """Get current capacity level classification.
        
        Returns:
            Capacity level string
        """
        if not self.current_state:
            return 'UNKNOWN'
        
        capacity = self.current_state.available_capacity
        
        if capacity < self.CAPACITY_CRITICAL:
            return 'CRITICAL'
        elif capacity < self.CAPACITY_LOW:
            return 'LOW'
        elif capacity < self.CAPACITY_MODERATE:
            return 'MODERATE'
        elif capacity < self.CAPACITY_HEALTHY:
            return 'ADEQUATE'
        else:
            return 'OPTIMAL'
    
    def check_budget(self, requested_load: float) -> Dict:
        """Check if requested activity fits within capacity budget.
        
        Args:
            requested_load: Estimated load of requested activity [0,1]
            
        Returns:
            Budget check result
        """
        if not self.current_state:
            return {
                'approved': False,
                'reason': 'No baseline state established'
            }
        
        capacity = self.current_state.available_capacity
        
        if requested_load <= capacity:
            return {
                'approved': True,
                'remaining_capacity': capacity - requested_load
            }
        else:
            return {
                'approved': False,
                'reason': 'Insufficient capacity',
                'deficit': requested_load - capacity,
                'recommendation': 'Schedule for later or reduce scope'
            }
    
    def get_recovery_estimate(self) -> timedelta:
        """Estimate time until capacity recovery.
        
        Returns:
            Estimated recovery duration
        """
        if not self.current_state or len(self.history) < 3:
            return timedelta(hours=4)  # Default estimate
        
        # Calculate recent trend
        recent = self.history[-6:]  # Last 6 hours
        capacity_change = recent[-1].available_capacity - recent[0].available_capacity
        time_delta = (recent[-1].timestamp - recent[0].timestamp).total_seconds() / 3600
        
        if time_delta == 0 or capacity_change >= 0:
            return timedelta(hours=2)  # Already recovering or stable
        
        # Extrapolate to healthy threshold
        rate = capacity_change / time_delta  # Change per hour
        target = self.CAPACITY_HEALTHY - self.current_state.available_capacity
        hours = abs(target / rate) if rate != 0 else 4
        
        return timedelta(hours=min(hours, 24))  # Cap at 24 hours
    
    def get_recommendations(self) -> List[str]:
        """Get equilibrium maintenance recommendations.
        
        Returns:
            List of recommendation strings
        """
        if not self.current_state:
            return []
        
        recs = []
        state = self.current_state
        
        # Cognitive overload
        if state.cognitive_load > 0.8:
            recs.append("Take a cognitive break - reduce information intake")
        
        # Emotional overload
        if state.emotional_load > 0.8:
            recs.append("Practice emotional regulation - breathing, grounding")
        
        # Physical overload
        if state.physical_load > 0.8:
            recs.append("Prioritize physical rest - sleep, nutrition, movement")
        
        # Low Z-score
        if state.z_score < 6.0:
            recs.append("Increase coherence practices - meditation, nature, creativity")
        
        # Overall capacity
        level = self.get_capacity_level()
        if level in ['CRITICAL', 'LOW']:
            recs.append("Reduce all non-essential activities immediately")
        
        return recs
    
    def _prune_history(self):
        """Remove history older than window."""
        cutoff = datetime.now() - self.history_window
        self.history = [s for s in self.history if s.timestamp > cutoff]
