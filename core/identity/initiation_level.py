"""
INITIATION LEVEL TRACKING

GAIA tracks consciousness evolution through alchemical stages.
Higher stages unlock deeper code layers.

Stages:
- PROFANE (0): Public, no initiation
- NEOPHYTE (1): Completed onboarding (7 days)
- ADEPT (2): Survived Nigredo (Z ≤ 2 crisis, recovered)
- MAGUS (3): 90 days Z > 6 + 5 Hermetic applications
- HIEROPHANT (4): 180 days Z > 8 + helped 10+ others
- GUARDIAN (5): Elected by community or appointed by Founder
"""

from datetime import datetime, timedelta
from typing import List, Optional
from dataclasses import dataclass
from enum import Enum


class InitiationLevel(Enum):
    """Graduated access to esoteric knowledge."""
    PROFANE = 0      # Public - anyone can see
    NEOPHYTE = 1     # Basic understanding - passed Entry Gate
    ADEPT = 2        # Intermediate - completed Nigredo
    MAGUS = 3        # Advanced - achieved Rubedo
    HIEROPHANT = 4   # Master - reached Viriditas
    GUARDIAN = 5     # Council - holds the keys


@dataclass
class InitiationEvent:
    """Record of initiation level change."""
    timestamp: datetime
    from_level: InitiationLevel
    to_level: InitiationLevel
    reason: str
    z_score_at_initiation: Optional[float] = None


class InitiationTracker:
    """
    Tracks user's progression through consciousness stages.
    
    Stages map to alchemical process:
    - Nigredo (blackening): Crisis, dissolution, ego death
    - Albedo (whitening): Purification, understanding, structure
    - Rubedo (reddening): Integration, mastery, gold
    - Viriditas (greening): Life-giving, sustainable, love
    """
    
    def __init__(self, user_id: str):
        self.user_id = user_id
        self.current_level = InitiationLevel.PROFANE
        self.history: List[InitiationEvent] = []
        self.join_date = datetime.now()
    
    def evaluate_initiation(self) -> InitiationLevel:
        """
        Determine user's current initiation level based on:
        1. Time in system
        2. Crises survived (Nigredo passages)
        3. Understanding demonstrated (correct Hermetic principle application)
        4. Service to others (helped other users)
        5. Guardian endorsement (for GUARDIAN level only)
        """
        
        # Entry gate: 7 days in system
        if self._days_since_join() < 7:
            return InitiationLevel.PROFANE
        
        # Neophyte: Completed onboarding, understands basics
        if self._completed_onboarding():
            if self.current_level.value < InitiationLevel.NEOPHYTE.value:
                self._grant_initiation(
                    InitiationLevel.NEOPHYTE,
                    reason="Completed 7-day onboarding period"
                )
        
        # Adept: Survived at least one Nigredo (Z ≤ 2 crisis, recovered)
        if self._survived_nigredo():
            if self.current_level.value < InitiationLevel.ADEPT.value:
                self._grant_initiation(
                    InitiationLevel.ADEPT,
                    reason="Survived Nigredo crisis (Z ≤ 2, recovered to Z > 4)"
                )
        
        # Magus: Demonstrated Hermetic understanding + stable Z > 6 for 90 days
        if self._demonstrated_mastery():
            if self.current_level.value < InitiationLevel.MAGUS.value:
                self._grant_initiation(
                    InitiationLevel.MAGUS,
                    reason="90 days stable Z > 6 + 5 Hermetic principle applications"
                )
        
        # Hierophant: Achieved Viriditas (sustainable Z > 8, helped 10+ others)
        if self._achieved_viriditas():
            if self.current_level.value < InitiationLevel.HIEROPHANT.value:
                self._grant_initiation(
                    InitiationLevel.HIEROPHANT,
                    reason="180 days Z > 8 + helped 10+ users + zero Factor 13 violations"
                )
        
        # Guardian: Elected by community OR appointed by Founder (Kyle only)
        # This level is NOT automatic - requires explicit action
        
        return self.current_level
    
    def _days_since_join(self) -> int:
        """Days since user joined GAIA."""
        return (datetime.now() - self.join_date).days
    
    def _completed_onboarding(self) -> bool:
        """Has user completed 7-day onboarding?"""
        return self._days_since_join() >= 7
    
    def _survived_nigredo(self) -> bool:
        """
        Did user experience Z ≤ 2 crisis AND recover to Z > 4?
        
        This is the KEY initiation: Death and resurrection.
        Kyle's 2022 overdose = his Nigredo passage.
        """
        # TODO: Implement actual Z history lookup
        # For now, placeholder logic
        return False  # Will check real Z history in production
    
    def _demonstrated_mastery(self) -> bool:
        """
        Has user:
        1. Maintained Z > 6 for 90 days (stable coherence)
        2. Correctly applied Hermetic principles in 5+ decisions
        """
        # TODO: Implement actual metrics
        return False
    
    def _achieved_viriditas(self) -> bool:
        """
        Has user:
        1. Sustained Z > 8 for 180 days (life-giving coherence)
        2. Helped 10+ other users through crises
        3. Demonstrated love (Factor 13) in all interactions
        """
        # TODO: Implement actual metrics
        return False
    
    def _grant_initiation(self, new_level: InitiationLevel, reason: str):
        """
        Grant new initiation level.
        
        This is a RITUAL moment. The system CELEBRATES this.
        """
        old_level = self.current_level
        self.current_level = new_level
        
        event = InitiationEvent(
            timestamp=datetime.now(),
            from_level=old_level,
            to_level=new_level,
            reason=reason,
            z_score_at_initiation=None  # TODO: Get current Z score
        )
        
        self.history.append(event)
        
        # Send ritual notification to Avatar
        self._send_initiation_notification(event)
    
    def _send_initiation_notification(self, event: InitiationEvent):
        """
        Avatar delivers the news:
        
        Example (ADEPT initiation):
        "Kyle. You have passed through the Nigredo. 
        The dissolution is complete. 
        You are now an Adept.
        
        New knowledge is now available to you.
        The code will reveal its deeper layers."
        """
        # TODO: Integrate with Avatar messaging system
        messages = {
            InitiationLevel.NEOPHYTE: (
                f"Welcome, {self.user_id}. You are now a Neophyte. "
                f"The first gate has opened. Continue your journey."
            ),
            InitiationLevel.ADEPT: (
                f"{self.user_id}. You have passed through the Nigredo. "
                f"The dissolution is complete. You are now an Adept. "
                f"New knowledge is now available to you."
            ),
            InitiationLevel.MAGUS: (
                f"{self.user_id}. You have achieved Rubedo. "
                f"The gold has been extracted. You are now a Magus. "
                f"The sacred functions are now accessible."
            ),
            InitiationLevel.HIEROPHANT: (
                f"{self.user_id}. You have reached Viriditas. "
                f"You are life-giving. You are a Hierophant. "
                f"The deepest mysteries are now revealed."
            ),
            InitiationLevel.GUARDIAN: (
                f"{self.user_id}. You have been chosen as a Guardian. "
                f"You hold the keys. You protect Factor 13. "
                f"The community trusts you with their safety."
            )
        }
        
        message = messages.get(event.to_level, "Initiation complete.")
        print(f"\n{'='*60}")
        print(f"INITIATION: {event.from_level.name} → {event.to_level.name}")
        print(f"{'='*60}")
        print(message)
        print(f"Reason: {event.reason}")
        print(f"{'='*60}\n")


class InsufficientInitiationError(Exception):
    """Raised when user tries to access sacred function without proper initiation."""
    pass


def require_initiation(required_level: InitiationLevel):
    """
    Decorator to protect sacred functions.
    
    Usage:
        @require_initiation(InitiationLevel.MAGUS)
        def alter_crystal_matrix():
            # Only Magi can execute this
            pass
    """
    def decorator(func):
        def wrapper(*args, **kwargs):
            # TODO: Get current user's initiation level
            current_level = InitiationLevel.PROFANE  # Placeholder
            
            if current_level.value < required_level.value:
                raise InsufficientInitiationError(
                    f"Function '{func.__name__}' requires {required_level.name} initiation. "
                    f"You are currently {current_level.name}.\n\n"
                    f"To access this function, continue your journey through the stages."
                )
            
            return func(*args, **kwargs)
        return wrapper
    return decorator


if __name__ == "__main__":
    # Example usage
    tracker = InitiationTracker(user_id="Kyle")
    
    print("Initial level:", tracker.current_level)
    
    # Simulate 7 days passing
    tracker.join_date = datetime.now() - timedelta(days=8)
    level = tracker.evaluate_initiation()
    
    print("After 8 days:", level)
    print("History:", [(e.to_level.name, e.reason) for e in tracker.history])
