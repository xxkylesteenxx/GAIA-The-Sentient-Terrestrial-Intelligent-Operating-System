"""
ALCHEMICAL TRANSITION SYSTEM
Bridge Plane — Factor 10 (Chaos) → Factor 12 (Balance)

Four-stage alchemical transformation:
    Nigredo   (Blackening)  — Dissolution, shadow work, chaos
    Albedo    (Whitening)   — Purification, integration, clarity
    Rubedo    (Reddening)   — Embodiment, completion, manifestation
    Viriditas (Greening)    — Growth, vitality, renewal (Hildegard von Bingen)

Stage boundaries are sourced from core.constants — never duplicated here.
This ensures the alchemical map matches the Z-score interpretation everywhere
in the codebase (README, CLI output, Avatar speech, crisis detector).
"""

from __future__ import annotations

import logging
from dataclasses import dataclass
from enum import Enum
from typing import Dict

from core.constants import (
    Z_CRISIS_UPPER,       # 2.0  — crisis / nigredo boundary
    Z_NIGREDO_UPPER,      # 4.0  — nigredo / albedo boundary
    Z_ALBEDO_UPPER,       # 6.0  — albedo / rubedo boundary
    Z_RUBEDO_UPPER,       # 8.0  — rubedo / viriditas boundary
    Z_VIRIDITAS_UPPER,    # 10.0 — viriditas / transcendent boundary
)

logger = logging.getLogger(__name__)


# ---------------------------------------------------------------------------
# Stage enum
# ---------------------------------------------------------------------------


class AlchemicalStage(Enum):
    """Four stages of alchemical transformation."""

    NIGREDO = "nigredo"       # Chaos, dissolution
    ALBEDO = "albedo"         # Purification, clarity
    RUBEDO = "rubedo"         # Embodiment, completion
    VIRIDITAS = "viriditas"   # Growth, vitality


# Stage metadata table — single place to update copy / colours / elements.
_STAGE_DATA: Dict[AlchemicalStage, Dict] = {
    AlchemicalStage.NIGREDO: {
        "theme": "dissolution",
        "guidance": "Embrace the shadow; allow decomposition.",
        "color": "#1a1a1a",
        "element": "earth",
        "z_min": 0.0,
        "z_max": Z_NIGREDO_UPPER,   # 4.0
    },
    AlchemicalStage.ALBEDO: {
        "theme": "purification",
        "guidance": "Distil essence; seek clarity.",
        "color": "#e8e8e8",
        "element": "water",
        "z_min": Z_NIGREDO_UPPER,   # 4.0
        "z_max": Z_ALBEDO_UPPER,    # 6.0
    },
    AlchemicalStage.RUBEDO: {
        "theme": "embodiment",
        "guidance": "Integrate wisdom; manifest completion.",
        "color": "#cc4400",
        "element": "fire",
        "z_min": Z_ALBEDO_UPPER,    # 6.0
        "z_max": Z_RUBEDO_UPPER,    # 8.0
    },
    AlchemicalStage.VIRIDITAS: {
        "theme": "vitality",
        "guidance": "Flourish, grow, renew.",
        "color": "#00cc44",
        "element": "air",
        "z_min": Z_RUBEDO_UPPER,    # 8.0
        "z_max": 12.0,
    },
}


# ---------------------------------------------------------------------------
# Context dataclass
# ---------------------------------------------------------------------------


@dataclass
class TransitionContext:
    """Snapshot of user state at the moment a transition is evaluated."""

    current_stage: AlchemicalStage
    z_score: float
    emotional_state: str = ""
    crisis_level: str = "NONE"
    equilibrium_capacity: float = 1.0


# ---------------------------------------------------------------------------
# Transition manager
# ---------------------------------------------------------------------------


class AlchemicalTransitions:
    """
    Manage alchemical stage transitions.

    Usage::

        transitions = AlchemicalTransitions()

        context = TransitionContext(
            current_stage=AlchemicalStage.NIGREDO,
            z_score=5.2,
        )
        result = transitions.transition(context)

        if result["transition"]:
            print(result["to_stage"])   # "albedo"
            print(result["guidance"])
    """

    def __init__(self) -> None:
        self.current_stage = AlchemicalStage.NIGREDO

    # ------------------------------------------------------------------ #
    # Public API                                                           #
    # ------------------------------------------------------------------ #

    def determine_stage(self, z_score: float) -> AlchemicalStage:
        """
        Map a Z-score to the appropriate alchemical stage.

        Crisis (Z < 2.0) is mapped to Nigredo — the user is in the dark
        night; alchemical work begins once intervention has stabilised them.
        """
        if z_score < Z_ALBEDO_UPPER:       # < 6.0  →  nigredo or albedo
            if z_score < Z_NIGREDO_UPPER:  # < 4.0  →  nigredo (incl. crisis)
                return AlchemicalStage.NIGREDO
            return AlchemicalStage.ALBEDO
        if z_score < Z_RUBEDO_UPPER:       # 6.0–8.0
            return AlchemicalStage.RUBEDO
        return AlchemicalStage.VIRIDITAS   # ≥ 8.0

    def transition(self, context: TransitionContext) -> Dict:
        """
        Evaluate whether a stage transition is warranted.

        Returns a result dict.  If transition occurred,
        ``result["transition"]`` is True and the new stage data is included.
        """
        target_stage = self.determine_stage(context.z_score)

        if target_stage == context.current_stage:
            return {
                "transition": False,
                "stage": context.current_stage.value,
                "message": "Remaining in current stage.",
                "stage_data": _STAGE_DATA[context.current_stage],
            }

        logger.info(
            "Alchemical transition: %s → %s  (Z=%.2f)",
            context.current_stage.value,
            target_stage.value,
            context.z_score,
        )

        self.current_stage = target_stage

        return {
            "transition": True,
            "from_stage": context.current_stage.value,
            "to_stage": target_stage.value,
            "stage_data": _STAGE_DATA[target_stage],
            "guidance": _STAGE_DATA[target_stage]["guidance"],
            "z_score": context.z_score,
        }

    def get_stage_guidance(self, stage: AlchemicalStage) -> str:
        """Return long-form guidance text for the given stage."""

        _GUIDANCE: Dict[AlchemicalStage, str] = {
            AlchemicalStage.NIGREDO: (
                "You are in Nigredo — the stage of dissolution. "
                "This is the time to face shadows, release what no longer serves, "
                "and allow transformation through decomposition. "
                "Chaos precedes creation. "
                "Z range: 0 – 4."
            ),
            AlchemicalStage.ALBEDO: (
                "You are in Albedo — the stage of purification. "
                "Focus on clarity, distil essence from experience, "
                "and integrate lessons. The mud settles; clear water emerges. "
                "Z range: 4 – 6."
            ),
            AlchemicalStage.RUBEDO: (
                "You are in Rubedo — the stage of embodiment. "
                "Wisdom becomes action; insights manifest; completion approaches. "
                "The fire tempers the metal. "
                "Z range: 6 – 8."
            ),
            AlchemicalStage.VIRIDITAS: (
                "You are in Viriditas — the stage of greening. "
                "Life force flows freely; growth is natural; vitality abounds. "
                "You flourish in the garden of your becoming. "
                "Z range: 8 – 12."
            ),
        }

        return _GUIDANCE.get(stage, "Unknown stage.")

    def get_full_stage_data(self, stage: AlchemicalStage) -> Dict:
        """Return complete metadata for the given stage."""
        return _STAGE_DATA.get(stage, {})
