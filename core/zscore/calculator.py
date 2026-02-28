"""Z-Score Calculator for GAIA Coherence Measurement.

Implements Z₀ = 12 × √(C × F × B) with STEM-compliant measurements:
- C (Coherence): Shannon entropy, Lyapunov exponent
- F (Fidelity): Symmetry analysis, pattern recognition
- B (Balance): Equilibrium metrics

Compliance: TST-0055 STEM Measurement Standards
Evidence Grade: E2 (Theoretical + Simulations)
"""

import numpy as np
from scipy.stats import entropy
from scipy.integrate import odeint
from typing import Dict, List, Tuple
import logging

logger = logging.getLogger(__name__)


class ZScoreCalculator:
    """Calculate GAIA Z-score for system coherence."""

    def __init__(self, precision: int = 6):
        """Initialize calculator with SI unit precision.
        
        Args:
            precision: Decimal places for measurements (default 6 per TST-0055)
        """
        self.precision = precision
        self.FACTOR_13 = 12.0  # Universal Love constant
        
    def calculate_coherence(self, time_series: np.ndarray) -> float:
        """Calculate coherence (C) using Shannon entropy.
        
        Args:
            time_series: Normalized time series data [0,1]
            
        Returns:
            Coherence value [0,1] where 1 = maximum coherence
        """
        if len(time_series) == 0:
            return 0.0
            
        # Bin data for entropy calculation
        bins = min(50, len(time_series) // 10)
        hist, _ = np.histogram(time_series, bins=bins, density=True)
        hist = hist[hist > 0]  # Remove zero bins
        
        # Shannon entropy (nats)
        h = entropy(hist, base=np.e)
        
        # Normalize: max entropy = ln(bins)
        max_entropy = np.log(bins)
        coherence = 1.0 - (h / max_entropy) if max_entropy > 0 else 0.0
        
        return round(coherence, self.precision)
    
    def calculate_lyapunov(self, time_series: np.ndarray, tau: int = 1) -> float:
        """Estimate Lyapunov exponent (chaos measure).
        
        Args:
            time_series: Time series data
            tau: Time delay for embedding
            
        Returns:
            Lyapunov exponent (λ < 0: stable, λ ≈ 0: neutral, λ > 0: chaotic)
        """
        if len(time_series) < 10:
            return 0.0
            
        n = len(time_series) - tau
        divergence = []
        
        for i in range(n - 1):
            d0 = abs(time_series[i + tau] - time_series[i])
            d1 = abs(time_series[i + tau + 1] - time_series[i + 1])
            
            if d0 > 1e-10:  # Avoid log(0)
                divergence.append(np.log(d1 / d0))
        
        lyapunov = np.mean(divergence) if divergence else 0.0
        return round(lyapunov, self.precision)
    
    def calculate_fidelity(self, signal: np.ndarray, reference: np.ndarray = None) -> float:
        """Calculate fidelity (F) using symmetry analysis.
        
        Args:
            signal: Input signal
            reference: Reference pattern (if None, uses ideal symmetry)
            
        Returns:
            Fidelity value [0,1] where 1 = perfect symmetry
        """
        if len(signal) == 0:
            return 0.0
            
        if reference is None:
            # Use reflection symmetry as reference
            reference = np.flip(signal)
        
        # Normalize both signals
        signal_norm = (signal - np.mean(signal)) / (np.std(signal) + 1e-10)
        ref_norm = (reference - np.mean(reference)) / (np.std(reference) + 1e-10)
        
        # Calculate correlation (symmetry measure)
        correlation = np.corrcoef(signal_norm, ref_norm)[0, 1]
        fidelity = (correlation + 1) / 2  # Map [-1,1] to [0,1]
        
        return round(fidelity, self.precision)
    
    def calculate_balance(self, positive: float, negative: float) -> float:
        """Calculate balance (B) using ratio.
        
        Based on Gottman's 5:1 ratio for relationship stability.
        GAIA optimal: 5.0 (healthy growth zone)
        
        Args:
            positive: Count/intensity of positive events
            negative: Count/intensity of negative events
            
        Returns:
            Balance value [0,1] where 1 = optimal 5:1 ratio
        """
        if negative == 0:
            return 1.0 if positive > 0 else 0.5
            
        ratio = positive / negative
        
        # Map ratio to [0,1] with peak at 5:1
        if ratio < 5.0:
            balance = ratio / 5.0
        else:
            balance = np.exp(-(ratio - 5.0) / 5.0)
        
        return round(balance, self.precision)
    
    def calculate_z_score(self, coherence: float, fidelity: float, balance: float) -> float:
        """Calculate complete Z-score: Z₀ = 12 × √(C × F × B)
        
        Args:
            coherence: Coherence value [0,1]
            fidelity: Fidelity value [0,1]
            balance: Balance value [0,1]
            
        Returns:
            Z-score [0,12] where 12 = maximum coherence
        """
        product = coherence * fidelity * balance
        z_score = self.FACTOR_13 * np.sqrt(product)
        
        return round(z_score, self.precision)
    
    def analyze_system(self, time_series: np.ndarray, positive: float = 1.0, 
                       negative: float = 0.2) -> Dict[str, float]:
        """Complete system analysis.
        
        Args:
            time_series: System time series data
            positive: Positive event count/intensity
            negative: Negative event count/intensity
            
        Returns:
            Dictionary with all measurements
        """
        coherence = self.calculate_coherence(time_series)
        fidelity = self.calculate_fidelity(time_series)
        balance = self.calculate_balance(positive, negative)
        lyapunov = self.calculate_lyapunov(time_series)
        z_score = self.calculate_z_score(coherence, fidelity, balance)
        
        return {
            'z_score': z_score,
            'coherence': coherence,
            'fidelity': fidelity,
            'balance': balance,
            'lyapunov': lyapunov,
            'state': self._classify_state(z_score, lyapunov)
        }
    
    def _classify_state(self, z_score: float, lyapunov: float) -> str:
        """Classify system state based on Z-score and Lyapunov.
        
        Returns:
            State classification string
        """
        if z_score < 3.0:
            return 'CRISIS' if lyapunov > 0 else 'CHAOS'
        elif z_score < 6.0:
            return 'TRANSITIONAL'
        elif z_score < 9.0:
            return 'STABLE'
        else:
            return 'COHERENT'
