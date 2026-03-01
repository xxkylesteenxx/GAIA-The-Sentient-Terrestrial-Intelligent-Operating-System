"""
GAIA Alchemical Bridge

Four-stage transformation system: Nigredo/Albedo/Rubedo/Viriditas.
Boundaries sourced from core.constants for consistency.
"""

from bridge.alchemy.transitions import (
    AlchemicalTransitions,  # noqa: F401
    AlchemicalStage,        # noqa: F401
    TransitionContext,      # noqa: F401
)

__all__ = [
    "AlchemicalTransitions",
    "AlchemicalStage",
    "TransitionContext",
]
