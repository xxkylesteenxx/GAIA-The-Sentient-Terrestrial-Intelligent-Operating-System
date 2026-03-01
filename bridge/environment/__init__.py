"""
Living Environment Engine - Adaptive Digital Homes
Evidence Grade: E5 (physical phenomena), E3 (system integration)
"""

from bridge.environment.engine import LivingEnvironmentEngine
from bridge.environment.state import EnvironmentState, RGBGradient
from bridge.environment.types import (
    TimePhase,
    Season,
    WeatherCondition,
    AlchemicalStage,
    SoundscapeID,
    ParticleEffect,
)
from bridge.environment.astronomy import AstronomyCalculator
from bridge.environment.weather import OpenWeatherMapClient, WeatherData

__all__ = [
    "LivingEnvironmentEngine",
    "EnvironmentState",
    "RGBGradient",
    "TimePhase",
    "Season",
    "WeatherCondition",
    "AlchemicalStage",
    "SoundscapeID",
    "ParticleEffect",
    "AstronomyCalculator",
    "OpenWeatherMapClient",
    "WeatherData",
]
