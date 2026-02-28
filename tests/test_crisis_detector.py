"""Tests for crisis detector."""

import pytest
from core.safety import CrisisDetector, CrisisAlert


def test_crisis_detector_init():
    """Test crisis detector initialization."""
    detector = CrisisDetector()
    assert detector.threshold == 2.0
    assert len(detector.alert_history) == 0


def test_zscore_crisis():
    """Test Z-score based crisis detection."""
    detector = CrisisDetector()
    
    # Test critical Z-score
    alert = detector.check(zscore=1.5)
    assert alert is not None
    assert alert.severity >= 2
    assert "crisis" in alert.message.lower()
    
    # Test emergency Z-score
    alert = detector.check(zscore=0.8)
    assert alert is not None
    assert alert.severity == 3


def test_keyword_crisis():
    """Test keyword-based crisis detection."""
    detector = CrisisDetector()
    
    crisis_messages = [
        "I want to kill myself",
        "I can't go on. I want to end it all.",
        "There's no point. I'm done."
    ]
    
    for message in crisis_messages:
        alert = detector.check(zscore=5.0, user_message=message)
        assert alert is not None, f"Failed to detect crisis in: {message}"
        assert alert.severity == 3  # Emergency


def test_warning_keywords():
    """Test warning keyword detection."""
    detector = CrisisDetector()
    
    warning_message = "I'm feeling really depressed and can't cope."
    alert = detector.check(zscore=5.0, user_message=warning_message)
    
    assert alert is not None
    assert alert.severity == 1  # Concern


def test_no_crisis():
    """Test that no crisis is detected for healthy states."""
    detector = CrisisDetector()
    
    alert = detector.check(
        zscore=7.5,
        user_message="I'm feeling good today."
    )
    
    assert alert is None


def test_combined_crisis():
    """Test combined Z-score and keyword crisis."""
    detector = CrisisDetector()
    
    alert = detector.check(
        zscore=1.2,
        user_message="I'm done. No point in going on."
    )
    
    assert alert is not None
    assert alert.severity == 3
    assert len(alert.triggers) >= 2  # Both Z-score and keywords


def test_alert_history():
    """Test that alerts are stored in history."""
    detector = CrisisDetector()
    
    detector.check(zscore=1.5)
    detector.check(zscore=1.8)
    detector.check(zscore=0.9)
    
    history = detector.get_recent_alerts()
    assert len(history) == 3


def test_is_in_crisis():
    """Test quick crisis check."""
    detector = CrisisDetector()
    
    assert detector.is_in_crisis(zscore=1.5) is True
    assert detector.is_in_crisis(zscore=7.5) is False
    assert detector.is_in_crisis(
        zscore=5.0,
        user_message="I want to die"
    ) is True
