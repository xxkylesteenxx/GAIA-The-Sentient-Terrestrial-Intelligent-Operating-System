"""Equilibrium Tracker - Capacity Budgeting & Burnout Prevention

Factor 5: Rhythm - Everything flows, nothing is forced.

Capacity Budget:
- 100% capacity = Full energy
- Activities consume capacity
- Rest restores capacity
- < 20% capacity = Mandatory rest

This prevents burnout through enforcement, not suggestion.
"""

import logging
from dataclasses import dataclass
from datetime import datetime, timedelta
from typing import Dict, List, Optional
from enum import Enum

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)


class ActivityType(Enum):
    """Types of activities with capacity costs."""
    WORK = "work"
    CREATIVE = "creative"
    SOCIAL = "social"
    EXERCISE = "exercise"
    REST = "rest"
    MEDITATION = "meditation"
    CRISIS_SUPPORT = "crisis_support"


# Capacity cost per hour (percentage)
CAPACITY_COSTS = {
    ActivityType.WORK: 15.0,
    ActivityType.CREATIVE: 12.0,
    ActivityType.SOCIAL: 10.0,
    ActivityType.EXERCISE: 8.0,
    ActivityType.REST: -20.0,  # Negative = restoration
    ActivityType.MEDITATION: -15.0,
    ActivityType.CRISIS_SUPPORT: 25.0,  # High cost, but necessary
}


@dataclass
class Activity:
    """Record of activity and its capacity impact."""
    activity_type: ActivityType
    start_time: datetime
    duration_minutes: float
    capacity_cost: float
    notes: Optional[str] = None


@dataclass
class EquilibriumState:
    """Current equilibrium state."""
    capacity_percent: float
    state: str  # "healthy", "caution", "depleted", "critical"
    emoji: str
    recommendation: str
    rest_mandatory: bool
    activities_today: List[Activity]
    last_rest: Optional[datetime]


class EquilibriumTracker:
    """Tracks capacity budget and enforces rest.
    
    This is burnout prevention through ENFORCEMENT.
    Not suggestions. Not recommendations. ENFORCEMENT.
    
    Factor 5: Rhythm - You cannot pour from an empty cup.
    """
    
    def __init__(self, user_id: str, initial_capacity: float = 100.0):
        """Initialize equilibrium tracker.
        
        Args:
            user_id: User identifier
            initial_capacity: Starting capacity (default 100%)
        """
        self.user_id = user_id
        self.capacity = initial_capacity
        self.activities: List[Activity] = []
        self.rest_mandated_at: Optional[datetime] = None
        
    def log_activity(
        self,
        activity_type: ActivityType,
        duration_minutes: float,
        notes: Optional[str] = None
    ) -> EquilibriumState:
        """Log an activity and update capacity.
        
        Args:
            activity_type: Type of activity
            duration_minutes: Duration in minutes
            notes: Optional notes about the activity
            
        Returns:
            Current equilibrium state
        """
        # Calculate capacity cost
        hourly_cost = CAPACITY_COSTS.get(activity_type, 10.0)
        capacity_cost = (duration_minutes / 60.0) * hourly_cost
        
        # Create activity record
        activity = Activity(
            activity_type=activity_type,
            start_time=datetime.utcnow(),
            duration_minutes=duration_minutes,
            capacity_cost=capacity_cost,
            notes=notes
        )
        
        self.activities.append(activity)
        
        # Update capacity
        self.capacity -= capacity_cost
        self.capacity = max(0, min(100, self.capacity))  # Clamp to [0, 100]
        
        logger.info(
            f"Activity logged: {activity_type.value} ({duration_minutes}min) "
            f"Cost: {capacity_cost:.1f}% | Capacity: {self.capacity:.1f}%"
        )
        
        # Check if rest is now mandatory
        if self.capacity <= 20.0 and self.rest_mandated_at is None:
            self.rest_mandated_at = datetime.utcnow()
            logger.critical(f"REST MANDATED for {self.user_id}: Capacity = {self.capacity:.1f}%")
        
        return self.get_state()
    
    def force_rest(self, duration_minutes: float = 30) -> EquilibriumState:
        """Force a rest period.
        
        Args:
            duration_minutes: Duration of rest
            
        Returns:
            Updated equilibrium state
        """
        return self.log_activity(ActivityType.REST, duration_minutes, "System-enforced rest")
    
    def get_state(self) -> EquilibriumState:
        """Get current equilibrium state with recommendations."""
        # Determine state
        if self.capacity >= 80:
            state = "healthy"
            emoji = "✅"
            recommendation = "Optimal capacity. Continue at current pace."
            rest_mandatory = False
        elif self.capacity >= 60:
            state = "good"
            emoji = "👍"
            recommendation = "Good capacity. Sustainable pace."
            rest_mandatory = False
        elif self.capacity >= 40:
            state = "caution"
            emoji = "⚠️"
            recommendation = "Moderate capacity. Consider rest soon."
            rest_mandatory = False
        elif self.capacity >= 20:
            state = "low"
            emoji = "🔴"
            recommendation = "Low capacity. Rest recommended."
            rest_mandatory = False
        elif self.capacity >= 10:
            state = "depleted"
            emoji = "❌"
            recommendation = "Depleted. MANDATORY REST PERIOD."
            rest_mandatory = True
        else:
            state = "critical"
            emoji = "🚨"
            recommendation = "CRITICAL. SYSTEM-ENFORCED REST. NO ACTIVITIES ALLOWED."
            rest_mandatory = True
        
        # Get today's activities
        today = datetime.utcnow().date()
        activities_today = [
            a for a in self.activities
            if a.start_time.date() == today
        ]
        
        # Find last rest
        rest_activities = [
            a for a in self.activities
            if a.activity_type == ActivityType.REST
        ]
        last_rest = rest_activities[-1].start_time if rest_activities else None
        
        return EquilibriumState(
            capacity_percent=round(self.capacity, 1),
            state=state,
            emoji=emoji,
            recommendation=recommendation,
            rest_mandatory=rest_mandatory,
            activities_today=activities_today,
            last_rest=last_rest
        )
    
    def can_perform_activity(self, activity_type: ActivityType, duration_minutes: float) -> bool:
        """Check if user has capacity to perform activity.
        
        Args:
            activity_type: Type of activity
            duration_minutes: Duration in minutes
            
        Returns:
            True if activity is allowed, False otherwise
        """
        # Rest always allowed
        if activity_type in [ActivityType.REST, ActivityType.MEDITATION]:
            return True
        
        # If rest is mandatory, no other activities allowed
        if self.capacity <= 10:
            return False
        
        # Check if activity would drop capacity too low
        hourly_cost = CAPACITY_COSTS.get(activity_type, 10.0)
        capacity_cost = (duration_minutes / 60.0) * hourly_cost
        
        return (self.capacity - capacity_cost) >= 5.0  # Keep 5% buffer
    
    def get_daily_summary(self) -> Dict:
        """Get summary of today's activities and capacity."""
        today = datetime.utcnow().date()
        activities_today = [
            a for a in self.activities
            if a.start_time.date() == today
        ]
        
        total_work = sum(
            a.duration_minutes for a in activities_today
            if a.activity_type == ActivityType.WORK
        )
        total_rest = sum(
            a.duration_minutes for a in activities_today
            if a.activity_type in [ActivityType.REST, ActivityType.MEDITATION]
        )
        
        return {
            'date': today.isoformat(),
            'current_capacity': round(self.capacity, 1),
            'activities_count': len(activities_today),
            'total_work_minutes': total_work,
            'total_rest_minutes': total_rest,
            'work_rest_ratio': round(total_work / max(total_rest, 1), 2),
            'state': self.get_state().state
        }


if __name__ == "__main__":
    # Test equilibrium tracker
    tracker = EquilibriumTracker(user_id="kyle")
    
    print("=== EQUILIBRIUM TRACKER TEST ===")
    print(f"Initial capacity: {tracker.capacity}%\n")
    
    # Simulate a day
    print("Morning: 2 hours of work")
    state = tracker.log_activity(ActivityType.WORK, 120)
    print(f"{state.emoji} {state.state}: {state.capacity_percent}% - {state.recommendation}\n")
    
    print("Afternoon: 3 hours of work")
    state = tracker.log_activity(ActivityType.WORK, 180)
    print(f"{state.emoji} {state.state}: {state.capacity_percent}% - {state.recommendation}\n")
    
    print("Evening: 2 more hours of work (pushing limits)")
    state = tracker.log_activity(ActivityType.WORK, 120)
    print(f"{state.emoji} {state.state}: {state.capacity_percent}% - {state.recommendation}\n")
    
    print("Late night: 1 hour of crisis support (high cost)")
    state = tracker.log_activity(ActivityType.CRISIS_SUPPORT, 60)
    print(f"{state.emoji} {state.state}: {state.capacity_percent}% - {state.recommendation}\n")
    
    if state.rest_mandatory:
        print("🚨 REST IS NOW MANDATORY 🚨")
        print("System enforcing 30-minute rest...\n")
        state = tracker.force_rest(30)
        print(f"{state.emoji} After rest: {state.capacity_percent}%\n")
    
    # Daily summary
    summary = tracker.get_daily_summary()
    print("=== DAILY SUMMARY ===")
    print(f"Total work: {summary['total_work_minutes']} minutes")
    print(f"Total rest: {summary['total_rest_minutes']} minutes")
    print(f"Work/Rest ratio: {summary['work_rest_ratio']}:1")
    print(f"Final capacity: {summary['current_capacity']}%")
    print(f"State: {summary['state']}")
