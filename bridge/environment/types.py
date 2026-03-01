"""
Living Environment Engine - Type Definitions
Enums for time phases, seasons, weather, and alchemical stages.

Evidence Grade: E5 (observable physical phenomena)
"""

from enum import Enum


class TimePhase(Enum):
    """Six phases of day derived from solar altitude."""
    DAWN = "dawn"
    MORNING = "morning"
    AFTERNOON = "afternoon"
    DUSK = "dusk"
    NIGHT = "night"
    DEEP_NIGHT = "deep_night"


class Season(Enum):
    """Four seasons + tropical wet/dry."""
    SPRING = "spring"
    SUMMER = "summer"
    AUTUMN = "autumn"
    WINTER = "winter"
    WET = "wet"
    DRY = "dry"


class WeatherCondition(Enum):
    """Weather states (OpenWeatherMap + overrides)."""
    CLEAR = "clear"
    RAIN = "rain"
    STORM = "storm"
    SNOW = "snow"
    FOG = "fog"
    AURORA = "aurora"  # Transcendent override (Z≥10)


class AlchemicalStage(Enum):
    """Z-score to alchemical transformation stages."""
    NIGREDO = "nigredo"      # Z: 0-4 (Blackening)
    ALBEDO = "albedo"        # Z: 4-6 (Whitening)
    RUBEDO = "rubedo"        # Z: 6-8 (Reddening)
    VIRIDITAS = "viriditas"  # Z: 8-12 (Greening)


class SoundscapeID(Enum):
    """Ambient audio tracks."""
    FOREST = "forest"
    OCEAN = "ocean"
    RAIN = "rain"
    THUNDER = "thunder"
    WIND = "wind"


class ParticleEffect(Enum):
    """Visual particle systems."""
    RAIN_DROPS = "rain_drops"
    SNOW_FLAKES = "snow_flakes"
    FIREFLIES = "fireflies"
    LEAVES = "leaves"
    AURORA_SHIMMER = "aurora_shimmer"
