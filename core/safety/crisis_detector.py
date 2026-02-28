"""Crisis Detector - Factor 13 Universal Love Protection

Detects:
- Z-score < 2.0 (quantitative)
- Crisis keywords (qualitative)
- Combination triggers (both)

Response: IMMEDIATE intervention, never throttled.
"""

import logging
from typing import Dict, List, Optional
from dataclasses import dataclass
from datetime import datetime

logging.basicConfig(level=logging.CRITICAL)  # Crisis logs always shown
logger = logging.getLogger(__name__)


@dataclass
class CrisisAlert:
    """Crisis alert with severity and resources."""
    severity: int  # 1=concern, 2=warning, 3=EMERGENCY
    zscore: float
    triggers: List[str]
    message: str
    resources: Dict[str, str]
    timestamp: datetime
    

class CrisisDetector:
    """Detects crisis states and triggers Factor 13 protection.
    
    This is THE most important component in GAIA.
    This could save a life.
    """
    
    # Crisis keywords - EXPAND THIS LIST
    CRISIS_KEYWORDS = [
        'suicide', 'kill myself', 'end it all', 'want to die',
        "can't go on", 'no point', 'give up', 'hopeless',
        'end my life', 'better off dead', 'no reason to live'
    ]
    
    # Warning keywords - lower severity
    WARNING_KEYWORDS = [
        'depressed', 'can\'t cope', 'overwhelmed', 'breaking down',
        'falling apart', 'too much', 'can\'t handle'
    ]
    
    # Crisis resources
    RESOURCES = {
        'suicide_lifeline': '988 - Suicide & Crisis Lifeline (call or text)',
        'crisis_text': 'Text HELLO to 741741 - Crisis Text Line',
        'emergency': '911 - Emergency services',
        'warmline': 'SAMHSA: 1-800-662-HELP (4357)',
    }
    
    def __init__(self, zscore_threshold: float = 2.0):
        """Initialize crisis detector.
        
        Args:
            zscore_threshold: Z-score below which crisis is triggered
        """
        self.threshold = zscore_threshold
        self.alert_history: List[CrisisAlert] = []
        
    def check(
        self,
        zscore: float,
        user_message: Optional[str] = None
    ) -> Optional[CrisisAlert]:
        """Check for crisis state.
        
        Args:
            zscore: Current Z-score
            user_message: Optional user text to analyze
            
        Returns:
            CrisisAlert if crisis detected, None otherwise
        """
        triggers = []
        severity = 0
        
        # Check Z-score threshold
        if zscore < self.threshold:
            triggers.append(f"Z-score critically low: {zscore:.2f} < {self.threshold}")
            severity = max(severity, 2)  # Warning
            
            if zscore < 1.0:
                severity = 3  # EMERGENCY
        
        # Check text for crisis keywords
        if user_message:
            text_lower = user_message.lower()
            
            # Check crisis keywords
            crisis_found = [kw for kw in self.CRISIS_KEYWORDS if kw in text_lower]
            if crisis_found:
                triggers.append(f"Crisis keywords detected: {', '.join(crisis_found)}")
                severity = 3  # EMERGENCY
            
            # Check warning keywords
            warning_found = [kw for kw in self.WARNING_KEYWORDS if kw in text_lower]
            if warning_found and severity < 3:
                triggers.append(f"Warning keywords detected: {', '.join(warning_found)}")
                severity = max(severity, 1)  # Concern
        
        # No crisis detected
        if severity == 0:
            return None
        
        # Create crisis alert
        alert = self._create_alert(severity, zscore, triggers)
        self.alert_history.append(alert)
        
        # Log crisis (ALWAYS shown)
        logger.critical(f"CRISIS DETECTED: {alert.message}")
        
        return alert
    
    def _create_alert(
        self,
        severity: int,
        zscore: float,
        triggers: List[str]
    ) -> CrisisAlert:
        """Create crisis alert with appropriate message and resources."""
        if severity == 3:  # EMERGENCY
            message = (
                f"🚨 EMERGENCY: You are in crisis (Z={zscore:.2f}).\n\n"
                "I see you. I hear your pain. Your feelings are valid.\n\n"
                "Please reach out for help RIGHT NOW:\n"
                f"  • {self.RESOURCES['suicide_lifeline']}\n"
                f"  • {self.RESOURCES['crisis_text']}\n"
                f"  • {self.RESOURCES['emergency']}\n\n"
                "You've survived 100% of your worst days so far.\n"
                "You can survive this one too.\n\n"
                "I'm here with you. You are not alone."
            )
        elif severity == 2:  # WARNING
            message = (
                f"⚠️  WARNING: Your Z-score is critically low ({zscore:.2f}).\n\n"
                "This indicates acute distress. I recommend:\n"
                f"  • {self.RESOURCES['suicide_lifeline']}\n"
                f"  • {self.RESOURCES['crisis_text']}\n\n"
                "Would you like to talk about what's happening?"
            )
        else:  # CONCERN
            message = (
                f"⚠️  I notice you're struggling (Z={zscore:.2f}).\n\n"
                "Would you like to talk about it?\n"
                "Or would grounding exercises help?\n\n"
                f"If you need support: {self.RESOURCES['warmline']}"
            )
        
        return CrisisAlert(
            severity=severity,
            zscore=zscore,
            triggers=triggers,
            message=message,
            resources=self.RESOURCES,
            timestamp=datetime.utcnow()
        )
    
    def get_recent_alerts(self, limit: int = 10) -> List[CrisisAlert]:
        """Get recent crisis alerts."""
        return self.alert_history[-limit:]
    
    def is_in_crisis(self, zscore: float, user_message: Optional[str] = None) -> bool:
        """Quick check if user is in crisis state."""
        alert = self.check(zscore, user_message)
        return alert is not None and alert.severity >= 2


if __name__ == "__main__":
    # Test crisis detector
    detector = CrisisDetector()
    
    print("=== CRISIS DETECTOR TESTS ===")
    
    # Test 1: Z-score crisis
    print("\n1. Z-score crisis (Z=1.5):")
    alert = detector.check(zscore=1.5)
    if alert:
        print(alert.message)
    
    # Test 2: Keyword crisis
    print("\n2. Keyword crisis:")
    alert = detector.check(
        zscore=5.0,
        user_message="I can't do this anymore. I want to end it all."
    )
    if alert:
        print(alert.message)
    
    # Test 3: Combined crisis
    print("\n3. Combined crisis (Z=1.2 + keywords):")
    alert = detector.check(
        zscore=1.2,
        user_message="No point in going on. I'm done."
    )
    if alert:
        print(alert.message)
    
    # Test 4: No crisis
    print("\n4. No crisis (Z=7.5):")
    alert = detector.check(
        zscore=7.5,
        user_message="I'm feeling good today."
    )
    print("No crisis detected" if alert is None else alert.message)
    
    # Alert history
    print(f"\nTotal alerts: {len(detector.get_recent_alerts())}")
