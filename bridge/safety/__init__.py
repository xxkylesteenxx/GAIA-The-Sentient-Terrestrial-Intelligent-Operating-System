"""
SAFETY SYSTEM (Bridge Plane - Factor 10)

Protects users from harm, especially during crisis.

Key components:
1. Crisis detection (Z ≤ 2 threshold)
2. 988 integration (Suicide & Crisis Lifeline)
3. Avatar emergency protocols
4. Mandatory intervention (cannot be bypassed)
5. Graduated response (severity-appropriate actions)

Philosophy:
"Factor 13 (Universal Love) made manifest.
No one falls alone. No one suffers in silence."

Graduation:
- Z ≤ 2: Crisis detected, 988 recommended
- Z ≤ 1: Severe crisis, emergency contacts notified (with consent)
- Z ≤ 0: Critical emergency, local emergency services alert (if configured)

Governance:
- Cannot be disabled (safety is non-negotiable)
- User configurable (emergency contacts, escalation preferences)
- Privacy preserving (crisis data never shared without consent)
"""

from .crisis_detection import (
    CrisisDetector,
    CrisisLevel,
    CrisisResponse,
    CrisisResources
)

__all__ = [
    'CrisisDetector',
    'CrisisLevel',
    'CrisisResponse',
    'CrisisResources'
]
