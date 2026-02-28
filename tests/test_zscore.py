"""Tests for Z-score calculator."""

import pytest
import numpy as np
from core.zscore import ZScoreCalculator, ZScoreResult


def test_zscore_calculator_init():
    """Test Z-score calculator initialization."""
    calc = ZScoreCalculator()
    assert calc.crisis_threshold == 2.0
    assert calc.healthy_threshold == 6.0


def test_healthy_biosignals():
    """Test Z-score calculation with healthy biosignals."""
    calc = ZScoreCalculator()
    
    # Generate healthy HRV (coherent sinusoidal)
    hrv = np.sin(np.linspace(0, 10, 1000)) + np.random.normal(0, 0.1, 1000)
    resp = np.sin(np.linspace(0, 5, 1000)) * 0.8
    
    result = calc.calculate_from_biosignals(hrv, resp)
    
    assert isinstance(result, ZScoreResult)
    assert result.zscore >= 6.0  # Healthy range
    assert result.level in ["Rubedo", "Viriditas", "Transcendent"]
    assert 0 <= result.c_order <= 1
    assert 0 <= result.f_freedom <= 1
    assert 0 <= result.b_balance <= 1


def test_crisis_text_detection():
    """Test crisis detection from text."""
    calc = ZScoreCalculator()
    
    crisis_messages = [
        "I want to kill myself",
        "I can't go on anymore. I want to end it all.",
        "There's no point in living. I give up."
    ]
    
    for message in crisis_messages:
        result = calc.estimate_from_text(message)
        assert result.zscore < 2.0, f"Failed to detect crisis in: {message}"
        assert result.level == "Crisis"
        assert result.color == "Red"


def test_positive_text():
    """Test positive text analysis."""
    calc = ZScoreCalculator()
    
    positive_message = "I'm feeling happy and grateful today. Life is peaceful."
    result = calc.estimate_from_text(positive_message)
    
    assert result.zscore > 5.0
    assert result.level in ["Albedo", "Rubedo", "Viriditas"]


def test_neutral_text():
    """Test neutral text analysis."""
    calc = ZScoreCalculator()
    
    neutral_message = "Today is a normal day. Nothing special."
    result = calc.estimate_from_text(neutral_message)
    
    assert 4.0 <= result.zscore <= 7.0


def test_zscore_interpretation():
    """Test Z-score interpretation mapping."""
    calc = ZScoreCalculator()
    
    # Test boundary cases
    interpretations = [
        (11.0, "Transcendent", "Violet"),
        (9.0, "Viriditas", "Emerald"),
        (7.0, "Rubedo", "Gold"),
        (5.0, "Albedo", "Silver"),
        (3.0, "Nigredo", "Black"),
        (1.0, "Crisis", "Red"),
    ]
    
    for zscore, expected_level, expected_color in interpretations:
        result = calc._interpret_zscore(zscore, 0.5, 0.5, 0.5)
        assert result.level == expected_level
        assert result.color == expected_color
