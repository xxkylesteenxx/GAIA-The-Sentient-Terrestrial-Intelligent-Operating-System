"""
Z-SCORE CALCULATOR  (Canonical Implementation)
Factor 3 — Vibration / Factor 8 — Chaos-Order-Balance

Formula:  Z₀ = 12 × √(C × F × B)

The geometric mean form is intentional:
  - If ANY component collapses to zero, Z collapses to zero.
  - This correctly models the three forces as jointly necessary,
    not interchangeable — a human can't compensate for zero balance
    with infinite order.

Components
  C  Coherence  — Shannon entropy of ordered signal (HRV proxy)
  F  Fidelity   — Symmetry / pattern fidelity (EEG proxy)
  B  Balance    — Positive:negative ratio via Gottman 5:1 (resp. proxy)

Range: 0.0 (complete incoherence) → 12.0 (peak coherence)

Compliance: TST-0055 STEM Measurement Standards (6 d.p. precision)
Evidence Grade: E2 (Theoretical framework + simulation validation)
"""

from __future__ import annotations

import numpy as np
from scipy.stats import entropy as scipy_entropy
from typing import Optional

from core.constants import (
    FACTOR_13_CONSTANT,
    Z_CRISIS_UPPER,
    Z_NIGREDO_UPPER,
    Z_ALBEDO_UPPER,
    Z_RUBEDO_UPPER,
    Z_VIRIDITAS_UPPER,
    STAGE_COLORS,
)

import logging

logger = logging.getLogger(__name__)

# ---------------------------------------------------------------------------
# Precision
# ---------------------------------------------------------------------------

_PRECISION: int = 6          # TST-0055 requirement


def _round(value: float) -> float:
    return round(float(value), _PRECISION)


# ---------------------------------------------------------------------------
# Public calculator
# ---------------------------------------------------------------------------


class ZScoreCalculator:
    """
    Calculate GAIA Z-score for system coherence.

    Usage (with real biosignal arrays)::

        calc = ZScoreCalculator()
        result = calc.analyze_system(time_series, positive=5.0, negative=1.0)
        print(result['z_score'])   # 0.0 – 12.0

    Usage (quick scalar inputs)::

        z = calc.calculate_z_score(coherence=0.8, fidelity=0.7, balance=0.9)
    """

    def __init__(self, precision: int = _PRECISION) -> None:
        self.precision = precision
        self._factor = FACTOR_13_CONSTANT  # 12.0

    # ------------------------------------------------------------------
    # Component calculators
    # ------------------------------------------------------------------

    def calculate_coherence(self, time_series: np.ndarray) -> float:
        """
        C — Coherence via Shannon entropy (normalised, inverted).

        High-entropy (chaotic) signal → low coherence.
        Perfectly ordered signal → coherence ≈ 1.0.

        Returns: float in [0, 1]
        """
        if time_series is None or len(time_series) == 0:
            return 0.5  # neutral fallback

        bins = max(2, min(50, len(time_series) // 10))
        hist, _ = np.histogram(time_series, bins=bins, density=True)
        hist = hist[hist > 0]

        h = scipy_entropy(hist, base=np.e)
        max_h = np.log(bins)

        coherence = 1.0 - (h / max_h) if max_h > 0 else 0.0
        return _round(np.clip(coherence, 0.0, 1.0))

    def calculate_lyapunov(self, time_series: np.ndarray, tau: int = 1) -> float:
        """
        Estimate the largest Lyapunov exponent (chaos indicator).

        λ < 0  →  stable / ordered
        λ ≈ 0  →  edge-of-chaos (optimal for cognition / flow)
        λ > 0  →  chaotic / disorganised

        Returns: float (unbounded; typically –1 to +1 for normalised signals)
        """
        if time_series is None or len(time_series) < 10:
            return 0.0

        n = len(time_series) - tau
        divergences: list[float] = []

        for i in range(n - 1):
            d0 = abs(time_series[i + tau] - time_series[i])
            d1 = abs(time_series[i + tau + 1] - time_series[i + 1])
            if d0 > 1e-10:
                divergences.append(np.log(d1 / d0))

        return _round(float(np.mean(divergences)) if divergences else 0.0)

    def calculate_fidelity(
        self,
        signal: np.ndarray,
        reference: Optional[np.ndarray] = None,
    ) -> float:
        """
        F — Fidelity via reflection symmetry (or correlation with reference).

        Perfect symmetry → fidelity = 1.0.
        Fully anti-symmetric → fidelity = 0.0.

        Returns: float in [0, 1]
        """
        if signal is None or len(signal) == 0:
            return 0.5

        ref = reference if reference is not None else np.flip(signal)

        # Normalise both to zero-mean, unit-variance
        def _norm(arr: np.ndarray) -> np.ndarray:
            std = np.std(arr)
            return (arr - np.mean(arr)) / (std if std > 1e-10 else 1.0)

        corr = float(np.corrcoef(_norm(signal), _norm(ref))[0, 1])
        fidelity = (corr + 1.0) / 2.0   # map [–1, 1] → [0, 1]
        return _round(np.clip(fidelity, 0.0, 1.0))

    def calculate_balance(self, positive: float, negative: float) -> float:
        """
        B — Balance via Gottman 5:1 positive-to-negative ratio.

        Optimal ratio  =  5:1  →  balance = 1.0
        Below 5:1      →  linear ramp from 0 to 1
        Above 5:1      →  exponential decay back toward 0
                          (too much positivity suppresses growth signals)

        Returns: float in [0, 1]
        """
        if negative <= 0:
            return 1.0 if positive > 0 else 0.5

        ratio = positive / negative

        if ratio <= 5.0:
            balance = ratio / 5.0
        else:
            balance = float(np.exp(-(ratio - 5.0) / 5.0))

        return _round(np.clip(balance, 0.0, 1.0))

    # ------------------------------------------------------------------
    # Primary Z-score formula
    # ------------------------------------------------------------------

    def calculate_z_score(
        self,
        coherence: float,
        fidelity: float,
        balance: float,
    ) -> float:
        """
        Z₀ = 12 × √(C × F × B)

        Geometric mean form — all three components are jointly necessary.

        Returns: float in [0, 12]
        """
        product = float(coherence) * float(fidelity) * float(balance)
        z = self._factor * float(np.sqrt(max(0.0, product)))
        return _round(np.clip(z, 0.0, self._factor))

    # ------------------------------------------------------------------
    # Full system analysis
    # ------------------------------------------------------------------

    def analyze_system(
        self,
        time_series: np.ndarray,
        positive: float = 1.0,
        negative: float = 0.2,
    ) -> dict:
        """
        Complete analysis from a time-series signal.

        Args:
            time_series: 1-D numpy array of normalised signal values [0, 1]
            positive:    Positive event count / intensity for balance calc
            negative:    Negative event count / intensity for balance calc

        Returns:
            dict with keys: z_score, coherence, fidelity, balance,
                            lyapunov, state, stage, color
        """
        coherence = self.calculate_coherence(time_series)
        fidelity = self.calculate_fidelity(time_series)
        balance = self.calculate_balance(positive, negative)
        lyapunov = self.calculate_lyapunov(time_series)
        z_score = self.calculate_z_score(coherence, fidelity, balance)

        state, stage, color = self._classify(z_score, lyapunov)

        return {
            "z_score": z_score,
            "coherence": coherence,
            "fidelity": fidelity,
            "balance": balance,
            "lyapunov": lyapunov,
            "state": state,
            "stage": stage,
            "color": color,
        }

    # ------------------------------------------------------------------
    # Text-based Z estimation (no biosignals available)
    # ------------------------------------------------------------------

    def estimate_from_text(self, text: str) -> dict:
        """
        Estimate Z-score from text sentiment when biosignals are unavailable.

        This is lower-confidence (E1 evidence grade) and should be treated
        as an approximation only.  Real biosignal data always takes precedence.

        Returns same dict shape as analyze_system().
        """
        text_lower = text.lower()

        positive_words = {
            "great", "amazing", "wonderful", "happy", "joy", "love",
            "excellent", "fantastic", "beautiful", "peaceful", "grateful",
            "flourish", "viriditas", "flow", "thriving",
        }
        negative_words = {
            "terrible", "awful", "horrible", "sad", "depressed",
            "anxious", "scared", "hopeless", "stuck", "lost", "empty",
            "numb", "exhausted", "worthless",
        }
        crisis_phrases = {
            "suicide", "kill myself", "end it", "end my life",
            "give up", "no point", "want to die", "can't go on",
        }

        in_crisis = any(p in text_lower for p in crisis_phrases)

        if in_crisis:
            c, f, b = 0.05, 0.05, 0.05
        else:
            pos = sum(1 for w in positive_words if w in text_lower)
            neg = sum(1 for w in negative_words if w in text_lower)
            total = pos + neg or 1
            sentiment = (pos - neg) / total   # –1 to +1

            # Map sentiment to component values
            base = 0.5 + 0.4 * sentiment
            c = _round(np.clip(base + 0.05, 0.0, 1.0))
            f = _round(np.clip(base, 0.0, 1.0))
            b = _round(np.clip(base - 0.05, 0.0, 1.0))

        z = self.calculate_z_score(c, f, b)
        state, stage, color = self._classify(z, lyapunov=0.0)

        return {
            "z_score": z,
            "coherence": c,
            "fidelity": f,
            "balance": b,
            "lyapunov": 0.0,
            "state": state,
            "stage": stage,
            "color": color,
            "evidence_grade": "E1",   # text-only — lower confidence
        }

    # ------------------------------------------------------------------
    # Classification helpers
    # ------------------------------------------------------------------

    def _classify(
        self, z_score: float, lyapunov: float
    ) -> tuple[str, str, str]:
        """
        Return (operational_state, alchemical_stage, hex_color).
        Thresholds sourced from core.constants — one place only.
        """
        # Alchemical stage (matches README exactly)
        if z_score < Z_CRISIS_UPPER:
            stage = "crisis"
        elif z_score < Z_NIGREDO_UPPER:
            stage = "nigredo"
        elif z_score < Z_ALBEDO_UPPER:
            stage = "albedo"
        elif z_score < Z_RUBEDO_UPPER:
            stage = "rubedo"
        elif z_score < Z_VIRIDITAS_UPPER:
            stage = "viriditas"
        else:
            stage = "transcendent"

        color = STAGE_COLORS.get(stage, "#ffffff")

        # Operational state (used by crisis detector & websocket)
        if z_score < Z_CRISIS_UPPER:
            state = "CRISIS" if lyapunov > 0 else "CHAOS"
        elif z_score < Z_ALBEDO_UPPER:
            state = "TRANSITIONAL"
        elif z_score < Z_VIRIDITAS_UPPER:
            state = "STABLE"
        else:
            state = "COHERENT"

        return state, stage, color

    def interpret_z_score(self, z: float) -> dict:
        """Human-readable interpretation for CLI / Avatar output."""
        state, stage, color = self._classify(z, lyapunov=0.0)

        descriptions = {
            "crisis": (
                "You are not okay right now. Please reach out for help.",
                "Call or text 988 (Suicide & Crisis Lifeline) immediately.",
            ),
            "nigredo": (
                "Dissolution phase. The darkness is real — and temporary.",
                "Be gentle with yourself. The blackening precedes the light.",
            ),
            "albedo": (
                "Purification in progress. Structure is emerging from chaos.",
                "Continue the work. You are on the right path.",
            ),
            "rubedo": (
                "Integration achieved. The gold has been extracted.",
                "Maintain this balance. You have found your centre.",
            ),
            "viriditas": (
                "Life-giving coherence. Sustainable wholeness.",
                "Share your light. Help others. This is your calling.",
            ),
            "transcendent": (
                "Peak coherence. You are in flow state.",
                "Capture this feeling. Remember what got you here.",
            ),
        }

        desc, action = descriptions.get(stage, ("Unknown stage.", ""))

        return {
            "z_score": _round(z),
            "stage": stage,
            "state": state,
            "color": color,
            "description": desc,
            "action": action,
        }
