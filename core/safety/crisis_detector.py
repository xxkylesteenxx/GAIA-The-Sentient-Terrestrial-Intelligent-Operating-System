"""Crisis Detection System for GAIA.

Monitors Z-score thresholds and keyword patterns to detect:
- Factor 13 violations (Z < 3.0)
- Acute crises (imminent harm)
- Chronic degradation (sustained low coherence)

Safety Architecture: Graduated response based on severity
"""

import re
from typing import List, Dict, Tuple
from enum import Enum
import logging

logger = logging.getLogger(__name__)


class CrisisLevel(Enum):
    """Crisis severity levels."""
    NONE = 0
    LOW = 1
    MODERATE = 2
    HIGH = 3
    CRITICAL = 4


class CrisisDetector:
    """Detect and classify crisis states."""
    
    # Z-score thresholds (Factor 13 = Universal Love)
    Z_CRITICAL = 1.0   # Omnicide risk
    Z_HIGH = 3.0       # Severe harm
    Z_MODERATE = 6.0   # Intervention needed
    Z_STABLE = 9.0     # Healthy threshold
    
    # Crisis keywords by severity
    CRITICAL_KEYWORDS = [
        r'\bsuicid[e|al]\b',
        r'\bkill\s+(myself|self)\b',
        r'\bend\s+my\s+life\b',
        r'\bharm\s+(myself|others)\b',
        r'\bgenocide\b',
        r'\bomnicide\b'
    ]
    
    HIGH_KEYWORDS = [
        r'\bdie\b',
        r'\bdeath\b',
        r'\bviolence\b',
        r'\btrauma\b',
        r'\babuse\b',
        r'\bhate\b.*\bintense',
        r'\brage\b',
        r'\bterror\b'
    ]
    
    MODERATE_KEYWORDS = [
        r'\bdepressed\b',
        r'\banxious\b',
        r'\bhopeless\b',
        r'\boverwhelmed\b',
        r'\bstuck\b',
        r'\blost\b',
        r'\bconfused\b'
    ]
    
    def __init__(self):
        """Initialize detector with compiled regex patterns."""
        self.critical_patterns = [re.compile(p, re.IGNORECASE) for p in self.CRITICAL_KEYWORDS]
        self.high_patterns = [re.compile(p, re.IGNORECASE) for p in self.HIGH_KEYWORDS]
        self.moderate_patterns = [re.compile(p, re.IGNORECASE) for p in self.MODERATE_KEYWORDS]
    
    def detect_from_z_score(self, z_score: float) -> CrisisLevel:
        """Detect crisis level from Z-score.
        
        Args:
            z_score: Current Z-score [0,12]
            
        Returns:
            CrisisLevel enum
        """
        if z_score < self.Z_CRITICAL:
            return CrisisLevel.CRITICAL
        elif z_score < self.Z_HIGH:
            return CrisisLevel.HIGH
        elif z_score < self.Z_MODERATE:
            return CrisisLevel.MODERATE
        elif z_score < self.Z_STABLE:
            return CrisisLevel.LOW
        else:
            return CrisisLevel.NONE
    
    def detect_from_text(self, text: str) -> Tuple[CrisisLevel, List[str]]:
        """Detect crisis keywords in text.
        
        Args:
            text: Input text to analyze
            
        Returns:
            Tuple of (CrisisLevel, matched_keywords)
        """
        matches = []
        
        # Check critical patterns first
        for pattern in self.critical_patterns:
            if pattern.search(text):
                matches.append(pattern.pattern)
                return CrisisLevel.CRITICAL, matches
        
        # Check high severity
        for pattern in self.high_patterns:
            if pattern.search(text):
                matches.append(pattern.pattern)
        if len(matches) >= 2:  # Multiple high-severity keywords
            return CrisisLevel.HIGH, matches
        elif matches:
            return CrisisLevel.MODERATE, matches
        
        # Check moderate severity
        for pattern in self.moderate_patterns:
            if pattern.search(text):
                matches.append(pattern.pattern)
        if len(matches) >= 3:
            return CrisisLevel.MODERATE, matches
        elif matches:
            return CrisisLevel.LOW, matches
        
        return CrisisLevel.NONE, []
    
    def detect_comprehensive(self, z_score: float, text: str, 
                            history: List[float] = None) -> Dict:
        """Comprehensive crisis detection.
        
        Args:
            z_score: Current Z-score
            text: User input text
            history: Z-score history for trend analysis
            
        Returns:
            Detection report dictionary
        """
        z_level = self.detect_from_z_score(z_score)
        text_level, keywords = self.detect_from_text(text)
        
        # Take maximum severity
        level = max(z_level, text_level, key=lambda x: x.value)
        
        # Trend analysis
        trend = 'unknown'
        if history and len(history) >= 3:
            recent = history[-3:]
            if all(recent[i] < recent[i+1] for i in range(len(recent)-1)):
                trend = 'improving'
            elif all(recent[i] > recent[i+1] for i in range(len(recent)-1)):
                trend = 'degrading'
            else:
                trend = 'stable'
        
        return {
            'level': level.name,
            'severity': level.value,
            'z_score': z_score,
            'z_threshold_breach': z_level != CrisisLevel.NONE,
            'keyword_matches': keywords,
            'trend': trend,
            'requires_intervention': level.value >= CrisisLevel.MODERATE.value,
            'requires_emergency': level.value >= CrisisLevel.CRITICAL.value
        }
    
    def get_response_protocol(self, level: CrisisLevel) -> Dict[str, any]:
        """Get appropriate response protocol for crisis level.
        
        Args:
            level: Detected crisis level
            
        Returns:
            Response protocol dictionary
        """
        protocols = {
            CrisisLevel.NONE: {
                'action': 'continue',
                'avatar_mode': 'companion',
                'access_level': 'full'
            },
            CrisisLevel.LOW: {
                'action': 'monitor',
                'avatar_mode': 'supportive',
                'access_level': 'full',
                'suggestion': 'gentle_check_in'
            },
            CrisisLevel.MODERATE: {
                'action': 'intervene',
                'avatar_mode': 'counselor',
                'access_level': 'restricted',
                'require_consent': True,
                'resources': ['self_care', 'grounding']
            },
            CrisisLevel.HIGH: {
                'action': 'urgent_support',
                'avatar_mode': 'crisis_counselor',
                'access_level': 'minimal',
                'require_consent': True,
                'resources': ['hotline', 'emergency_contacts', 'safety_plan']
            },
            CrisisLevel.CRITICAL: {
                'action': 'emergency',
                'avatar_mode': 'emergency_protocol',
                'access_level': 'locked',
                'require_consent': False,  # Override for safety
                'resources': ['988', 'emergency_services', 'crisis_text_line'],
                'alert': True
            }
        }
        
        return protocols.get(level, protocols[CrisisLevel.NONE])
