"""
Living Environment Engine - Astronomy Calculations
Solar position using simplified NOAA algorithms.

Evidence Grade: E5 (celestial mechanics, SI units)
"""

import math
from datetime import datetime
from typing import Dict

from bridge.environment.types import Season


class AstronomyCalculator:
    """
    Calculate solar position and seasonal information.
    Uses simplified NOAA Solar Calculator algorithms.
    """
    
    def __init__(self, latitude: float, longitude: float):
        self.latitude = latitude
        self.longitude = longitude
    
    def calculate_solar_position(self, dt: datetime) -> Dict:
        """
        Calculate sun altitude and azimuth for given time.
        
        Returns:
            dict with 'altitude', 'azimuth', 'rising'
        """
        # Day of year for approximate solar declination
        day_of_year = dt.timetuple().tm_yday
        
        # Approximate solar declination (degrees)
        declination = 23.45 * math.sin(math.radians((360/365) * (day_of_year - 81)))
        
        # Hour angle (simplified)
        hours_since_midnight = dt.hour + dt.minute/60 + dt.second/3600
        hour_angle = 15 * (hours_since_midnight - 12)  # degrees
        
        # Calculate altitude
        lat_rad = math.radians(self.latitude)
        dec_rad = math.radians(declination)
        ha_rad = math.radians(hour_angle)
        
        sin_alt = (math.sin(lat_rad) * math.sin(dec_rad) + 
                   math.cos(lat_rad) * math.cos(dec_rad) * math.cos(ha_rad))
        altitude = math.degrees(math.asin(max(-1, min(1, sin_alt))))
        
        # Calculate azimuth (north=0, east=90)
        azimuth = 180 + math.degrees(math.atan2(
            math.sin(ha_rad),
            math.cos(ha_rad) * math.sin(lat_rad) - math.tan(dec_rad) * math.cos(lat_rad)
        ))
        
        return {
            "altitude": altitude,
            "azimuth": azimuth % 360,
            "rising": hour_angle < 0
        }
    
    def calculate_season(self, dt: datetime) -> Season:
        """Determine season based on hemisphere and month."""
        month = dt.month
        northern_hemisphere = self.latitude >= 0
        
        # Tropical regions (within 23.5° of equator)
        if abs(self.latitude) < 23.5:
            # Wet: May-October, Dry: November-April
            return Season.WET if 5 <= month <= 10 else Season.DRY
        
        # Northern hemisphere
        if northern_hemisphere:
            if month in [3, 4, 5]:
                return Season.SPRING
            elif month in [6, 7, 8]:
                return Season.SUMMER
            elif month in [9, 10, 11]:
                return Season.AUTUMN
            else:
                return Season.WINTER
        
        # Southern hemisphere (reversed)
        else:
            if month in [3, 4, 5]:
                return Season.AUTUMN
            elif month in [6, 7, 8]:
                return Season.WINTER
            elif month in [9, 10, 11]:
                return Season.SPRING
            else:
                return Season.SUMMER
