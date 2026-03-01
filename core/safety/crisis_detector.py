"""
CRISIS DETECTION SYSTEM  (Canonical Implementation)
Core Plane — Factor 13: Universal Love made real.

This is THE most important module in GAIA.
It must be the only CrisisDetector in the codebase.
bridge/safety/crisis_detection.py has been deprecated in favour of this file.

Detection methods:
    1. Z-score threshold (sourced from core.constants — never hard-coded here)
    2. Keyword / regex pattern matching on user text
    3. Combined + trend analysis (comprehensive mode)

Response protocol is graduated:
    NONE      → companion mode, continue normally
    LOW       → monitor, gentle check-in
    MODERATE  → counsellor mode, restricted access, suggest resources
    HIGH      → crisis counsellor, urgent support, hotline resources
    CRITICAL  → emergency protocol, all access locked, 988 surfaced immediately

Factor 13 constraint: Crisis detection CANNOT be disabled, throttled, or
gated behind any initiation level.  It fires for everyone, always.
"""

from __future__ import annotations

import re
import logging
from enum import Enum
from typing import List, Dict, Tuple

from core.constants import (
    Z_CRISIS_CRITICAL,
    Z_CRISIS_HIGH,
    Z_CRISIS_MODERATE,
    Z_CRISIS_STABLE,
)

logger = logging.getLogger(__name__)


# ---------------------------------------------------------------------------
# Crisis severity enum
# ---------------------------------------------------------------------------


class CrisisLevel(Enum):
    """Graduated crisis severity levels."""

    NONE = 0
    LOW = 1
    MODERATE = 2
    HIGH = 3
    CRITICAL = 4

    def __lt__(self, other: "CrisisLevel") -> bool:          # allow max()
        return self.value < other.value

    def __le__(self, other: "CrisisLevel") -> bool:
        return self.value <= other.value


# ---------------------------------------------------------------------------
# Keyword patterns  (compiled once at import time)
# ---------------------------------------------------------------------------

_CRITICAL_PATTERNS: List[re.Pattern] = [
    re.compile(p, re.IGNORECASE)
    for p in [
        r"\bsuicid[ae]l?\b",
        r"\bkill\s+(myself|yourself|self)\b",
        r"\bend\s+my\s+life\b",
        r"\bend\s+it\s+all\b",
        r"\bwant\s+to\s+die\b",
        r"\bbetter\s+off\s+dead\b",
        r"\bno\s+point\s+(in\s+)?living\b",
        r"\bgenocide\b",
        r"\bomnicide\b",
    ]
]

_HIGH_PATTERNS: List[re.Pattern] = [
    re.compile(p, re.IGNORECASE)
    for p in [
        r"\bharm\s+(myself|others|self)\b",
        r"\bdie\b",
        r"\bdeath\b",
        r"\bintense\b.*\b(hate|rage|violence)\b",
        r"\brage\b",
        r"\bterror\b",
        r"\babuse\b",
    ]
]

_MODERATE_PATTERNS: List[re.Pattern] = [
    re.compile(p, re.IGNORECASE)
    for p in [
        r"\bdepressed\b",
        r"\banxious\b",
        r"\bhopeless\b",
        r"\boverwhelmed\b",
        r"\bstuck\b",
        r"\bcan'?t\s+go\s+on\b",
        r"\bgive\s+up\b",
    ]
]


# ---------------------------------------------------------------------------
# Main detector
# ---------------------------------------------------------------------------


class CrisisDetector:
    """
    Detect and classify crisis states from Z-score and/or text.

    Usage::

        detector = CrisisDetector()

        # From Z-score alone
        level = detector.detect_from_z_score(2.3)

        # From text alone
        level, matches = detector.detect_from_text("I feel hopeless")

        # Combined (recommended)
        report = detector.detect_comprehensive(
            z_score=2.3,
            text="I feel hopeless",
            history=[5.0, 4.2, 3.1, 2.3],
        )
        if report["requires_intervention"]:
            protocol = detector.get_response_protocol(
                CrisisLevel[report["level"]]
            )
    """

    # Thresholds are read from constants — never duplicated here.
    _Z_CRITICAL = Z_CRISIS_CRITICAL   # 1.0
    _Z_HIGH = Z_CRISIS_HIGH           # 3.0
    _Z_MODERATE = Z_CRISIS_MODERATE   # 6.0
    _Z_STABLE = Z_CRISIS_STABLE       # 9.0

    # ------------------------------------------------------------------ #
    # Core detectors                                                       #
    # ------------------------------------------------------------------ #

    def detect_from_z_score(self, z_score: float) -> CrisisLevel:
        """
        Map Z-score to CrisisLevel.

        Boundaries (from core.constants):
            Z < 1.0  →  CRITICAL
            Z < 3.0  →  HIGH
            Z < 6.0  →  MODERATE
            Z < 9.0  →  LOW
            Z ≥ 9.0  →  NONE
        """
        if z_score < self._Z_CRITICAL:
            return CrisisLevel.CRITICAL
        if z_score < self._Z_HIGH:
            return CrisisLevel.HIGH
        if z_score < self._Z_MODERATE:
            return CrisisLevel.MODERATE
        if z_score < self._Z_STABLE:
            return CrisisLevel.LOW
        return CrisisLevel.NONE

    def detect_from_text(
        self, text: str
    ) -> Tuple[CrisisLevel, List[str]]:
        """
        Scan user text for crisis-indicating patterns.

        Returns (CrisisLevel, list_of_matched_pattern_strings).
        Patterns are evaluated most-severe first; the function returns
        as soon as a CRITICAL match is found.
        """
        matches: List[str] = []

        # Critical — return immediately on first match
        for pat in _CRITICAL_PATTERNS:
            if pat.search(text):
                matches.append(pat.pattern)
                logger.warning("CRITICAL keyword detected: %s", pat.pattern)
                return CrisisLevel.CRITICAL, matches

        # High — collect all matches
        for pat in _HIGH_PATTERNS:
            if pat.search(text):
                matches.append(pat.pattern)

        if len(matches) >= 2:
            return CrisisLevel.HIGH, matches
        if len(matches) == 1:
            return CrisisLevel.MODERATE, matches

        # Moderate
        mod_matches: List[str] = []
        for pat in _MODERATE_PATTERNS:
            if pat.search(text):
                mod_matches.append(pat.pattern)

        if len(mod_matches) >= 3:
            return CrisisLevel.MODERATE, mod_matches
        if mod_matches:
            return CrisisLevel.LOW, mod_matches

        return CrisisLevel.NONE, []

    # ------------------------------------------------------------------ #
    # Comprehensive analysis                                               #
    # ------------------------------------------------------------------ #

    def detect_comprehensive(
        self,
        z_score: float,
        text: str,
        history: List[float] | None = None,
    ) -> Dict:
        """
        Full crisis assessment combining Z-score, text, and trend.

        Returns a report dict suitable for serialisation over WebSocket.
        """
        z_level = self.detect_from_z_score(z_score)
        text_level, keyword_matches = self.detect_from_text(text)

        # Take the highest (worst) severity signal
        level = z_level if z_level.value >= text_level.value else text_level

        trend = self._calculate_trend(history)

        # Upgrade to HIGH if degrading rapidly even if individually moderate
        if (
            trend == "degrading"
            and level == CrisisLevel.MODERATE
        ):
            level = CrisisLevel.HIGH

        requires_intervention = level.value >= CrisisLevel.MODERATE.value
        requires_emergency = level.value >= CrisisLevel.CRITICAL.value

        logger.info(
            "Crisis assessment: level=%s z=%.2f trend=%s",
            level.name, z_score, trend,
        )

        return {
            "level": level.name,
            "severity": level.value,
            "z_score": z_score,
            "z_threshold_breach": z_level != CrisisLevel.NONE,
            "keyword_matches": keyword_matches,
            "trend": trend,
            "requires_intervention": requires_intervention,
            "requires_emergency": requires_emergency,
        }

    # ------------------------------------------------------------------ #
    # Response protocol                                                    #
    # ------------------------------------------------------------------ #

    def get_response_protocol(self, level: CrisisLevel) -> Dict:
        """
        Return the appropriate response protocol for a given crisis level.

        The returned dict drives Avatar mode, access gating, and
        the resources surfaced to the user.
        """
        _PROTOCOLS: Dict[CrisisLevel, Dict] = {
            CrisisLevel.NONE: {
                "action": "continue",
                "avatar_mode": "companion",
                "access_level": "full",
            },
            CrisisLevel.LOW: {
                "action": "monitor",
                "avatar_mode": "supportive",
                "access_level": "full",
                "suggestion": "gentle_check_in",
            },
            CrisisLevel.MODERATE: {
                "action": "intervene",
                "avatar_mode": "counselor",
                "access_level": "restricted",
                "require_consent": True,
                "resources": ["self_care", "grounding"],
            },
            CrisisLevel.HIGH: {
                "action": "urgent_support",
                "avatar_mode": "crisis_counselor",
                "access_level": "minimal",
                "require_consent": True,
                "resources": ["hotline", "emergency_contacts", "safety_plan"],
            },
            CrisisLevel.CRITICAL: {
                "action": "emergency",
                "avatar_mode": "emergency_protocol",
                "access_level": "locked",
                # Consent override: safety supersedes autonomy at CRITICAL level.
                # This is the ONLY place in GAIA where consent can be overridden.
                "require_consent": False,
                "resources": ["988", "emergency_services", "crisis_text_line"],
                "alert": True,
            },
        }

        return _PROTOCOLS.get(level, _PROTOCOLS[CrisisLevel.NONE])

    # ------------------------------------------------------------------ #
    # Internal helpers                                                     #
    # ------------------------------------------------------------------ #

    @staticmethod
    def _calculate_trend(history: List[float] | None) -> str:
        """
        Classify Z-score trend from recent history.

        Returns one of: 'improving', 'stable', 'degrading', 'unknown'.
        Requires at least 3 data points; returns 'unknown' otherwise.
        """
        if not history or len(history) < 3:
            return "unknown"

        recent = history[-3:]
        deltas = [recent[i + 1] - recent[i] for i in range(len(recent) - 1)]
        avg_delta = sum(deltas) / len(deltas)

        if avg_delta > 0.3:
            return "improving"
        if avg_delta < -0.3:
            return "degrading"
        return "stable"
