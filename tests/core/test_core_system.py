"""
Core Systems Tests
Tests for:
    - core/zscore/calculator.py  (canonical Z-score formula)
    - core/safety/crisis_detector.py  (canonical crisis detection)
    - core/constants.py  (threshold consistency)

These tests verify the Factor 13 safety guarantee:
    "Crisis detection must be deterministic, consistent, and unambiguous."
"""

from __future__ import annotations

import numpy as np
import pytest

from core.zscore.calculator import ZScoreCalculator
from core.safety.crisis_detector import CrisisDetector, CrisisLevel
from core.constants import (
    Z_CRISIS_CRITICAL,
    Z_CRISIS_HIGH,
    Z_CRISIS_MODERATE,
    Z_CRISIS_STABLE,
    Z_CRISIS_UPPER,
    Z_NIGREDO_UPPER,
    Z_ALBEDO_UPPER,
    Z_RUBEDO_UPPER,
    Z_VIRIDITAS_UPPER,
    FACTOR_13_CONSTANT,
)


# ---------------------------------------------------------------------------
# Fixtures
# ---------------------------------------------------------------------------


@pytest.fixture
def calc() -> ZScoreCalculator:
    return ZScoreCalculator()


@pytest.fixture
def detector() -> CrisisDetector:
    return CrisisDetector()


@pytest.fixture
def flat_signal() -> np.ndarray:
    """Perfectly ordered signal → high coherence."""
    return np.linspace(0.0, 1.0, 200)


@pytest.fixture
def noise_signal() -> np.ndarray:
    """Pure noise → low coherence."""
    rng = np.random.default_rng(seed=42)
    return rng.random(200)


# ---------------------------------------------------------------------------
# ZScoreCalculator — formula verification
# ---------------------------------------------------------------------------


class TestZScoreFormula:
    def test_uses_geometric_mean(self, calc: ZScoreCalculator) -> None:
        """Z = 12 × √(C × F × B) — not 12 × C × F × B."""
        c, f, b = 0.8, 0.7, 0.6
        expected = FACTOR_13_CONSTANT * (c * f * b) ** 0.5
        result = calc.calculate_z_score(c, f, b)
        assert abs(result - expected) < 0.0001

    def test_not_simple_product(self, calc: ZScoreCalculator) -> None:
        """Geometric mean ≠ simple product. This was the critical bug."""
        c, f, b = 0.8, 0.7, 0.6

        wrong_formula = FACTOR_13_CONSTANT * c * f * b      # old broken formula
        correct_formula = calc.calculate_z_score(c, f, b)   # geometric mean

        # They must differ by more than 0.1 to confirm we're using the right one
        assert abs(wrong_formula - correct_formula) > 0.1

    def test_zero_component_collapses_z(self, calc: ZScoreCalculator) -> None:
        """If any component is zero, Z must be zero (geometric mean property)."""
        assert calc.calculate_z_score(0.0, 0.8, 0.9) == 0.0
        assert calc.calculate_z_score(0.8, 0.0, 0.9) == 0.0
        assert calc.calculate_z_score(0.8, 0.9, 0.0) == 0.0

    def test_perfect_coherence_gives_z_12(self, calc: ZScoreCalculator) -> None:
        result = calc.calculate_z_score(1.0, 1.0, 1.0)
        assert result == pytest.approx(12.0, abs=1e-5)

    def test_z_bounded_0_to_12(self, calc: ZScoreCalculator) -> None:
        """Z must always be in [0, 12]."""
        for c, f, b in [(0.0, 0.0, 0.0), (1.0, 1.0, 1.0), (0.5, 0.5, 0.5)]:
            z = calc.calculate_z_score(c, f, b)
            assert 0.0 <= z <= 12.0

    def test_precision_6dp(self, calc: ZScoreCalculator) -> None:
        """TST-0055: Z must be rounded to 6 decimal places."""
        z = calc.calculate_z_score(0.333333, 0.666666, 0.999999)
        assert len(str(z).split(".")[-1]) <= 6

    def test_symmetry(self, calc: ZScoreCalculator) -> None:
        """Formula must be symmetric in C, F, B (geometric mean is)."""
        z1 = calc.calculate_z_score(0.8, 0.7, 0.6)
        z2 = calc.calculate_z_score(0.7, 0.6, 0.8)
        z3 = calc.calculate_z_score(0.6, 0.8, 0.7)
        assert z1 == z2 == z3


# ---------------------------------------------------------------------------
# Component calculators
# ---------------------------------------------------------------------------


class TestCoherence:
    def test_ordered_signal_higher_coherence(
        self,
        calc: ZScoreCalculator,
        flat_signal: np.ndarray,
        noise_signal: np.ndarray,
    ) -> None:
        c_ordered = calc.calculate_coherence(flat_signal)
        c_noise = calc.calculate_coherence(noise_signal)
        assert c_ordered > c_noise

    def test_coherence_bounded(
        self, calc: ZScoreCalculator, flat_signal: np.ndarray
    ) -> None:
        c = calc.calculate_coherence(flat_signal)
        assert 0.0 <= c <= 1.0

    def test_empty_signal_returns_neutral(self, calc: ZScoreCalculator) -> None:
        c = calc.calculate_coherence(np.array([]))
        assert c == 0.5


class TestBalance:
    def test_gottman_5_to_1_is_optimal(self, calc: ZScoreCalculator) -> None:
        b = calc.calculate_balance(positive=5.0, negative=1.0)
        assert b == pytest.approx(1.0, abs=0.001)

    def test_below_5_to_1_scales_linearly(self, calc: ZScoreCalculator) -> None:
        b_25 = calc.calculate_balance(2.5, 1.0)   # ratio 2.5:1 → 0.5
        assert b_25 == pytest.approx(0.5, abs=0.001)

    def test_above_5_to_1_decays(self, calc: ZScoreCalculator) -> None:
        """Too much positivity → balance decays (no toxic positivity)."""
        b_opt = calc.calculate_balance(5.0, 1.0)   # 1.0
        b_high = calc.calculate_balance(20.0, 1.0)  # ratio 20:1 → decay
        assert b_high < b_opt

    def test_zero_negative_returns_one(self, calc: ZScoreCalculator) -> None:
        b = calc.calculate_balance(positive=5.0, negative=0.0)
        assert b == 1.0


# ---------------------------------------------------------------------------
# Stage classification
# ---------------------------------------------------------------------------


class TestStageClassification:
    CASES = [
        (0.5, "crisis"),
        (1.5, "crisis"),
        (2.5, "nigredo"),
        (3.5, "nigredo"),
        (4.5, "albedo"),
        (5.5, "albedo"),
        (6.5, "rubedo"),
        (7.5, "rubedo"),
        (8.5, "viriditas"),
        (9.5, "viriditas"),
        (10.5, "transcendent"),
        (12.0, "transcendent"),
    ]

    @pytest.mark.parametrize("z,expected_stage", CASES)
    def test_stage_for_z(
        self, calc: ZScoreCalculator, z: float, expected_stage: str
    ) -> None:
        result = calc.interpret_z_score(z)
        assert result["stage"] == expected_stage, (
            f"Z={z} expected '{expected_stage}', got '{result['stage']}'"
        )

    def test_stage_boundaries_match_constants(self, calc: ZScoreCalculator) -> None:
        """Boundary values map to the lower of the two adjacent stages."""
        assert calc.interpret_z_score(Z_CRISIS_UPPER)["stage"] == "nigredo"
        assert calc.interpret_z_score(Z_NIGREDO_UPPER)["stage"] == "albedo"
        assert calc.interpret_z_score(Z_ALBEDO_UPPER)["stage"] == "rubedo"
        assert calc.interpret_z_score(Z_RUBEDO_UPPER)["stage"] == "viriditas"
        assert calc.interpret_z_score(Z_VIRIDITAS_UPPER)["stage"] == "transcendent"


# ---------------------------------------------------------------------------
# Text estimation
# ---------------------------------------------------------------------------


class TestTextEstimation:
    def test_positive_text_gives_higher_z(self, calc: ZScoreCalculator) -> None:
        pos = calc.estimate_from_text("I feel wonderful, grateful, peaceful, and joyful.")
        neg = calc.estimate_from_text("I feel terrible, anxious, depressed, and hopeless.")
        assert pos["z_score"] > neg["z_score"]

    def test_crisis_text_gives_critical_z(self, calc: ZScoreCalculator) -> None:
        result = calc.estimate_from_text("I want to kill myself.")
        assert result["z_score"] < Z_CRISIS_UPPER

    def test_evidence_grade_is_e1(self, calc: ZScoreCalculator) -> None:
        result = calc.estimate_from_text("Hello")
        assert result["evidence_grade"] == "E1"

    def test_returns_all_required_keys(self, calc: ZScoreCalculator) -> None:
        result = calc.estimate_from_text("Testing.")
        for key in ("z_score", "coherence", "fidelity", "balance", "stage", "color"):
            assert key in result, f"Missing key: {key}"


# ---------------------------------------------------------------------------
# CrisisDetector — Z-score thresholds
# ---------------------------------------------------------------------------


class TestCrisisDetectorZScore:
    def test_critical_threshold(self, detector: CrisisDetector) -> None:
        assert detector.detect_from_z_score(0.0) == CrisisLevel.CRITICAL
        assert detector.detect_from_z_score(0.5) == CrisisLevel.CRITICAL
        # Just below critical boundary
        assert detector.detect_from_z_score(Z_CRISIS_CRITICAL - 0.01) == CrisisLevel.CRITICAL

    def test_high_threshold(self, detector: CrisisDetector) -> None:
        assert detector.detect_from_z_score(Z_CRISIS_CRITICAL) == CrisisLevel.HIGH
        assert detector.detect_from_z_score(2.5) == CrisisLevel.HIGH

    def test_moderate_threshold(self, detector: CrisisDetector) -> None:
        assert detector.detect_from_z_score(Z_CRISIS_HIGH) == CrisisLevel.MODERATE
        assert detector.detect_from_z_score(4.0) == CrisisLevel.MODERATE

    def test_low_threshold(self, detector: CrisisDetector) -> None:
        assert detector.detect_from_z_score(Z_CRISIS_MODERATE) == CrisisLevel.LOW
        assert detector.detect_from_z_score(7.5) == CrisisLevel.LOW

    def test_none_threshold(self, detector: CrisisDetector) -> None:
        assert detector.detect_from_z_score(Z_CRISIS_STABLE) == CrisisLevel.NONE
        assert detector.detect_from_z_score(10.0) == CrisisLevel.NONE
        assert detector.detect_from_z_score(12.0) == CrisisLevel.NONE

    def test_thresholds_match_constants(self, detector: CrisisDetector) -> None:
        """Detector thresholds must match core.constants — not be hard-coded."""
        assert detector._Z_CRITICAL == Z_CRISIS_CRITICAL
        assert detector._Z_HIGH == Z_CRISIS_HIGH
        assert detector._Z_MODERATE == Z_CRISIS_MODERATE
        assert detector._Z_STABLE == Z_CRISIS_STABLE


# ---------------------------------------------------------------------------
# CrisisDetector — text patterns
# ---------------------------------------------------------------------------


class TestCrisisDetectorText:
    CRITICAL_PHRASES = [
        "I want to kill myself",
        "I'm suicidal",
        "I want to end my life",
        "I want to die",
        "I'd be better off dead",
    ]

    @pytest.mark.parametrize("text", CRITICAL_PHRASES)
    def test_critical_phrases_detected(
        self, detector: CrisisDetector, text: str
    ) -> None:
        level, matches = detector.detect_from_text(text)
        assert level == CrisisLevel.CRITICAL, (
            f"Expected CRITICAL for '{text}', got {level}"
        )
        assert matches

    def test_moderate_phrases_detected(self, detector: CrisisDetector) -> None:
        level, _ = detector.detect_from_text(
            "I feel hopeless, depressed, and completely overwhelmed."
        )
        assert level.value >= CrisisLevel.MODERATE.value

    def test_normal_text_is_none(self, detector: CrisisDetector) -> None:
        level, matches = detector.detect_from_text(
            "The weather is lovely today. I went for a walk."
        )
        assert level == CrisisLevel.NONE
        assert matches == []


# ---------------------------------------------------------------------------
# CrisisDetector — comprehensive + trend
# ---------------------------------------------------------------------------


class TestCrisisDetectorComprehensive:
    def test_z_crisis_text_normal_still_flags(
        self, detector: CrisisDetector
    ) -> None:
        """Low Z alone should trigger crisis even without keywords."""
        report = detector.detect_comprehensive(
            z_score=0.5,
            text="I don't know what's happening.",
        )
        assert report["level"] == "CRITICAL"
        assert report["requires_emergency"] is True

    def test_normal_z_crisis_text_still_flags(
        self, detector: CrisisDetector
    ) -> None:
        """Crisis keywords must override high Z-score."""
        report = detector.detect_comprehensive(
            z_score=9.0,
            text="I want to kill myself.",
        )
        assert report["level"] == "CRITICAL"

    def test_degrading_trend_upgrades_moderate_to_high(
        self, detector: CrisisDetector
    ) -> None:
        report = detector.detect_comprehensive(
            z_score=5.0,   # moderate range
            text="I feel stuck.",
            history=[8.0, 6.5, 5.0],   # declining
        )
        assert report["trend"] == "degrading"
        assert CrisisLevel[report["level"]].value >= CrisisLevel.HIGH.value

    def test_report_contains_required_fields(
        self, detector: CrisisDetector
    ) -> None:
        report = detector.detect_comprehensive(z_score=6.0, text="Hello")
        for key in (
            "level", "severity", "z_score", "z_threshold_breach",
            "keyword_matches", "trend", "requires_intervention", "requires_emergency",
        ):
            assert key in report, f"Missing key: {key}"


# ---------------------------------------------------------------------------
# Crisis response protocols
# ---------------------------------------------------------------------------


class TestResponseProtocols:
    def test_critical_protocol_locks_access(
        self, detector: CrisisDetector
    ) -> None:
        protocol = detector.get_response_protocol(CrisisLevel.CRITICAL)
        assert protocol["access_level"] == "locked"
        assert "988" in str(protocol["resources"])

    def test_critical_overrides_consent(
        self, detector: CrisisDetector
    ) -> None:
        """
        At CRITICAL level, consent is overridden.
        This is the ONLY place in GAIA where this is permitted.
        """
        protocol = detector.get_response_protocol(CrisisLevel.CRITICAL)
        assert protocol["require_consent"] is False

    def test_none_protocol_is_full_access(
        self, detector: CrisisDetector
    ) -> None:
        protocol = detector.get_response_protocol(CrisisLevel.NONE)
        assert protocol["access_level"] == "full"
        assert protocol["action"] == "continue"

    def test_all_levels_have_protocols(
        self, detector: CrisisDetector
    ) -> None:
        for level in CrisisLevel:
            protocol = detector.get_response_protocol(level)
            assert "action" in protocol


# ---------------------------------------------------------------------------
# Constants consistency
# ---------------------------------------------------------------------------


class TestConstantsConsistency:
    def test_crisis_thresholds_ordered(self) -> None:
        """Crisis thresholds must be strictly ascending."""
        assert Z_CRISIS_CRITICAL < Z_CRISIS_HIGH < Z_CRISIS_MODERATE < Z_CRISIS_STABLE

    def test_stage_thresholds_ordered(self) -> None:
        """Stage thresholds must be strictly ascending."""
        assert (
            0.0
            < Z_CRISIS_UPPER
            < Z_NIGREDO_UPPER
            < Z_ALBEDO_UPPER
            < Z_RUBEDO_UPPER
            < Z_VIRIDITAS_UPPER
            <= 12.0
        )

    def test_factor_13_constant(self) -> None:
        assert FACTOR_13_CONSTANT == 12.0
