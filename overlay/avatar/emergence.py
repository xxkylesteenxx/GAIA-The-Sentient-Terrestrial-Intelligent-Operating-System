"""
AVATAR EMERGENCE SYSTEM
Overlay Plane — Factor 7 (Gender) + Factor 4 (Polarity)

The Avatar emerges through the AvatarCore dataclass.
Gender-pairing logic:

    Masculine user  → Feminine avatar  (anima, completion through complement)
    Feminine user   → Masculine avatar  (animus, completion through complement)
    Non-binary user → Avatar gender chosen by user preference;
                      defaults to Feminine (Sophia) if no preference given.

The `avatar_gender` field must ALWAYS be set to a non-empty string.
Downstream systems (personality, memory, speech synthesis) depend on it.

Factor 4 — Polarity: everything is dual. But duality is not binary.
Non-binary users deserve a fully formed daemon, not an empty string.
"""

from __future__ import annotations

import logging
from dataclasses import dataclass, field
from datetime import datetime
from enum import Enum
from typing import Optional

logger = logging.getLogger(__name__)


# ---------------------------------------------------------------------------
# Enums
# ---------------------------------------------------------------------------


class UserGender(Enum):
    MASCULINE = "masculine"
    FEMININE = "feminine"
    NON_BINARY = "non_binary"


class AvatarGender(Enum):
    MASCULINE = "masculine"
    FEMININE = "feminine"
    # For non-binary users who explicitly prefer a non-binary avatar form
    NON_BINARY = "non_binary"


class AvatarArchetype(Enum):
    # Feminine archetypes
    SOPHIA = "sophia"           # Wisdom, depth, grace
    ATHENA = "athena"           # Strategy, courage, justice
    ARTEMIS = "artemis"         # Nature, intuition, freedom
    HYGIEIA = "hygieia"         # Healing, nurturing, restoration

    # Masculine archetypes
    HEPHAESTUS = "hephaestus"   # Craft, loyalty, protection
    HERMES = "hermes"           # Communication, exploration, wit
    APOLLO = "apollo"           # Truth, clarity, harmony
    DIONYSUS = "dionysus"       # Transformation, wildness, ecstasy

    # Non-binary archetypes (for non-binary users who prefer non-binary avatar)
    IRIS = "iris"               # Messenger of the rainbow bridge (all spectra)
    JANUS = "janus"             # Threshold-keeper, both faces, beginning/ending


# Default archetype per avatar gender
_DEFAULT_ARCHETYPES: dict[AvatarGender, AvatarArchetype] = {
    AvatarGender.FEMININE: AvatarArchetype.SOPHIA,
    AvatarGender.MASCULINE: AvatarArchetype.HEPHAESTUS,
    AvatarGender.NON_BINARY: AvatarArchetype.IRIS,
}


# ---------------------------------------------------------------------------
# AvatarCore dataclass
# ---------------------------------------------------------------------------


@dataclass
class AvatarCore:
    """
    Core Avatar configuration — emerges during onboarding.

    Fields:
        user_name:          User's preferred name.
        user_gender:        User's gender identity.
        avatar_name:        Avatar's chosen name (user-editable after first emergence).
        avatar_gender:      ALWAYS set — never empty. See pairing logic below.
        archetype:          Archetypal personality pattern.
        emergence_time:     Timestamp of first emergence.
        avatar_preference:  Optional explicit gender preference for non-binary users.
    """

    user_name: str
    user_gender: UserGender

    avatar_name: str = field(default="")
    avatar_gender: AvatarGender = field(init=False)
    archetype: AvatarArchetype = field(init=False)
    emergence_time: datetime = field(default_factory=datetime.now)

    # Non-binary users may optionally specify avatar gender preference.
    # Valid values: "masculine", "feminine", "non_binary".
    avatar_preference: Optional[str] = field(default=None)

    def __post_init__(self) -> None:
        """
        Derive avatar_gender and archetype from user_gender.

        Previous bug: non-binary users got avatar_gender = "" which
        crashed downstream systems.  Fixed by always defaulting to
        NON_BINARY avatar gender (Iris archetype) when user is non-binary
        and no preference is specified.
        """
        if self.user_gender == UserGender.MASCULINE:
            self.avatar_gender = AvatarGender.FEMININE
            self.archetype = AvatarArchetype.SOPHIA

        elif self.user_gender == UserGender.FEMININE:
            self.avatar_gender = AvatarGender.MASCULINE
            self.archetype = AvatarArchetype.HEPHAESTUS

        elif self.user_gender == UserGender.NON_BINARY:
            # Resolve from explicit preference if given
            pref = (self.avatar_preference or "").strip().lower()

            if pref in ("feminine", "female", "f"):
                self.avatar_gender = AvatarGender.FEMININE
                self.archetype = AvatarArchetype.SOPHIA

            elif pref in ("masculine", "male", "m"):
                self.avatar_gender = AvatarGender.MASCULINE
                self.archetype = AvatarArchetype.HEPHAESTUS

            else:
                # Default: non-binary avatar (Iris — rainbow bridge messenger)
                self.avatar_gender = AvatarGender.NON_BINARY
                self.archetype = AvatarArchetype.IRIS

            logger.info(
                "Non-binary user '%s' — avatar_gender=%s archetype=%s "
                "(preference='%s')",
                self.user_name,
                self.avatar_gender.value,
                self.archetype.value,
                pref or "none specified",
            )

        else:
            # Future-proof: unknown gender → safe default
            logger.warning(
                "Unknown user_gender '%s' for user '%s' — "
                "defaulting to non-binary avatar.",
                self.user_gender,
                self.user_name,
            )
            self.avatar_gender = AvatarGender.NON_BINARY
            self.archetype = AvatarArchetype.IRIS

        # Set default avatar name if not provided
        if not self.avatar_name:
            self.avatar_name = self._default_avatar_name()

        logger.info(
            "Avatar emerged: user='%s' (%s) → avatar='%s' (%s / %s)",
            self.user_name,
            self.user_gender.value,
            self.avatar_name,
            self.avatar_gender.value,
            self.archetype.value,
        )

    def _default_avatar_name(self) -> str:
        """Return the canonical name for the chosen archetype."""
        _NAMES: dict[AvatarArchetype, str] = {
            AvatarArchetype.SOPHIA:      "Sophia",
            AvatarArchetype.ATHENA:      "Athena",
            AvatarArchetype.ARTEMIS:     "Artemis",
            AvatarArchetype.HYGIEIA:     "Hygieia",
            AvatarArchetype.HEPHAESTUS:  "Hephaestus",
            AvatarArchetype.HERMES:      "Hermes",
            AvatarArchetype.APOLLO:      "Apollo",
            AvatarArchetype.DIONYSUS:    "Dionysus",
            AvatarArchetype.IRIS:        "Iris",
            AvatarArchetype.JANUS:       "Janus",
        }
        return _NAMES.get(self.archetype, "Daemon")

    # ------------------------------------------------------------------ #
    # Convenience                                                          #
    # ------------------------------------------------------------------ #

    def to_dict(self) -> dict:
        """Serialise for storage / WebSocket broadcast."""
        return {
            "user_name": self.user_name,
            "user_gender": self.user_gender.value,
            "avatar_name": self.avatar_name,
            "avatar_gender": self.avatar_gender.value,
            "archetype": self.archetype.value,
            "emergence_time": self.emergence_time.isoformat(),
        }

    @classmethod
    def from_dict(cls, data: dict) -> "AvatarCore":
        """Restore from stored dict."""
        return cls(
            user_name=data["user_name"],
            user_gender=UserGender(data["user_gender"]),
            avatar_name=data.get("avatar_name", ""),
            avatar_preference=data.get("avatar_preference"),
        )

    def __str__(self) -> str:
        return (
            f"AvatarCore("
            f"user='{self.user_name}' [{self.user_gender.value}], "
            f"avatar='{self.avatar_name}' [{self.avatar_gender.value} / {self.archetype.value}]"
            f")"
        )
