"""Tests for Z-Score Calculator."""

import pytest
import numpy as np
from core.zscore.calculator import ZScoreCalculator


class TestZScoreCalculator:
    """Test Z-score calculation functions."""
    
    @pytest.fixture
    def calculator(self):
        return ZScoreCalculator()
    
    def test_coherence_perfect(self, calculator):
        """Test coherence with perfectly ordered data."""
        signal = np.ones(100)  # Perfect order = low entropy
        coherence = calculator.calculate_coherence(signal)
        assert coherence > 0.9, "Perfect order should have high coherence"
    
    def test_coherence_random(self, calculator):
        """Test coherence with random noise."""
        signal = np.random.random(100)  # High entropy
        coherence = calculator.calculate_coherence(signal)
        assert coherence < 0.5, "Random noise should have low coherence"
    
    def test_lyapunov_stable(self, calculator):
        """Test Lyapunov exponent for stable system."""
        signal = np.linspace(0, 1, 100)  # Stable linear
        lyapunov = calculator.calculate_lyapunov(signal)
        assert lyapunov <= 0, "Stable system should have λ ≤ 0"
    
    def test_lyapunov_chaotic(self, calculator):
        """Test Lyapunov for chaotic system."""
        # Logistic map (chaotic)
        signal = [0.5]
        r = 3.9
        for _ in range(99):
            signal.append(r * signal[-1] * (1 - signal[-1]))
        lyapunov = calculator.calculate_lyapunov(np.array(signal))
        assert lyapunov > 0, "Chaotic system should have λ > 0"
    
    def test_fidelity_symmetric(self, calculator):
        """Test fidelity with symmetric signal."""
        signal = np.array([1, 2, 3, 4, 3, 2, 1])  # Perfect symmetry
        fidelity = calculator.calculate_fidelity(signal)
        assert fidelity > 0.9, "Symmetric signal should have high fidelity"
    
    def test_balance_optimal(self, calculator):
        """Test balance at optimal 5:1 ratio (Gottman)."""
        balance = calculator.calculate_balance(5.0, 1.0)
        assert balance == 1.0, "5:1 ratio should yield perfect balance"
    
    def test_balance_suboptimal(self, calculator):
        """Test balance below optimal ratio."""
        balance = calculator.calculate_balance(2.0, 1.0)
        assert 0.3 < balance < 0.5, "2:1 ratio should yield moderate balance"
    
    def test_z_score_maximum(self, calculator):
        """Test maximum Z-score (Factor 13)."""
        z_score = calculator.calculate_z_score(1.0, 1.0, 1.0)
        assert z_score == 12.0, "Perfect C×F×B should yield Z=12"
    
    def test_z_score_minimum(self, calculator):
        """Test minimum Z-score."""
        z_score = calculator.calculate_z_score(0.0, 0.0, 0.0)
        assert z_score == 0.0, "Zero metrics should yield Z=0"
    
    def test_z_score_crisis_threshold(self, calculator):
        """Test crisis threshold (Z < 3.0)."""
        # Should trigger crisis: Z = 12 * sqrt(0.0625) = 3.0
        z_score = calculator.calculate_z_score(0.25, 0.25, 0.25)
        assert z_score == 3.0, "Should be at crisis boundary"
    
    def test_analyze_system_complete(self, calculator):
        """Test complete system analysis."""
        signal = np.sin(np.linspace(0, 4*np.pi, 100))  # Coherent wave
        result = calculator.analyze_system(signal, positive=5.0, negative=1.0)
        
        assert 'z_score' in result
        assert 'coherence' in result
        assert 'fidelity' in result
        assert 'balance' in result
        assert 'lyapunov' in result
        assert 'state' in result
        
        assert result['balance'] == 1.0, "5:1 ratio should be optimal"
        assert result['state'] in ['STABLE', 'COHERENT'], "Sine wave should be stable/coherent"
    
    def test_precision_compliance(self, calculator):
        """Test TST-0055 precision compliance (6 decimal places)."""
        signal = np.random.random(100)
        coherence = calculator.calculate_coherence(signal)
        
        # Check decimal places
        decimal_places = len(str(coherence).split('.')[-1])
        assert decimal_places <= 6, f"Precision must be ≤6 decimals (TST-0055), got {decimal_places}"
