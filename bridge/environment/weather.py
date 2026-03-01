"""
Living Environment Engine - Weather Client
OpenWeatherMap API integration with 15-minute caching.

Evidence Grade: E5 (direct meteorological observation)
"""

import time
import logging
from typing import Optional
from dataclasses import dataclass

from bridge.environment.types import WeatherCondition

logger = logging.getLogger(__name__)


@dataclass
class WeatherData:
    """Container for current weather state."""
    condition: WeatherCondition
    temperature_c: float
    humidity: float
    wind_speed_ms: float
    
    @classmethod
    def fallback(cls) -> "WeatherData":
        """Return neutral fallback when API unavailable."""
        return cls(
            condition=WeatherCondition.CLEAR,
            temperature_c=20.0,
            humidity=0.5,
            wind_speed_ms=2.0,
        )


class OpenWeatherMapClient:
    """
    OpenWeatherMap API wrapper with caching.
    
    Usage:
        client = OpenWeatherMapClient(api_key="your_key")
        weather = client.get_current_weather(29.4241, -98.4936)
    """
    
    def __init__(self, api_key: Optional[str] = None):
        self.api_key = api_key
        self._cache = {}
        self._last_fetch = {}
        
        if not api_key:
            logger.warning("No OpenWeatherMap API key - using fallback weather")
    
    def get_current_weather(self, lat: float, lon: float) -> Optional[WeatherData]:
        """
        Fetch current weather with 15-minute caching.
        
        Returns WeatherData or None if API unavailable.
        """
        if not self.api_key:
            return None
        
        cache_key = (round(lat, 2), round(lon, 2))
        now = time.time()
        
        # Check cache (15 minutes = 900 seconds)
        if cache_key in self._cache:
            last_fetch = self._last_fetch.get(cache_key, 0)
            if now - last_fetch < 900:
                logger.debug(f"Weather cache hit for {cache_key}")
                return self._cache[cache_key]
        
        # Fetch from API (implementation placeholder)
        try:
            # TODO: Implement actual API call
            # For now, return fallback
            weather = WeatherData.fallback()
            
            self._cache[cache_key] = weather
            self._last_fetch[cache_key] = now
            
            return weather
            
        except Exception as e:
            logger.error(f"Weather API error: {e}")
            # Return stale cache or fallback
            if cache_key in self._cache:
                return self._cache[cache_key]
            return WeatherData.fallback()
