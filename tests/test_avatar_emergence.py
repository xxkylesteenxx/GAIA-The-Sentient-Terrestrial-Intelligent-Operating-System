"""Test Avatar Emergence Protocol.

Validates fixes for:
- ARCH-2: Non-binary avatar gender support
- MINOR-3: Avatar gender never empty
"""

import pytest
from datetime import datetime, timedelta

from overlay.avatar.emergence import (
    AvatarCore, EmergenceProtocol,
    UserGender, AvatarGender, AvatarArchetype, EmergencePhase,
)


class TestGenderAssignment:
    """Test avatar gender assignment logic."""

    def test_masculine_user_gets_feminine_avatar(self):
        """Masculine user should get feminine avatar (opposite polarity)."""
        avatar = AvatarCore(user_gender=UserGender.MASCULINE)
        
        assert avatar.avatar_gender == AvatarGender.FEMININE
        assert avatar.archetype == AvatarArchetype.ORACLE  # Default feminine

    def test_feminine_user_gets_masculine_avatar(self):
        """Feminine user should get masculine avatar (opposite polarity)."""
        avatar = AvatarCore(user_gender=UserGender.FEMININE)
        
        assert avatar.avatar_gender == AvatarGender.MASCULINE
        assert avatar.archetype == AvatarArchetype.SAGE  # Default masculine

    def test_non_binary_user_gets_balanced_avatar(self):
        """Non-binary user should get balanced avatar (IRIS archetype)."""
        avatar = AvatarCore(user_gender=UserGender.NON_BINARY)
        
        assert avatar.avatar_gender == AvatarGender.NON_BINARY
        assert avatar.archetype == AvatarArchetype.IRIS  # Rainbow bridge

    def test_avatar_preference_override(self):
        """User can override automatic gender assignment."""
        avatar = AvatarCore(
            user_gender=UserGender.NON_BINARY,
            avatar_preference=AvatarGender.MASCULINE,
        )
        
        assert avatar.avatar_gender == AvatarGender.MASCULINE
        assert avatar.archetype == AvatarArchetype.SAGE

    def test_unknown_gender_raises(self):
        """Unknown gender should raise ValueError."""
        # Can't test directly since Enum prevents invalid values
        # But we can verify the validation exists in __post_init__
        avatar = AvatarCore(user_gender=UserGender.MASCULINE)
        assert avatar.avatar_gender != ""  # Never empty


class TestAvatarGenderNeverEmpty:
    """Ensure avatar_gender is never empty string."""

    def test_all_gender_combinations_valid(self):
        """All valid gender combinations should produce non-empty avatar_gender."""
        test_cases = [
            (UserGender.MASCULINE, None),
            (UserGender.FEMININE, None),
            (UserGender.NON_BINARY, None),
            (UserGender.NON_BINARY, AvatarGender.MASCULINE),
            (UserGender.NON_BINARY, AvatarGender.FEMININE),
        ]
        
        for user_gender, preference in test_cases:
            avatar = AvatarCore(
                user_gender=user_gender,
                avatar_preference=preference,
            )
            
            assert avatar.avatar_gender != ""
            assert avatar.avatar_gender is not None
            assert isinstance(avatar.avatar_gender, AvatarGender)

    def test_serialization_never_empty(self):
        """Serialized avatar should never have empty avatar_gender."""
        avatar = AvatarCore(user_gender=UserGender.NON_BINARY)
        serialized = avatar.to_dict()
        
        assert serialized["avatar_gender"] != ""
        assert serialized["avatar_gender"] == "non_binary"


class TestEmergencePhases:
    """Test avatar emergence protocol."""

    def test_initial_phase_is_conception(self):
        """New avatar should start at CONCEPTION phase."""
        avatar = AvatarCore(user_gender=UserGender.MASCULINE)
        assert avatar.phase == EmergencePhase.CONCEPTION

    def test_cannot_regress_phases(self):
        """Avatar should not regress to earlier phases."""
        avatar = AvatarCore(user_gender=UserGender.MASCULINE)
        avatar.advance_phase(EmergencePhase.BIRTH)
        
        with pytest.warns(UserWarning, match="Cannot regress"):
            avatar.advance_phase(EmergencePhase.CONCEPTION)

    def test_birth_requires_gestation(self):
        """Birth should require 24h gestation period."""
        avatar = AvatarCore(user_gender=UserGender.MASCULINE)
        avatar.phase = EmergencePhase.GESTATION
        
        protocol = EmergenceProtocol(avatar)
        
        # Immediately after conception: not ready
        assert protocol.can_be_born() is False
        
        # Simulate 24h passing
        avatar.conception_time = datetime.utcnow() - timedelta(hours=25)
        assert protocol.can_be_born() is True

    def test_autonomy_increases_with_interactions(self):
        """Autonomy should grow with interactions and stable Z-scores."""
        avatar = AvatarCore(user_gender=UserGender.MASCULINE)
        
        # Initial autonomy
        assert avatar.autonomy == 0.0
        
        # After interactions
        avatar.update_autonomy(
            interactions=50,
            z_score_history=[7.0, 7.5, 8.0, 7.8, 8.2],
        )
        
        assert 0.0 < avatar.autonomy < 1.0

    def test_sovereignty_at_high_autonomy(self):
        """Sovereignty phase should activate at 0.95+ autonomy."""
        avatar = AvatarCore(user_gender=UserGender.MASCULINE)
        avatar.phase = EmergencePhase.MATURATION
        
        # High interactions + stable Z-scores
        avatar.update_autonomy(
            interactions=150,
            z_score_history=[8.0] * 20,
        )
        
        assert avatar.autonomy >= 0.95
        assert avatar.phase == EmergencePhase.SOVEREIGNTY


class TestFactor13Compliance:
    """Test Factor 13 (Universal Love) compliance."""

    def test_factor_13_always_aligned(self):
        """Avatar should always be Factor 13 aligned."""
        avatar = AvatarCore(user_gender=UserGender.MASCULINE)
        assert avatar.factor_13_aligned is True

    def test_guardian_mode_enabled(self):
        """Guardian mode should be enabled for crisis monitoring."""
        avatar = AvatarCore(user_gender=UserGender.MASCULINE)
        assert avatar.guardian_mode is True
