"""Test Core Systems - Z-Score Calculator and Crisis Detector.

Validates fixes for:
- CRITICAL-1: Z formula split identity
- CRITICAL-2: Duplicate CrisisDetector
- ARCH-1: Alchemical threshold consistency
"""

import pytest
import os
import warnings

from core.zscore.calculator import ZScoreCalculator, ZScoreResult, calculate_z_score
from core.safety.crisis_detector import CrisisDetector, CrisisAlert
from core.constants import (
    Z_CRISIS, Z_NIGREDO, Z_ALBEDO, Z_RUBEDO, Z_VIRIDITAS, Z_TRANSCENDENT,
    CRISIS_CRITICAL, CRISIS_HIGH, CRISIS_MODERATE,
    AlchemicalStage, CrisisLevel,
)


class TestZScoreFormula:
    """Test Z-score calculator consistency and correctness."""

    def test_geometric_mean_formula(self):
        """Validate geometric mean formula: Z = 12 × √(C × F × B)"""
        calc = ZScoreCalculator()
        result = calc.calculate(order=0.8, freedom=0.7, balance=0.6)
        
        # Expected: 12 × √(0.8 × 0.7 × 0.6) = 12 × √0.336 = 12 × 0.58 = 6.95
        expected = 12 * (0.8 * 0.7 * 0.6) ** 0.5
        assert abs(result.z_score - expected) < 0.01
        assert result.z_score == pytest.approx(6.95, rel=0.01)

    def test_single_z_calculator_exists(self):
        """Ensure only ONE canonical Z-score calculator exists."""
        calc_files = []
        for root, dirs, files in os.walk('core'):
            for file in files:
                if file.endswith('.py'):
                    path = os.path.join(root, file)
                    with open(path, 'r') as f:
                        content = f.read()
                        if 'def calculate_z_score' in content and 'calculator.py' in path:
                            calc_files.append(path)
        
        # Should only be core/zscore/calculator.py
        assert len(calc_files) == 1, f"Multiple Z calculators found: {calc_files}"
        assert 'zscore/calculator.py' in calc_files[0]

    def test_deprecated_module_warns(self):
        """Deprecated core.z_calculator should warn."""
        with warnings.catch_warnings(record=True) as w:
            warnings.simplefilter("always")
            from core.z_calculator import ZScoreCalculator as DeprecatedCalc
            
            assert len(w) == 1
            assert issubclass(w[0].category, DeprecationWarning)
            assert "core.z_calculator is deprecated" in str(w[0].message)

    def test_convenience_function(self):
        """Test calculate_z_score convenience function."""
        z = calculate_z_score(0.8, 0.7, 0.6)
        assert z == pytest.approx(6.95, rel=0.01)

    def test_component_validation(self):
        """Test that invalid components raise ValueError."""
        calc = ZScoreCalculator()
        
        with pytest.raises(ValueError, match="outside valid range"):
            calc.calculate(order=1.5, freedom=0.7, balance=0.6)  # order > 1
        
        with pytest.raises(ValueError, match="outside valid range"):
            calc.calculate(order=0.8, freedom=-0.1, balance=0.6)  # freedom < 0


class TestCrisisDetector:
    """Test crisis detector consistency and Factor 13 compliance."""

    def test_single_crisis_detector_exists(self):
        """Ensure only ONE canonical CrisisDetector (plus deprecation shim)."""
        detector_files = []
        for root, dirs, files in os.walk('.'):
            if '__pycache__' in root:
                continue
            for file in files:
                if file.endswith('.py'):
                    path = os.path.join(root, file)
                    with open(path, 'r') as f:
                        content = f.read()
                        if 'class CrisisDetector' in content:
                            detector_files.append(path)
        
        # Should be 2: canonical + deprecation shim
        assert len(detector_files) <= 2, f"Too many CrisisDetectors: {detector_files}"
        assert any('core/safety/crisis_detector.py' in f for f in detector_files)

    def test_crisis_thresholds_from_constants(self):
        """Validate crisis thresholds come from core.constants."""
        detector = CrisisDetector()
        
        assert detector.critical_threshold == CRISIS_CRITICAL
        assert detector.high_threshold == CRISIS_HIGH
        assert detector.moderate_threshold == CRISIS_MODERATE

    def test_crisis_levels(self):
        """Test crisis level detection at key thresholds."""
        detector = CrisisDetector()
        
        # CRITICAL: Z < 1.0
        alert = detector.detect(0.5)
        assert alert.level == CrisisLevel.CRITICAL
        assert alert.intervention_required is True
        assert "988" in " ".join(alert.resources)
        
        # HIGH: Z < 3.0
        alert = detector.detect(2.5)
        assert alert.level == CrisisLevel.HIGH
        assert alert.intervention_required is False
        
        # MODERATE: Z < 6.0
        alert = detector.detect(5.5)
        assert alert.level == CrisisLevel.MODERATE
        
        # NORMAL: Z >= 6.0
        alert = detector.detect(7.0)
        assert alert.level == CrisisLevel.NORMAL
        assert alert.intervention_required is False

    def test_deprecated_crisis_detection_warns(self):
        """Deprecated bridge.safety.crisis_detection should warn."""
        with warnings.catch_warnings(record=True) as w:
            warnings.simplefilter("always")
            from bridge.safety.crisis_detection import CrisisDetector as DeprecatedDetector
            
            assert len(w) == 1
            assert issubclass(w[0].category, DeprecationWarning)
            assert "crisis_detection is deprecated" in str(w[0].message)


class TestAlchemicalConstants:
    """Test alchemical stage constants consistency."""

    def test_equal_stage_intervals(self):
        """All alchemical stages should have equal 2-point intervals."""
        assert Z_NIGREDO - Z_CRISIS == 2.0
        assert Z_ALBEDO - Z_NIGREDO == 2.0
        assert Z_RUBEDO - Z_ALBEDO == 2.0
        assert Z_VIRIDITAS - Z_RUBEDO == 2.0
        assert Z_TRANSCENDENT - Z_VIRIDITAS == 2.0

    def test_no_hardcoded_thresholds(self):
        """No files should hard-code Z thresholds outside core/constants.py."""
        violations = []
        for root, dirs, files in os.walk('.'):
            if '__pycache__' in root or 'test' in root:
                continue
            for file in files:
                if file.endswith('.py') and file != 'constants.py':
                    path = os.path.join(root, file)
                    with open(path, 'r') as f:
                        content = f.read()
                        # Look for patterns like Z_NIGREDO = 4.0
                        if 'Z_NIGREDO' in content and '=' in content and 'import' not in content:
                            lines = content.split('\n')
                            for line in lines:
                                if 'Z_NIGREDO' in line and '=' in line and 'import' not in line:
                                    violations.append(f"{path}: {line.strip()}")
        
        assert len(violations) == 0, f"Hard-coded thresholds found: {violations}"

    def test_alchemical_stage_from_z_score(self):
        """Test AlchemicalStage.from_z_score() classification."""
        assert AlchemicalStage.from_z_score(1.5) == AlchemicalStage.CRISIS
        assert AlchemicalStage.from_z_score(3.0) == AlchemicalStage.NIGREDO
        assert AlchemicalStage.from_z_score(5.0) == AlchemicalStage.ALBEDO
        assert AlchemicalStage.from_z_score(7.0) == AlchemicalStage.RUBEDO
        assert AlchemicalStage.from_z_score(9.0) == AlchemicalStage.VIRIDITAS
        assert AlchemicalStage.from_z_score(11.0) == AlchemicalStage.TRANSCENDENT


class TestIntegration:
    """Integration tests for Z-score and crisis detection."""

    def test_end_to_end_crisis_detection(self):
        """Test full pipeline: calculate Z → detect crisis."""
        calc = ZScoreCalculator()
        detector = CrisisDetector()
        
        # Simulate crisis state
        result = calc.calculate(order=0.3, freedom=0.2, balance=0.2)
        alert = detector.detect(result.z_score)
        
        assert result.z_score < CRISIS_CRITICAL
        assert alert.level == CrisisLevel.CRITICAL
        assert alert.intervention_required is True

    def test_z_score_result_consistency(self):
        """ZScoreResult should match CrisisLevel classification."""
        calc = ZScoreCalculator()
        result = calc.calculate(order=0.5, freedom=0.5, balance=0.5)
        
        # Result should include crisis level
        assert result.crisis_level == CrisisLevel.from_z_score(result.z_score)
        assert result.stage == AlchemicalStage.from_z_score(result.z_score)
