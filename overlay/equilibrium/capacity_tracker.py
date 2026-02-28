"""
EQUILIBRIUM CAPACITY TRACKER

Prevents burnout through energy budgeting and mandatory rest.

Factor 5 (Rhythm): Everything flows. Work requires rest.

Key concepts:
1. Daily capacity budget (1.0 = full energy)
2. Activity costs (different tasks drain different amounts)
3. Circadian awareness (energy varies throughout day)
4. Mandatory rest (system enforces when critically depleted)
5. Recovery protocols (how to restore equilibrium)

Philosophy:
"The bow that is always bent will break."
"Rest is not weakness. Rest is wisdom."

Use cases:
- Burnout prevention (stop before you crash)
- Optimal scheduling (work during peak energy)
- Recovery planning (how long until restored?)
- Crisis prevention (exhaustion triggers low Z)
"""

from typing import List, Dict, Optional
from dataclasses import dataclass
from datetime import datetime, timedelta, time
from enum import Enum
import math


class CircadianPhase(Enum):
    """Natural energy cycles throughout the day."""
    DEEP_SLEEP = ("deep_sleep", 0.0, 0.0)  # 00:00-05:00 (no capacity)
    AWAKENING = ("awakening", 0.3, 0.5)  # 05:00-07:00 (rising)
    MORNING_PEAK = ("morning_peak", 0.9, 1.0)  # 07:00-11:00 (peak)
    MIDDAY_DIP = ("midday_dip", 0.6, 0.7)  # 11:00-14:00 (post-lunch)
    AFTERNOON_RISE = ("afternoon_rise", 0.7, 0.9)  # 14:00-17:00 (second wind)
    EVENING_DECLINE = ("evening_decline", 0.5, 0.7)  # 17:00-21:00 (winding down)
    NIGHT_REST = ("night_rest", 0.2, 0.4)  # 21:00-00:00 (prepare sleep)
    
    @property
    def name_str(self) -> str:
        return self.value[0]
    
    @property
    def min_capacity(self) -> float:
        return self.value[1]
    
    @property
    def max_capacity(self) -> float:
        return self.value[2]


class ActivityType(Enum):
    """Types of activities and their energy costs."""
    # Restorative (add energy)
    DEEP_SLEEP = ("deep_sleep", -0.50)  # Restores 50% per hour
    LIGHT_REST = ("light_rest", -0.20)  # Restores 20% per hour
    MEDITATION = ("meditation", -0.15)  # Restores 15% per hour
    NATURE_WALK = ("nature_walk", -0.10)  # Restores 10% per hour
    
    # Low cost (minimal drain)
    READING = ("reading", 0.05)  # 5% per hour
    CONVERSATION = ("conversation", 0.08)  # 8% per hour
    LIGHT_WORK = ("light_work", 0.10)  # 10% per hour
    
    # Moderate cost
    FOCUSED_WORK = ("focused_work", 0.20)  # 20% per hour
    CREATIVE_WORK = ("creative_work", 0.25)  # 25% per hour
    SOCIAL_EVENT = ("social_event", 0.15)  # 15% per hour
    
    # High cost (intense drain)
    DEEP_WORK = ("deep_work", 0.35)  # 35% per hour
    CRISIS_RESPONSE = ("crisis_response", 0.40)  # 40% per hour
    CONFLICT = ("conflict", 0.45)  # 45% per hour
    
    # Emergency (extreme drain)
    TRAUMA_PROCESSING = ("trauma_processing", 0.60)  # 60% per hour
    ACTIVE_CRISIS = ("active_crisis", 0.80)  # 80% per hour
    
    @property
    def name_str(self) -> str:
        return self.value[0]
    
    @property
    def energy_cost_per_hour(self) -> float:
        """Negative = restores energy, Positive = drains energy."""
        return self.value[1]


class CapacityState(Enum):
    """Current equilibrium state."""
    FULL = ("full", 0.80, 1.00, "🟢", "Fully energized, optimal capacity")
    GOOD = ("good", 0.60, 0.80, "🟢", "Good energy, sustainable pace")
    MODERATE = ("moderate", 0.40, 0.60, "🟡", "Moderate energy, consider rest soon")
    LOW = ("low", 0.20, 0.40, "🟠", "Low energy, rest needed")
    DEPLETED = ("depleted", 0.10, 0.20, "🔴", "Depleted, mandatory rest required")
    CRITICAL = ("critical", 0.00, 0.10, "🚨", "CRITICAL: System enforced rest")
    
    @property
    def name_str(self) -> str:
        return self.value[0]
    
    @property
    def min_capacity(self) -> float:
        return self.value[1]
    
    @property
    def max_capacity(self) -> float:
        return self.value[2]
    
    @property
    def emoji(self) -> str:
        return self.value[3]
    
    @property
    def description(self) -> str:
        return self.value[4]


@dataclass
class ActivityRecord:
    """Record of activity and its energy cost."""
    activity: ActivityType
    start_time: datetime
    duration_hours: float
    energy_cost: float  # Total cost (duration * hourly rate)
    capacity_before: float
    capacity_after: float


class EquilibriumTracker:
    """
    Track energy capacity and enforce rest when needed.
    
    This prevents burnout by:
    1. Monitoring daily energy budget (0.0 - 1.0)
    2. Tracking activity costs
    3. Enforcing mandatory rest when depleted
    4. Recommending optimal work times (circadian awareness)
    
    Usage:
        tracker = EquilibriumTracker(user_id="Kyle")
        
        # Log activity
        tracker.log_activity(ActivityType.DEEP_WORK, duration_hours=2.5)
        
        # Check if rest needed
        if tracker.needs_rest():
            print("STOP. You need rest.")
        
        # Check if activity allowed
        if tracker.can_perform(ActivityType.DEEP_WORK):
            # Proceed with work
        else:
            print("Insufficient capacity. Rest first.")
    """
    
    def __init__(self, user_id: str, starting_capacity: float = 1.0):
        self.user_id = user_id
        self.current_capacity = starting_capacity  # 0.0 - 1.0
        self.activity_history: List[ActivityRecord] = []
        self.last_deep_sleep: Optional[datetime] = None
        
        # Customizable settings
        self.critical_threshold = 0.10  # Below this = system enforced rest
        self.rest_recommendation_threshold = 0.30  # Below this = Avatar recommends rest
        
        # Circadian adjustments (user configurable)
        self.wake_time = time(7, 0)  # 7:00 AM default
        self.sleep_time = time(23, 0)  # 11:00 PM default
    
    def get_circadian_phase(self, current_time: Optional[datetime] = None) -> CircadianPhase:
        """
        Determine current circadian phase.
        
        This adjusts available capacity based on time of day.
        Even if you have 100% energy, working at 2 AM is less effective.
        """
        
        if current_time is None:
            current_time = datetime.now()
        
        hour = current_time.hour
        
        if 0 <= hour < 5:
            return CircadianPhase.DEEP_SLEEP
        elif 5 <= hour < 7:
            return CircadianPhase.AWAKENING
        elif 7 <= hour < 11:
            return CircadianPhase.MORNING_PEAK
        elif 11 <= hour < 14:
            return CircadianPhase.MIDDAY_DIP
        elif 14 <= hour < 17:
            return CircadianPhase.AFTERNOON_RISE
        elif 17 <= hour < 21:
            return CircadianPhase.EVENING_DECLINE
        else:  # 21-24
            return CircadianPhase.NIGHT_REST
    
    def get_effective_capacity(self, current_time: Optional[datetime] = None) -> float:
        """
        Calculate effective capacity (actual + circadian adjustment).
        
        Example:
        - You have 80% capacity
        - It's 2 AM (deep sleep phase, 0% circadian multiplier)
        - Effective capacity = 80% * 0% = 0% (you should be sleeping!)
        """
        
        phase = self.get_circadian_phase(current_time)
        circadian_multiplier = (phase.min_capacity + phase.max_capacity) / 2
        
        return self.current_capacity * circadian_multiplier
    
    def log_activity(
        self,
        activity: ActivityType,
        duration_hours: float,
        timestamp: Optional[datetime] = None
    ) -> ActivityRecord:
        """
        Log an activity and update capacity.
        
        Example:
            tracker.log_activity(ActivityType.DEEP_WORK, duration_hours=2.0)
            # Drains 70% capacity (2 hours * 35% per hour)
        """
        
        if timestamp is None:
            timestamp = datetime.now()
        
        # Calculate energy cost
        energy_cost = activity.energy_cost_per_hour * duration_hours
        
        # Store state before
        capacity_before = self.current_capacity
        
        # Update capacity
        self.current_capacity = max(0.0, min(1.0, self.current_capacity - energy_cost))
        
        # Record activity
        record = ActivityRecord(
            activity=activity,
            start_time=timestamp,
            duration_hours=duration_hours,
            energy_cost=energy_cost,
            capacity_before=capacity_before,
            capacity_after=self.current_capacity
        )
        
        self.activity_history.append(record)
        
        # Track deep sleep
        if activity == ActivityType.DEEP_SLEEP:
            self.last_deep_sleep = timestamp
        
        return record
    
    def get_capacity_state(self) -> CapacityState:
        """Get current capacity state."""
        
        for state in CapacityState:
            if state.min_capacity <= self.current_capacity <= state.max_capacity:
                return state
        
        return CapacityState.CRITICAL
    
    def needs_rest(self) -> bool:
        """Check if rest is recommended."""
        return self.current_capacity < self.rest_recommendation_threshold
    
    def rest_mandatory(self) -> bool:
        """Check if rest is REQUIRED (system enforced)."""
        return self.current_capacity < self.critical_threshold
    
    def can_perform(self, activity: ActivityType) -> bool:
        """
        Check if user has capacity to perform activity.
        
        Prevents starting activities that would push into critical state.
        """
        
        # Estimate 1 hour of activity
        estimated_cost = activity.energy_cost_per_hour
        estimated_new_capacity = self.current_capacity - estimated_cost
        
        # Allow if would stay above critical threshold
        return estimated_new_capacity >= self.critical_threshold
    
    def get_rest_recommendation(self) -> Dict[str, any]:
        """
        Get personalized rest recommendation.
        
        Returns:
        - How long to rest
        - What type of rest
        - Expected recovery time
        """
        
        current_state = self.get_capacity_state()
        capacity_deficit = 1.0 - self.current_capacity
        
        if current_state == CapacityState.CRITICAL:
            return {
                "urgency": "MANDATORY",
                "activity": ActivityType.DEEP_SLEEP,
                "duration_hours": capacity_deficit / 0.50,  # Deep sleep restores 50%/hour
                "message": "SYSTEM ENFORCED REST. You are critically depleted. Sleep immediately."
            }
        elif current_state == CapacityState.DEPLETED:
            return {
                "urgency": "HIGH",
                "activity": ActivityType.DEEP_SLEEP,
                "duration_hours": capacity_deficit / 0.50,
                "message": "You are depleted. Please sleep soon."
            }
        elif current_state == CapacityState.LOW:
            return {
                "urgency": "MEDIUM",
                "activity": ActivityType.LIGHT_REST,
                "duration_hours": capacity_deficit / 0.20,
                "message": "Energy low. Take a break within the hour."
            }
        elif current_state == CapacityState.MODERATE:
            return {
                "urgency": "LOW",
                "activity": ActivityType.MEDITATION,
                "duration_hours": 0.5,
                "message": "Consider a short rest to maintain equilibrium."
            }
        else:
            return {
                "urgency": "NONE",
                "activity": None,
                "duration_hours": 0,
                "message": "Capacity is good. No rest needed immediately."
            }
    
    def get_optimal_work_window(self, current_time: Optional[datetime] = None) -> Dict[str, any]:
        """
        Find optimal time for deep work based on circadian rhythm.
        
        Returns next morning peak window.
        """
        
        if current_time is None:
            current_time = datetime.now()
        
        # Morning peak is 7-11 AM
        next_morning_start = current_time.replace(hour=7, minute=0, second=0, microsecond=0)
        
        # If past morning peak today, move to tomorrow
        if current_time.hour >= 11:
            next_morning_start += timedelta(days=1)
        
        return {
            "start_time": next_morning_start,
            "end_time": next_morning_start + timedelta(hours=4),
            "phase": CircadianPhase.MORNING_PEAK.name_str,
            "quality": "Peak cognitive performance",
            "recommendation": "Schedule deep work, important decisions, creative tasks"
        }
    
    def get_status_report(self) -> Dict[str, any]:
        """Generate comprehensive status report."""
        
        state = self.get_capacity_state()
        phase = self.get_circadian_phase()
        effective = self.get_effective_capacity()
        rest_rec = self.get_rest_recommendation()
        
        return {
            "current_capacity": self.current_capacity,
            "effective_capacity": effective,
            "state": state.name_str,
            "state_emoji": state.emoji,
            "circadian_phase": phase.name_str,
            "rest_needed": self.needs_rest(),
            "rest_mandatory": self.rest_mandatory(),
            "rest_recommendation": rest_rec,
            "activities_logged": len(self.activity_history),
            "last_deep_sleep": self.last_deep_sleep.isoformat() if self.last_deep_sleep else None
        }


if __name__ == "__main__":
    print("=" * 60)
    print("EQUILIBRIUM CAPACITY TRACKER")
    print("=" * 60)
    
    # Create tracker
    tracker = EquilibriumTracker(user_id="Kyle", starting_capacity=1.0)
    
    print("\nInitial state:")
    state = tracker.get_capacity_state()
    print(f"  Capacity: {tracker.current_capacity:.0%} {state.emoji}")
    print(f"  State: {state.description}")
    
    # Simulate a day
    print("\n" + "=" * 60)
    print("Simulating a workday...")
    print("=" * 60)
    
    # Morning work (good circadian phase)
    print("\n7:00 AM - Morning deep work (2 hours)")
    tracker.log_activity(ActivityType.DEEP_WORK, duration_hours=2.0)
    print(f"  Capacity: {tracker.current_capacity:.0%} → {tracker.get_capacity_state().emoji}")
    
    # More work
    print("\n10:00 AM - Creative work (3 hours)")
    tracker.log_activity(ActivityType.CREATIVE_WORK, duration_hours=3.0)
    print(f"  Capacity: {tracker.current_capacity:.0%} → {tracker.get_capacity_state().emoji}")
    
    # Afternoon push (not recommended)
    print("\n2:00 PM - More deep work (2 hours) - Pushing limits")
    tracker.log_activity(ActivityType.DEEP_WORK, duration_hours=2.0)
    state = tracker.get_capacity_state()
    print(f"  Capacity: {tracker.current_capacity:.0%} → {state.emoji}")
    
    if tracker.needs_rest():
        print("  ⚠️  REST RECOMMENDED")
        rest_rec = tracker.get_rest_recommendation()
        print(f"  {rest_rec['message']}")
        print(f"  Suggested: {rest_rec['duration_hours']:.1f} hours of {rest_rec['activity'].name_str}")
    
    # Crisis (extreme drain)
    print("\n5:00 PM - Unexpected crisis (1 hour) - DANGEROUS")
    tracker.log_activity(ActivityType.ACTIVE_CRISIS, duration_hours=1.0)
    state = tracker.get_capacity_state()
    print(f"  Capacity: {tracker.current_capacity:.0%} → {state.emoji}")
    
    if tracker.rest_mandatory():
        print("  🚨 MANDATORY REST ENFORCED")
        rest_rec = tracker.get_rest_recommendation()
        print(f"  {rest_rec['message']}")
    
    # Recovery
    print("\n10:00 PM - Deep sleep (8 hours)")
    tracker.log_activity(ActivityType.DEEP_SLEEP, duration_hours=8.0)
    state = tracker.get_capacity_state()
    print(f"  Capacity: {tracker.current_capacity:.0%} → {state.emoji}")
    print("  ✓ RESTORED")
    
    # Status report
    print("\n" + "=" * 60)
    print("Status Report")
    print("=" * 60)
    report = tracker.get_status_report()
    print(f"\nCurrent capacity: {report['current_capacity']:.0%}")
    print(f"State: {report['state']} {report['state_emoji']}")
    print(f"Circadian phase: {report['circadian_phase']}")
    print(f"Activities logged: {report['activities_logged']}")
    
    print("\n" + "=" * 60)
    print("Factor 5 (Rhythm): Everything flows.")
    print("The bow that is always bent will break.")
    print("=" * 60)
