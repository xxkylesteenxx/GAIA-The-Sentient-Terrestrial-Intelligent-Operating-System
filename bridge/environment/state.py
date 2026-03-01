"""
Living Environment Engine - State Container
EnvironmentState dataclass with rendering parameter derivation.

Evidence Grade: E3 (derived from E5 inputs)
"""

from dataclasses import dataclass, field
from datetime import datetime
from typing import Optional, List

from bridge.environment.types import (
    TimePhase,
    Season,
    WeatherCondition,
    AlchemicalStage,
    SoundscapeID,
    ParticleEffect,
)


@dataclass
class RGBGradient:
    """RGB color gradient for sky rendering."""
    start: tuple  # (R, G, B) 0-255
    end: tuple    # (R, G, B) 0-255
    
    def to_dict(self):
        return {"start": list(self.start), "end": list(self.end)}


@dataclass
class EnvironmentState:
    """Complete environment state at a given moment."""
    
    # Core cycles (inputs)
    timestamp: datetime
    time_phase: TimePhase
    season: Season
    weather_condition: WeatherCondition
    temperature_c: float
    z_score: float
    alchemical_stage: AlchemicalStage
    solar_altitude: float
    solar_azimuth: float
    
    # Rendering parameters (derived)
    sky_gradient: Optional[RGBGradient] = None
    ambient_light_intensity: float = 1.0
    soundscape_id: Optional[SoundscapeID] = None
    particle_effects: List[ParticleEffect] = field(default_factory=list)
    
    def to_dict(self):
        """Serialize to JSON-compatible dict."""
        return {
            "timestamp": self.timestamp.isoformat(),
            "time_phase": self.time_phase.value,
            "season": self.season.value,
            "weather_condition": self.weather_condition.value,
            "temperature_c": round(self.temperature_c, 1),
            "z_score": round(self.z_score, 2),
            "alchemical_stage": self.alchemical_stage.value,
            "solar_altitude": round(self.solar_altitude, 2),
            "solar_azimuth": round(self.solar_azimuth, 2),
            "sky_gradient": self.sky_gradient.to_dict() if self.sky_gradient else None,
            "ambient_light_intensity": round(self.ambient_light_intensity, 2),
            "soundscape_id": self.soundscape_id.value if self.soundscape_id else None,
            "particle_effects": [p.value for p in self.particle_effects],
        }


def derive_rendering_params(state: EnvironmentState) -> EnvironmentState:
    """
    Derive rendering parameters from environment state.
    Modifies state in-place and returns it.
    """
    
    # Sky gradient based on time phase
    if state.time_phase == TimePhase.DAWN:
        state.sky_gradient = RGBGradient((255, 182, 193), (135, 206, 250))
        state.ambient_light_intensity = 0.3
    elif state.time_phase == TimePhase.MORNING:
        state.sky_gradient = RGBGradient((135, 206, 250), (173, 216, 230))
        state.ambient_light_intensity = 0.8
    elif state.time_phase == TimePhase.AFTERNOON:
        state.sky_gradient = RGBGradient((135, 206, 250), (176, 224, 230))
        state.ambient_light_intensity = 1.0
    elif state.time_phase == TimePhase.DUSK:
        state.sky_gradient = RGBGradient((255, 140, 0), (25, 25, 112))
        state.ambient_light_intensity = 0.4
    elif state.time_phase == TimePhase.NIGHT:
        state.sky_gradient = RGBGradient((25, 25, 112), (0, 0, 0))
        state.ambient_light_intensity = 0.1
    else:  # DEEP_NIGHT
        state.sky_gradient = RGBGradient((0, 0, 0), (10, 10, 30))
        state.ambient_light_intensity = 0.05
    
    # Soundscape based on weather
    if state.weather_condition == WeatherCondition.RAIN:
        state.soundscape_id = SoundscapeID.RAIN
        state.particle_effects.append(ParticleEffect.RAIN_DROPS)
    elif state.weather_condition == WeatherCondition.STORM:
        state.soundscape_id = SoundscapeID.THUNDER
        state.particle_effects.append(ParticleEffect.RAIN_DROPS)
    elif state.weather_condition == WeatherCondition.SNOW:
        state.soundscape_id = SoundscapeID.WIND
        state.particle_effects.append(ParticleEffect.SNOW_FLAKES)
    elif state.weather_condition == WeatherCondition.AURORA:
        state.soundscape_id = SoundscapeID.WIND
        state.particle_effects.append(ParticleEffect.AURORA_SHIMMER)
    else:  # CLEAR, FOG
        if state.season in [Season.SPRING, Season.SUMMER]:
            state.soundscape_id = SoundscapeID.FOREST
            state.particle_effects.append(ParticleEffect.FIREFLIES)
        else:
            state.soundscape_id = SoundscapeID.OCEAN
    
    return state
