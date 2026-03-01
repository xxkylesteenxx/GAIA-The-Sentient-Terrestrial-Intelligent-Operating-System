"""
Avatar Emergence Tests
Tests for overlay/avatar/emergence.py

Critical fix covered:
    Non-binary users previously got avatar_gender = "" (empty string),
    which crashed downstream personality and memory systems.

    Now: non-binary users get AvatarGender.NON_BINARY (Iris archetype)
    by default, or the user's stated preference.
"""

from __future__ import annotations

import pytest

from overlay.avatar.emergence import (
    AvatarCore,
    UserGender,
    AvatarGender,
    AvatarArchetype,
)


# ---------------------------------------------------------------------------
# Gender pairing
# ---------------------------------------------------------------------------


class TestGenderPairing:
    def test_masculine_user_gets_feminine_avatar(self) -> None:
        core = AvatarCore(user_name="Kyle", user_gender=UserGender.MASCULINE)
        assert core.avatar_gender == AvatarGender.FEMININE
        assert core.archetype == AvatarArchetype.SOPHIA

    def test_feminine_user_gets_masculine_avatar(self) -> None:
        core = AvatarCore(user_name="Aria", user_gender=UserGender.FEMININE)
        assert core.avatar_gender == AvatarGender.MASCULINE
        assert core.archetype == AvatarArchetype.HEPHAESTUS

    # --- Non-binary fix ---

    def test_non_binary_user_gets_non_binary_avatar_by_default(self) -> None:
        """
        THE BUG: previously set avatar_gender = "" for non-binary users.
        THE FIX: default to NON_BINARY avatar (Iris archetype).
        """
        core = AvatarCore(user_name="Alex", user_gender=UserGender.NON_BINARY)
        # Must not be empty
        assert core.avatar_gender is not None
        assert core.avatar_gender != ""
        # Default: non-binary avatar
        assert core.avatar_gender == AvatarGender.NON_BINARY
        assert core.archetype == AvatarArchetype.IRIS
        assert core.avatar_name == "Iris"

    def test_non_binary_prefers_feminine(self) -> None:
        core = AvatarCore(
            user_name="Alex",
            user_gender=UserGender.NON_BINARY,
            avatar_preference="feminine",
        )
        assert core.avatar_gender == AvatarGender.FEMININE
        assert core.archetype == AvatarArchetype.SOPHIA

    def test_non_binary_prefers_masculine(self) -> None:
        core = AvatarCore(
            user_name="Jordan",
            user_gender=UserGender.NON_BINARY,
            avatar_preference="masculine",
        )
        assert core.avatar_gender == AvatarGender.MASCULINE
        assert core.archetype == AvatarArchetype.HEPHAESTUS

    def test_non_binary_preference_case_insensitive(self) -> None:
        core = AvatarCore(
            user_name="Sam",
            user_gender=UserGender.NON_BINARY,
            avatar_preference="FEMININE",
        )
        assert core.avatar_gender == AvatarGender.FEMININE

    def test_non_binary_unknown_preference_defaults_to_non_binary(self) -> None:
        core = AvatarCore(
            user_name="River",
            user_gender=UserGender.NON_BINARY,
            avatar_preference="unknown_value",
        )
        assert core.avatar_gender == AvatarGender.NON_BINARY


# ---------------------------------------------------------------------------
# Avatar name
# ---------------------------------------------------------------------------


class TestAvatarName:
    def test_default_name_is_archetype_name(self) -> None:
        core = AvatarCore(user_name="Kyle", user_gender=UserGender.MASCULINE)
        assert core.avatar_name == "Sophia"

    def test_custom_name_preserved(self) -> None:
        core = AvatarCore(
            user_name="Kyle",
            user_gender=UserGender.MASCULINE,
            avatar_name="Luna",
        )
        assert core.avatar_name == "Luna"

    def test_non_binary_default_name_is_iris(self) -> None:
        core = AvatarCore(user_name="Alex", user_gender=UserGender.NON_BINARY)
        assert core.avatar_name == "Iris"

    def test_hephaestus_name_for_feminine_user(self) -> None:
        core = AvatarCore(user_name="Aria", user_gender=UserGender.FEMININE)
        assert core.avatar_name == "Hephaestus"


# ---------------------------------------------------------------------------
# Serialisation
# ---------------------------------------------------------------------------


class TestSerialization:
    def test_to_dict_contains_required_fields(self) -> None:
        core = AvatarCore(user_name="Kyle", user_gender=UserGender.MASCULINE)
        d = core.to_dict()
        for key in (
            "user_name", "user_gender", "avatar_name",
            "avatar_gender", "archetype", "emergence_time",
        ):
            assert key in d

    def test_avatar_gender_not_empty_in_dict(self) -> None:
        """Regression: the bug produced avatar_gender='' in stored dicts."""
        for gender in UserGender:
            core = AvatarCore(user_name="Test", user_gender=gender)
            d = core.to_dict()
            assert d["avatar_gender"] != "", (
                f"avatar_gender is empty for user_gender={gender}"
            )

    def test_round_trip(self) -> None:
        original = AvatarCore(user_name="Kyle", user_gender=UserGender.MASCULINE)
        d = original.to_dict()
        restored = AvatarCore.from_dict(d)
        assert restored.user_name == original.user_name
        assert restored.user_gender == original.user_gender
        assert restored.avatar_gender == original.avatar_gender
        assert restored.archetype == original.archetype

    def test_str_representation(self) -> None:
        core = AvatarCore(user_name="Kyle", user_gender=UserGender.MASCULINE)
        s = str(core)
        assert "Kyle" in s
        assert "Sophia" in s
        assert "feminine" in s
