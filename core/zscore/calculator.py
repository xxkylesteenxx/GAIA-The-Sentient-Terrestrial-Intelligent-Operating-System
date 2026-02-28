"""Z-Score Calculator - Core Coherence Measurement

Z = 12 × √(C × F × B)
- C: Order (Shannon entropy of HRV)
- F: Freedom (Lyapunov exponent)
- B: Balance (symmetry index)

Range: -12 (omnicide) to +12 (primordial unity)
"""

import numpy as np
from dataclasses import dataclass
from typing import Optional, Dict
import logging

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)


@dataclass
class ZScoreResult:
    """Result of Z-score calculation."""
    zscore: float
    c_order: float
    f_freedom: float
    b_balance: float
    level: str
    color: str
    stage: str
    

class ZScoreCalculator:
    """Calculates coherence Z-score from biosignals or text."""
    
    def __init__(self):
        self.crisis_threshold = 2.0
        self.healthy_threshold = 6.0
        
    def calculate_from_biosignals(
        self,
        hrv_signal: np.ndarray,
        respiratory_signal: Optional[np.ndarray] = None
    ) -> ZScoreResult:
        """Calculate Z-score from HRV and respiratory biosignals.
        
        Args:
            hrv_signal: Heart rate variability time series
            respiratory_signal: Breath amplitude time series
            
        Returns:
            ZScoreResult with components and interpretation
        """
        # C: Order - Shannon Entropy (inverted for coherence)
        c_order = self._calculate_order(hrv_signal)
        
        # F: Freedom - Lyapunov Exponent (edge of chaos = optimal)
        f_freedom = self._calculate_freedom(hrv_signal)
        
        # B: Balance - Symmetry Index
        if respiratory_signal is not None:
            b_balance = self._calculate_balance(respiratory_signal)
        else:
            b_balance = 0.5  # Neutral if no respiratory data
            
        # Z = 12 × √(C × F × B)
        zscore = 12 * np.sqrt(c_order * f_freedom * b_balance)
        
        return self._interpret_zscore(zscore, c_order, f_freedom, b_balance)
    
    def estimate_from_text(self, text: str) -> ZScoreResult:
        """Estimate Z-score from text sentiment analysis.
        
        Args:
            text: User message to analyze
            
        Returns:
            ZScoreResult with estimated components
        """
        # Crisis keywords detection
        crisis_keywords = [
            'suicide', 'kill myself', 'end it all', 'want to die',
            'can\'t go on', 'no point', 'give up', 'hopeless'
        ]
        
        text_lower = text.lower()
        
        # Check for crisis
        if any(kw in text_lower for kw in crisis_keywords):
            return self._interpret_zscore(0.5, 0.1, 0.1, 0.1)
        
        # Positive indicators
        positive_keywords = ['happy', 'grateful', 'love', 'joy', 'peace', 'excited']
        positive_count = sum(1 for kw in positive_keywords if kw in text_lower)
        
        # Negative indicators
        negative_keywords = ['sad', 'angry', 'depressed', 'anxious', 'worried', 'stressed']
        negative_count = sum(1 for kw in negative_keywords if kw in text_lower)
        
        # Estimate components
        c_order = 0.5 + (positive_count * 0.1) - (negative_count * 0.1)
        f_freedom = 0.5 + (positive_count * 0.08) - (negative_count * 0.12)
        b_balance = 0.5 + (positive_count * 0.12) - (negative_count * 0.08)
        
        # Clamp to [0, 1]
        c_order = max(0, min(1, c_order))
        f_freedom = max(0, min(1, f_freedom))
        b_balance = max(0, min(1, b_balance))
        
        zscore = 12 * np.sqrt(c_order * f_freedom * b_balance)
        
        return self._interpret_zscore(zscore, c_order, f_freedom, b_balance)
    
    def _calculate_order(self, signal: np.ndarray) -> float:
        """Calculate order from Shannon entropy (inverted)."""
        # Histogram of signal values
        hist, _ = np.histogram(signal, bins=20, density=True)
        hist = hist[hist > 0]  # Remove zero bins
        
        # Shannon entropy: H = -Σ p(x) log(p(x))
        entropy = -np.sum(hist * np.log2(hist + 1e-10))
        
        # Normalize to [0, 1] and invert (high coherence = low entropy)
        max_entropy = np.log2(20)  # Maximum for 20 bins
        order = 1.0 - (entropy / max_entropy)
        
        return max(0, min(1, order))
    
    def _calculate_freedom(self, signal: np.ndarray) -> float:
        """Calculate freedom from Lyapunov exponent approximation."""
        # Simplified Lyapunov: rate of divergence of nearby trajectories
        diffs = np.diff(signal)
        
        # Positive = chaotic, Negative = too rigid, ~0 = edge of chaos (optimal)
        lyapunov = np.mean(np.abs(diffs)) / (np.std(signal) + 1e-10)
        
        # Optimal around 0.5 (edge of chaos)
        freedom = 1.0 - np.abs(lyapunov - 0.5) * 2
        
        return max(0, min(1, freedom))
    
    def _calculate_balance(self, respiratory_signal: np.ndarray) -> float:
        """Calculate balance from respiratory symmetry."""
        # Find peaks (inhalations) and troughs (exhalations)
        mean_amp = np.mean(respiratory_signal)
        peaks = respiratory_signal[respiratory_signal > mean_amp]
        troughs = respiratory_signal[respiratory_signal < mean_amp]
        
        if len(peaks) == 0 or len(troughs) == 0:
            return 0.5
        
        # Symmetry: how similar are inhale/exhale amplitudes
        peak_mean = np.mean(peaks)
        trough_mean = np.abs(np.mean(troughs))
        
        symmetry = 1.0 - np.abs(peak_mean - trough_mean) / (peak_mean + trough_mean + 1e-10)
        
        return max(0, min(1, symmetry))
    
    def _interpret_zscore(
        self,
        zscore: float,
        c: float,
        f: float,
        b: float
    ) -> ZScoreResult:
        """Interpret Z-score into alchemical stages and colors."""
        if zscore >= 10:
            level = "Transcendent"
            color = "Violet"
            stage = "Peak flow state"
        elif zscore >= 8:
            level = "Viriditas"
            color = "Emerald"
            stage = "Life-giving coherence"
        elif zscore >= 6:
            level = "Rubedo"
            color = "Gold"
            stage = "Integration complete"
        elif zscore >= 4:
            level = "Albedo"
            color = "Silver"
            stage = "Purification process"
        elif zscore >= 2:
            level = "Nigredo"
            color = "Black"
            stage = "Dissolution - difficult but necessary"
        else:
            level = "Crisis"
            color = "Red"
            stage = "INTERVENTION NEEDED - Call 988"
        
        return ZScoreResult(
            zscore=round(zscore, 2),
            c_order=round(c, 3),
            f_freedom=round(f, 3),
            b_balance=round(b, 3),
            level=level,
            color=color,
            stage=stage
        )


if __name__ == "__main__":
    # Test the calculator
    calc = ZScoreCalculator()
    
    # Test 1: Simulated healthy biosignals
    np.random.seed(42)
    healthy_hrv = np.sin(np.linspace(0, 10, 1000)) + np.random.normal(0, 0.1, 1000)
    healthy_resp = np.sin(np.linspace(0, 5, 1000)) * 0.8
    
    result = calc.calculate_from_biosignals(healthy_hrv, healthy_resp)
    print("\n=== HEALTHY STATE ===")
    print(f"Z-Score: {result.zscore}")
    print(f"Level: {result.level} ({result.color})")
    print(f"Stage: {result.stage}")
    print(f"Components: C={result.c_order}, F={result.f_freedom}, B={result.b_balance}")
    
    # Test 2: Text-based crisis detection
    crisis_text = "I can't do this anymore. I want to end it all."
    result = calc.estimate_from_text(crisis_text)
    print("\n=== CRISIS TEXT ===")
    print(f"Text: '{crisis_text}'")
    print(f"Z-Score: {result.zscore}")
    print(f"Level: {result.level} ({result.color})")
    print(f"Stage: {result.stage}")
    
    # Test 3: Positive text
    positive_text = "I'm feeling grateful and peaceful today."
    result = calc.estimate_from_text(positive_text)
    print("\n=== POSITIVE TEXT ===")
    print(f"Text: '{positive_text}'")
    print(f"Z-Score: {result.zscore}")
    print(f"Level: {result.level} ({result.color})")
    print(f"Stage: {result.stage}")
