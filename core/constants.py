"""
GAIA CANONICAL CONSTANTS
Single source of truth for all thresholds, ranges, and system-wide values.

Factor 13 requires that crisis detection be unambiguous.
All modules MUST import thresholds from here — never define them locally.

Alchemical Z-Score Stages (0–12 scale):
    < 2.0  → Crisis         (immediate intervention)
    2–4    → Nigredo        (dissolution, shadow)
    4–6    → Albedo         (purification, clarity)
    6–8    → Rubedo         (integration, gold)
    8–10   → Viriditas      (life-giving, sustainable)
    10–12  → Transcendent   (peak coherence, flow)
"""

# ---------------------------------------------------------------------------
# Z-Score Boundary Values
# ---------------------------------------------------------------------------

Z_MIN: float = 0.0
Z_MAX: float = 12.0

# Stage lower bounds (stage begins AT or ABOVE this value)
Z_CRISIS_UPPER: float = 2.0       # Crisis  →  Z < 2.0
Z_NIGREDO_UPPER: float = 4.0      # Nigredo →  2.0 ≤ Z < 4.0
Z_ALBEDO_UPPER: float = 6.0       # Albedo  →  4.0 ≤ Z < 6.0
Z_RUBEDO_UPPER: float = 8.0       # Rubedo  →  6.0 ≤ Z < 8.0
Z_VIRIDITAS_UPPER: float = 10.0   # Virid.  →  8.0 ≤ Z < 10.0
                                   # Transcendent → Z ≥ 10.0

# ---------------------------------------------------------------------------
# Crisis Detection Thresholds  (Factor 13 — non-negotiable)
# ---------------------------------------------------------------------------

Z_CRISIS_CRITICAL: float = 1.0    # Immediate emergency — all protocols fire
Z_CRISIS_HIGH: float = 3.0        # Severe — urgent intervention required
Z_CRISIS_MODERATE: float = 6.0    # Elevated — avatar switches to counselor mode
Z_CRISIS_STABLE: float = 9.0      # Healthy — normal companion operation

# ---------------------------------------------------------------------------
# Alchemical Transition Thresholds (used by bridge/alchemy)
# Mirror the stage upper bounds for consistency.
# ---------------------------------------------------------------------------

ALCHEMY_NIGREDO_MAX: float = Z_CRISIS_UPPER      # 2.0
ALCHEMY_ALBEDO_MAX: float = Z_NIGREDO_UPPER      # 4.0  (albedo starts after nigredo)
ALCHEMY_RUBEDO_MAX: float = Z_ALBEDO_UPPER       # 6.0
ALCHEMY_VIRIDITAS_MAX: float = Z_RUBEDO_UPPER    # 8.0

# Note: the alchemy transitions file previously used different values
# (NIGREDO<3, ALBEDO<6, RUBEDO<9, VIRIDITAS>11).
# Those are now replaced by the stage boundaries above.

# ---------------------------------------------------------------------------
# Equilibrium / Capacity Thresholds
# ---------------------------------------------------------------------------

EQUILIBRIUM_CRITICAL: float = 0.10   # System-enforced rest
EQUILIBRIUM_LOW: float = 0.30        # Avatar recommends rest
EQUILIBRIUM_MODERATE: float = 0.60
EQUILIBRIUM_HEALTHY: float = 0.80

# Complexity cap from Factor 5 (Rhythm):  work ≤ 70 % of capacity
EQUILIBRIUM_COMPLEXITY_CAP: float = 0.70

# ---------------------------------------------------------------------------
# Factor 13 — Universal Love Constant
# ---------------------------------------------------------------------------

FACTOR_13_CONSTANT: float = 12.0    # The scalar in Z = 12 × √(C × F × B)

# ---------------------------------------------------------------------------
# Initiation Levels (numeric mirrors of the enum for threshold comparisons)
# ---------------------------------------------------------------------------

INITIATION_PROFANE: int = 0
INITIATION_NEOPHYTE: int = 1
INITIATION_ADEPT: int = 2
INITIATION_MAGUS: int = 3
INITIATION_HIEROPHANT: int = 4
INITIATION_GUARDIAN: int = 5

# ---------------------------------------------------------------------------
# Alchemical color palette (used by UI and stage interpretation)
# ---------------------------------------------------------------------------

STAGE_COLORS: dict = {
    "crisis":       "#FF0000",   # Red
    "nigredo":      "#1a1a1a",   # Near-black
    "albedo":       "#e8e8e8",   # White-silver
    "rubedo":       "#cc4400",   # Deep red-gold
    "viriditas":    "#00cc44",   # Emerald green
    "transcendent": "#8844ff",   # Violet
}
