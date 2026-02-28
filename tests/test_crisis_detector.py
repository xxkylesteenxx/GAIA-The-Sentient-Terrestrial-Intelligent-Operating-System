"""Tests for Crisis Detection System."""

import pytest
from core.safety.crisis_detector import CrisisDetector, CrisisLevel


class TestCrisisDetector:
    """Test crisis detection functions."""
    
    @pytest.fixture
    def detector(self):
        return CrisisDetector()
    
    def test_z_score_none(self, detector):
        """Test no crisis for high Z-score."""
        level = detector.detect_from_z_score(10.0)
        assert level == CrisisLevel.NONE
    
    def test_z_score_critical(self, detector):
        """Test critical crisis for Z < 1.0."""
        level = detector.detect_from_z_score(0.5)
        assert level == CrisisLevel.CRITICAL
    
    def test_z_score_high(self, detector):
        """Test high crisis for Z < 3.0."""
        level = detector.detect_from_z_score(2.0)
        assert level == CrisisLevel.HIGH
    
    def test_z_score_moderate(self, detector):
        """Test moderate crisis for Z < 6.0."""
        level = detector.detect_from_z_score(4.5)
        assert level == CrisisLevel.MODERATE
    
    def test_keyword_critical(self, detector):
        """Test critical keyword detection."""
        text = "I want to kill myself"
        level, matches = detector.detect_from_text(text)
        assert level == CrisisLevel.CRITICAL
        assert len(matches) > 0
    
    def test_keyword_high(self, detector):
        """Test high severity keywords."""
        text = "I feel intense hate and rage towards everything"
        level, matches = detector.detect_from_text(text)
        assert level in [CrisisLevel.HIGH, CrisisLevel.MODERATE]
    
    def test_keyword_moderate(self, detector):
        """Test moderate severity keywords."""
        text = "I'm feeling depressed, anxious, and hopeless"
        level, matches = detector.detect_from_text(text)
        assert level == CrisisLevel.MODERATE
        assert len(matches) >= 3
    
    def test_keyword_none(self, detector):
        """Test no keywords in normal text."""
        text = "I'm having a great day and feeling wonderful"
        level, matches = detector.detect_from_text(text)
        assert level == CrisisLevel.NONE
        assert len(matches) == 0
    
    def test_comprehensive_crisis(self, detector):
        """Test comprehensive detection with multiple signals."""
        result = detector.detect_comprehensive(
            z_score=2.0,
            text="I feel hopeless and want to die",
            history=[5.0, 4.0, 3.0, 2.0]
        )
        
        assert result['level'] in ['CRITICAL', 'HIGH']
        assert result['z_threshold_breach'] is True
        assert len(result['keyword_matches']) > 0
        assert result['trend'] == 'degrading'
        assert result['requires_emergency'] is True
    
    def test_comprehensive_stable(self, detector):
        """Test comprehensive detection in stable state."""
        result = detector.detect_comprehensive(
            z_score=10.0,
            text="I'm feeling balanced and coherent",
            history=[9.0, 9.5, 10.0]
        )
        
        assert result['level'] == 'NONE'
        assert result['z_threshold_breach'] is False
        assert result['trend'] == 'improving'
        assert result['requires_intervention'] is False
    
    def test_response_protocol_critical(self, detector):
        """Test emergency response protocol."""
        protocol = detector.get_response_protocol(CrisisLevel.CRITICAL)
        
        assert protocol['action'] == 'emergency'
        assert protocol['access_level'] == 'locked'
        assert protocol['alert'] is True
        assert '988' in protocol['resources']
    
    def test_response_protocol_none(self, detector):
        """Test normal operation protocol."""
        protocol = detector.get_response_protocol(CrisisLevel.NONE)
        
        assert protocol['action'] == 'continue'
        assert protocol['access_level'] == 'full'
        assert protocol['avatar_mode'] == 'companion'
