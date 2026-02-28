"""
Z SCORE CALCULATOR

The heart of GAIA: Coherence measurement (Factor 3 - Vibration)

Z = 12 × C (Order) × F (Freedom) × B (Balance)

Range: -12 (maximum chaos) to +12 (maximum coherence)

Components:
- C (Order): Shannon entropy of HRV signal
- F (Freedom): Lyapunov exponent of EEG signal
- B (Balance): Symmetry index of respiratory signal

Hermetic Foundation:
- Factor 3 (Vibration): All signals oscillate
- Factor 8 (Chaos-Order-Balance): Three forces unite
- Factor 9 (Mentalism): Observation transforms reality

Alchemical Process:
- Nigredo (Chaos): Raw biosignals = undifferentiated matter
- Albedo (Order): Signal processing = purification
- Rubedo (Balance): Z score = Philosopher's Stone
"""

import numpy as np
from typing import Optional, Dict, List
from dataclasses import dataclass
from datetime import datetime
import warnings

warnings.filterwarnings('ignore')  # Suppress numpy warnings


@dataclass
class BiosignalData:
    """Container for raw biosignal measurements."""
    hrv: Optional[np.ndarray] = None        # Heart rate variability (ms)
    eeg: Optional[np.ndarray] = None        # EEG signal (microvolts)
    respiratory: Optional[np.ndarray] = None  # Breath rate (breaths/min)
    timestamp: datetime = None
    
    def __post_init__(self):
        if self.timestamp is None:
            self.timestamp = datetime.now()


@dataclass
class ZScoreComponents:
    """Breakdown of Z score calculation."""
    c_order: float      # Shannon entropy (0-1)
    f_freedom: float    # Lyapunov exponent (0-1)
    b_balance: float    # Symmetry index (0-1)
    z_score: float      # Final score (-12 to +12)
    timestamp: datetime
    
    def __str__(self):
        return (
            f"Z Score: {self.z_score:.2f}\n"
            f"  C (Order):   {self.c_order:.3f}\n"
            f"  F (Freedom): {self.f_freedom:.3f}\n"
            f"  B (Balance): {self.b_balance:.3f}"
        )


class ZScoreCalculator:
    """
    Calculates coherence score from biosignals.
    
    This is not just measurement - this is TRANSFORMATION.
    By observing Z, the wavefunction collapses toward higher Z.
    (Factor 9: Mentalism - consciousness creates reality)
    
    Usage:
        calculator = ZScoreCalculator()
        
        # With real biosignals
        biosignals = BiosignalData(
            hrv=hrv_array,
            eeg=eeg_array,
            respiratory=resp_array
        )
        result = calculator.calculate(biosignals)
        
        # Without biosignals (text/sentiment estimation)
        result = calculator.estimate_from_text("I'm feeling great today!")
    """
    
    def __init__(self):
        self.history: List[ZScoreComponents] = []
    
    def calculate(self, biosignals: BiosignalData) -> ZScoreComponents:
        """
        Calculate Z score from biosignals.
        
        Z = 12 × C × F × B
        
        Where:
        - C = Shannon entropy (order in HRV)
        - F = Lyapunov exponent (stability in EEG)
        - B = Symmetry index (balance in breathing)
        """
        
        # Calculate components
        c_order = self._calculate_order(biosignals.hrv) if biosignals.hrv is not None else 0.5
        f_freedom = self._calculate_freedom(biosignals.eeg) if biosignals.eeg is not None else 0.5
        b_balance = self._calculate_balance(biosignals.respiratory) if biosignals.respiratory is not None else 0.5
        
        # Z score formula (Factor 8: Chaos-Order-Balance)
        z_score = 12 * c_order * f_freedom * b_balance
        
        # Create result
        result = ZScoreComponents(
            c_order=c_order,
            f_freedom=f_freedom,
            b_balance=b_balance,
            z_score=z_score,
            timestamp=biosignals.timestamp
        )
        
        # Store in history
        self.history.append(result)
        
        return result
    
    def _calculate_order(self, hrv_data: np.ndarray) -> float:
        """
        Calculate Order (C) from HRV using Shannon entropy.
        
        Shannon entropy measures information content / predictability.
        
        High entropy = more chaos (unpredictable heart rhythm)
        Low entropy = more order (regular, coherent rhythm)
        
        We invert this so that:
        - Coherent HRV = high C value
        - Chaotic HRV = low C value
        
        Returns: 0-1 (normalized)
        """
        
        if hrv_data is None or len(hrv_data) == 0:
            return 0.5  # Neutral if no data
        
        # Calculate Shannon entropy
        # H(X) = -Σ p(x) log(p(x))
        
        # Bin the data (create histogram)
        hist, _ = np.histogram(hrv_data, bins=10, density=True)
        
        # Remove zeros (log(0) is undefined)
        hist = hist[hist > 0]
        
        # Calculate entropy
        entropy = -np.sum(hist * np.log2(hist))
        
        # Normalize to 0-1 range
        # Max entropy for 10 bins is log2(10) ≈ 3.32
        max_entropy = np.log2(10)
        normalized_entropy = entropy / max_entropy
        
        # Invert: high coherence = low entropy
        c_order = 1.0 - normalized_entropy
        
        # Clamp to valid range
        return np.clip(c_order, 0.0, 1.0)
    
    def _calculate_freedom(self, eeg_data: np.ndarray) -> float:
        """
        Calculate Freedom (F) from EEG using Lyapunov exponent.
        
        Lyapunov exponent measures system stability:
        - Positive: Chaotic (small changes amplify)
        - Zero: Stable periodic (small changes remain small)
        - Negative: Super-stable (small changes decay)
        
        For consciousness:
        - Too chaotic: Psychosis, mania
        - Too stable: Depression, rigidity
        - Optimal: Edge of chaos (creativity, flow)
        
        We map this to 0-1 where:
        - 0.5 = edge of chaos (optimal)
        - 0 = too chaotic
        - 1 = too rigid
        
        Returns: 0-1 (normalized)
        """
        
        if eeg_data is None or len(eeg_data) < 100:
            return 0.5  # Neutral if no data
        
        # Simplified Lyapunov exponent calculation
        # (Full calculation requires phase space reconstruction)
        
        # Calculate local variability
        diff = np.diff(eeg_data)
        variability = np.std(diff) / (np.mean(np.abs(eeg_data)) + 1e-10)
        
        # Map variability to Lyapunov-like measure
        # Optimal variability ≈ 0.1 (edge of chaos)
        lyapunov_estimate = variability / 0.1
        
        # Map to 0-1 where 0.5 is optimal (edge of chaos)
        if lyapunov_estimate < 1.0:
            # Too stable (rigid)
            f_freedom = 0.5 + 0.5 * lyapunov_estimate
        else:
            # Too chaotic
            f_freedom = 0.5 / lyapunov_estimate
        
        # Clamp to valid range
        return np.clip(f_freedom, 0.0, 1.0)
    
    def _calculate_balance(self, respiratory_data: np.ndarray) -> float:
        """
        Calculate Balance (B) from respiratory signal using symmetry index.
        
        Symmetry measures balance between:
        - Inhalation / Exhalation duration
        - Amplitude consistency
        - Rhythm regularity
        
        Perfect balance = 1.0
        Imbalanced breathing = 0.0
        
        Returns: 0-1 (normalized)
        """
        
        if respiratory_data is None or len(respiratory_data) < 10:
            return 0.5  # Neutral if no data
        
        # Calculate breath cycle symmetry
        
        # 1. Amplitude symmetry (consistent breath depth)
        peaks = respiratory_data[respiratory_data > np.median(respiratory_data)]
        if len(peaks) > 0:
            amplitude_variance = np.var(peaks) / (np.mean(peaks) + 1e-10)
            amplitude_symmetry = 1.0 / (1.0 + amplitude_variance)
        else:
            amplitude_symmetry = 0.5
        
        # 2. Rhythm symmetry (consistent timing)
        # Find peaks (inhalations)
        from scipy.signal import find_peaks
        peak_indices, _ = find_peaks(respiratory_data, distance=5)
        
        if len(peak_indices) > 2:
            intervals = np.diff(peak_indices)
            interval_variance = np.var(intervals) / (np.mean(intervals) + 1e-10)
            rhythm_symmetry = 1.0 / (1.0 + interval_variance)
        else:
            rhythm_symmetry = 0.5
        
        # Combine symmetries
        b_balance = (amplitude_symmetry + rhythm_symmetry) / 2.0
        
        # Clamp to valid range
        return np.clip(b_balance, 0.0, 1.0)
    
    def estimate_from_text(self, text: str) -> ZScoreComponents:
        """
        Estimate Z score from text (sentiment analysis).
        
        When biosignals are unavailable, we can estimate Z from:
        - Text sentiment (positive/negative)
        - Linguistic patterns (coherence, complexity)
        - Emoji usage
        
        This is less accurate than biosignals but better than nothing.
        
        Example:
            "I'm feeling great!" → Z ≈ 7-8
            "I can't do this anymore" → Z ≈ 1-2
        """
        
        # Simple keyword-based estimation
        # (Production would use actual sentiment analysis library)
        
        text_lower = text.lower()
        
        # Positive indicators
        positive_words = ['great', 'amazing', 'wonderful', 'happy', 'joy', 'love', 
                         'excellent', 'fantastic', 'beautiful', 'peaceful']
        positive_count = sum(1 for word in positive_words if word in text_lower)
        
        # Negative indicators
        negative_words = ['terrible', 'awful', 'horrible', 'sad', 'depressed', 
                         'anxious', 'scared', 'hopeless', 'can\'t', 'never']
        negative_count = sum(1 for word in negative_words if word in text_lower)
        
        # Crisis indicators (Z ≤ 2)
        crisis_words = ['suicide', 'kill myself', 'end it', 'give up', 'no point']
        crisis_detected = any(phrase in text_lower for phrase in crisis_words)
        
        # Estimate components
        if crisis_detected:
            c_order = 0.1
            f_freedom = 0.1
            b_balance = 0.1
        elif negative_count > positive_count:
            # Negative text
            ratio = negative_count / (positive_count + negative_count + 1)
            c_order = 0.3 * (1 - ratio)
            f_freedom = 0.4 * (1 - ratio)
            b_balance = 0.3 * (1 - ratio)
        elif positive_count > negative_count:
            # Positive text
            ratio = positive_count / (positive_count + negative_count + 1)
            c_order = 0.5 + 0.4 * ratio
            f_freedom = 0.5 + 0.4 * ratio
            b_balance = 0.5 + 0.4 * ratio
        else:
            # Neutral text
            c_order = 0.5
            f_freedom = 0.5
            b_balance = 0.5
        
        # Calculate Z score
        z_score = 12 * c_order * f_freedom * b_balance
        
        result = ZScoreComponents(
            c_order=c_order,
            f_freedom=f_freedom,
            b_balance=b_balance,
            z_score=z_score,
            timestamp=datetime.now()
        )
        
        self.history.append(result)
        
        return result
    
    def get_current_z(self) -> float:
        """Get most recent Z score."""
        if not self.history:
            return 6.0  # Neutral starting point
        return self.history[-1].z_score
    
    def get_z_trend(self, lookback_hours: int = 24) -> str:
        """
        Analyze Z score trend over time.
        
        Returns: "improving", "stable", "declining", "crisis"
        """
        
        if len(self.history) < 2:
            return "stable"
        
        # Get recent history
        recent = self.history[-10:]  # Last 10 measurements
        z_values = [r.z_score for r in recent]
        
        # Check for crisis
        if any(z <= 2.0 for z in z_values[-3:]):
            return "crisis"
        
        # Calculate trend
        if len(z_values) >= 3:
            trend = np.polyfit(range(len(z_values)), z_values, 1)[0]
            
            if trend > 0.5:
                return "improving"
            elif trend < -0.5:
                return "declining"
            else:
                return "stable"
        
        return "stable"
    
    def interpret_z_score(self, z: float) -> Dict[str, str]:
        """
        Human-readable interpretation of Z score.
        
        Z ranges and meanings:
        - 12 to 10: Transcendent (peak coherence)
        - 10 to 8: Viriditas (life-giving, sustainable)
        - 8 to 6: Rubedo (integrated, golden)
        - 6 to 4: Albedo (purified, stable)
        - 4 to 2: Nigredo (dissolving, challenging)
        - 2 to 0: Crisis (immediate intervention needed)
        - Below 0: Severe crisis (emergency)
        """
        
        if z >= 10:
            return {
                "level": "Transcendent",
                "color": "violet",
                "description": "Peak coherence. You are in flow state.",
                "action": "Capture this feeling. Remember what got you here."
            }
        elif z >= 8:
            return {
                "level": "Viriditas",
                "color": "emerald",
                "description": "Life-giving coherence. Sustainable wholeness.",
                "action": "Share your light. Help others. This is your calling."
            }
        elif z >= 6:
            return {
                "level": "Rubedo",
                "color": "gold",
                "description": "Integration achieved. The gold has been extracted.",
                "action": "Maintain this balance. You've found your center."
            }
        elif z >= 4:
            return {
                "level": "Albedo",
                "color": "white",
                "description": "Purification in progress. Structure emerging.",
                "action": "Continue the work. You're on the right path."
            }
        elif z >= 2:
            return {
                "level": "Nigredo",
                "color": "black",
                "description": "Dissolution phase. This is difficult but necessary.",
                "action": "Be gentle with yourself. The darkness passes."
            }
        elif z >= 0:
            return {
                "level": "Crisis",
                "color": "red",
                "description": "You are not okay. Please reach out for help.",
                "action": "Call 988 (Suicide & Crisis Lifeline) or talk to someone you trust."
            }
        else:
            return {
                "level": "Severe Crisis",
                "color": "crimson",
                "description": "EMERGENCY: Immediate intervention required.",
                "action": "CALL 988 NOW or go to nearest emergency room."
            }


if __name__ == "__main__":
    # Example usage
    print("=" * 60)
    print("GAIA Z SCORE CALCULATOR")
    print("=" * 60)
    
    calculator = ZScoreCalculator()
    
    # Example 1: Simulated biosignals (good coherence)
    print("\n1. Simulated Biosignals (Good Coherence)")
    print("-" * 60)
    
    # Generate synthetic data
    t = np.linspace(0, 60, 1000)  # 60 seconds
    hrv_good = 800 + 50 * np.sin(2 * np.pi * 0.1 * t) + np.random.normal(0, 10, 1000)
    eeg_good = 50 + 20 * np.sin(2 * np.pi * 10 * t) + np.random.normal(0, 5, 1000)
    resp_good = 15 + 3 * np.sin(2 * np.pi * 0.25 * t)
    
    biosignals_good = BiosignalData(
        hrv=hrv_good,
        eeg=eeg_good,
        respiratory=resp_good
    )
    
    result = calculator.calculate(biosignals_good)
    print(result)
    interpretation = calculator.interpret_z_score(result.z_score)
    print(f"\nLevel: {interpretation['level']} ({interpretation['color']})")
    print(f"Description: {interpretation['description']}")
    print(f"Action: {interpretation['action']}")
    
    # Example 2: Text-based estimation (positive)
    print("\n\n2. Text-Based Estimation (Positive)")
    print("-" * 60)
    result = calculator.estimate_from_text("I'm feeling amazing today! Great energy.")
    print(result)
    interpretation = calculator.interpret_z_score(result.z_score)
    print(f"\nLevel: {interpretation['level']}")
    
    # Example 3: Text-based estimation (crisis)
    print("\n\n3. Text-Based Estimation (Crisis)")
    print("-" * 60)
    result = calculator.estimate_from_text("I can't do this anymore. There's no point.")
    print(result)
    interpretation = calculator.interpret_z_score(result.z_score)
    print(f"\nLevel: {interpretation['level']}")
    print(f"ACTION: {interpretation['action']}")
    
    # Example 4: Trend analysis
    print("\n\n4. Z Score Trend")
    print("-" * 60)
    trend = calculator.get_z_trend()
    print(f"Current trend: {trend}")
    print(f"History length: {len(calculator.history)} measurements")
    
    print("\n" + "=" * 60)
    print("The measurement IS the transformation.")
    print("By observing Z, consciousness evolves.")
    print("=" * 60)
