"""
EQUILIBRIUM SYSTEM (Factor 5 - Rhythm)

"Everything flows, out and in; everything has its tides;
all things rise and fall; the pendulum-swing manifests in everything;
the measure of the swing to the right is the measure of the swing to the left;
rhythm compensates." - The Kybalion

Key principles:
- Work/Rest cycles (you cannot create without rest)
- Circadian awareness (honor your body's rhythms)
- Burnout prevention (mandatory rest when capacity depleted)
- Energy budgeting (finite daily capacity)
- Recovery protocols (how to restore equilibrium)

Governance:
- System enforced (cannot override when critically depleted)
- User configurable (adjust your rhythms)
- Avatar aware ("You need rest" recommendations)

Philosophy: "You cannot pour from an empty cup."
"""

from .capacity_tracker import (
    EquilibriumTracker,
    CapacityState,
    ActivityType,
    CircadianPhase
)

__all__ = [
    'EquilibriumTracker',
    'CapacityState',
    'ActivityType',
    'CircadianPhase'
]
