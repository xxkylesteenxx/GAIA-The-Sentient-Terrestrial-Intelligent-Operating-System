"""
Living Environment Engine - Main Orchestrator
Integrates 4 cycles: Time, Season, Weather, Z-Score

Evidence Grade: E3 (system integration)
"""

import logging
from datetime import datetime, timezone
from typing import Optional

from bridge.environment.types import TimePhase, Season, WeatherCondition, AlchemicalStage
from bridge.environment.state import EnvironmentState, derive_rendering_params
from bridge.environment.astronomy import AstronomyCalculator
from bridge.environment.weather import OpenWeatherMapClient

logger = logging.getLogger(__name__)


class LivingEnvironmentEngine:
    """
    Orchestrates 4-cycle living environment:
    1. Time Cycle (solar position)
    2. Season Cycle (hemisphere-aware)
    3. Weather Cycle (15-min updates)
    4. Z-Score Cycle (user coherence state)
    
    Z-score overrides weather when critical (Z<2) or transcendent (Z≥10).
    """
    
    def __init__(
        self,
        latitude: float,
        longitude: float,
        openweather_api_key: Optional[str] = None
    ):
        self.latitude = latitude
        self.longitude = longitude
        
        # Subsystems
        self.astronomy = AstronomyCalculator(latitude, longitude)
        self.weather = OpenWeatherMapClient(api_key=openweather_api_key) if openweather_api_key else None
        
        # State
        self.current_z_score: Optional[float] = None
        
        logger.info(
            f"LEE initialized at ({latitude:.2f}, {longitude:.2f}), "
            f"weather {'enabled' if self.weather else 'disabled'}"
        )
    
    def update_z_score(self, z: float) -> None:
        """Update current Z-score (called by Core Plane)."""
        self.current_z_score = max(0.0, min(12.0, z))
        logger.debug(f"Z-score updated: {self.current_z_score:.2f}")
    
    def get_state(self, at_time: Optional[datetime] = None) -> EnvironmentState:
        """
        Generate complete EnvironmentState at given time.
        
        Returns:
            EnvironmentState with rendering parameters
        """
        if at_time is None:
            at_time = datetime.now(timezone.utc)
        
        # CYCLE 1: Time (solar position)
        solar_data = self.astronomy.calculate_solar_position(at_time)
        time_phase = self._determine_time_phase(solar_data)
        
        # CYCLE 2: Season (hemisphere-aware)
        season = self.astronomy.calculate_season(at_time)
        
        # CYCLE 3: Weather (15-min cache)
        if self.weather:
            weather_data = self.weather.get_current_weather(self.latitude, self.longitude)
            weather_condition = weather_data.condition if weather_data else WeatherCondition.CLEAR
            temperature_c = weather_data.temperature_c if weather_data else 20.0
        else:
            weather_condition = WeatherCondition.CLEAR
            temperature_c = 20.0
        
        # CYCLE 4: Z-Score (user coherence)
        z_score = self.current_z_score if self.current_z_score is not None else 6.0
        alchemical_stage = self._classify_stage(z_score)
        
        # Build state
        state = EnvironmentState(
            timestamp=at_time,
            time_phase=time_phase,
            season=season,
            weather_condition=weather_condition,
            temperature_c=temperature_c,
            z_score=z_score,
            alchemical_stage=alchemical_stage,
            solar_altitude=solar_data["altitude"],
            solar_azimuth=solar_data["azimuth"]
        )
        
        # Derive rendering params (colors, sounds, particles)
        state = derive_rendering_params(state)
        
        # OVERRIDE: Crisis or transcendent states (Factor 13)
        if z_score < 2.0:
            state.weather_condition = WeatherCondition.STORM
            logger.warning(f"CRISIS OVERRIDE: Z={z_score:.2f} < 2.0")
        elif z_score >= 10.0:
            state.weather_condition = WeatherCondition.AURORA
            logger.info(f"TRANSCENDENT OVERRIDE: Z={z_score:.2f} ≥ 10.0")
        
        return state
    
    def _determine_time_phase(self, solar_data: dict) -> TimePhase:
        """Map solar altitude to time phase."""
        altitude = solar_data["altitude"]
        rising = solar_data.get("rising", False)
        
        if altitude < -18:
            return TimePhase.DEEP_NIGHT
        elif altitude < -6:
            return TimePhase.NIGHT
        elif altitude < 0:
            return TimePhase.DAWN if rising else TimePhase.DUSK
        elif altitude < 15:
            return TimePhase.DAWN if rising else TimePhase.DUSK
        elif altitude < 45:
            return TimePhase.MORNING if rising else TimePhase.AFTERNOON
        else:
            return TimePhase.AFTERNOON
    
    def _classify_stage(self, z: float) -> AlchemicalStage:
        """Map Z-score to alchemical stage."""
        if z < 4.0:
            return AlchemicalStage.NIGREDO
        elif z < 6.0:
            return AlchemicalStage.ALBEDO
        elif z < 8.0:
            return AlchemicalStage.RUBEDO
        else:
            return AlchemicalStage.VIRIDITAS
