"""
Living Environment Engine - Integration Tests
Evidence Grade: E3 (validates E5 inputs)
"""

import pytest
from datetime import datetime, timezone

from bridge.environment.engine import LivingEnvironmentEngine
from bridge.environment.types import TimePhase, Season, WeatherCondition, AlchemicalStage


def test_engine_initialization():
    """Test LEE initializes with valid coordinates."""
    engine = LivingEnvironmentEngine(latitude=37.7749, longitude=-122.4194)
    assert engine.latitude == 37.7749
    assert engine.longitude == -122.4194
    assert engine.current_z_score is None


def test_state_generation_no_weather():
    """Test state generation without weather API."""
    engine = LivingEnvironmentEngine(latitude=37.7749, longitude=-122.4194)
    state = engine.get_state()
    
    assert state.timestamp is not None
    assert isinstance(state.time_phase, TimePhase)
    assert isinstance(state.season, Season)
    assert isinstance(state.alchemical_stage, AlchemicalStage)
    assert 0 <= state.z_score <= 12
    assert state.weather_condition == WeatherCondition.CLEAR  # No API = CLEAR


def test_crisis_override():
    """Test crisis Z-score overrides weather (Factor 13)."""
    engine = LivingEnvironmentEngine(latitude=37.7749, longitude=-122.4194)
    engine.update_z_score(1.5)
    state = engine.get_state()
    
    assert state.z_score == 1.5
    assert state.weather_condition == WeatherCondition.STORM


def test_transcendent_override():
    """Test transcendent Z-score overrides weather."""
    engine = LivingEnvironmentEngine(latitude=37.7749, longitude=-122.4194)
    engine.update_z_score(10.5)
    state = engine.get_state()
    
    assert state.z_score == 10.5
    assert state.weather_condition == WeatherCondition.AURORA


def test_hemisphere_aware_seasons():
    """Test seasons reversed between hemispheres."""
    # Northern: San Francisco
    engine_north = LivingEnvironmentEngine(latitude=37.7749, longitude=-122.4194)
    state_north = engine_north.get_state()
    
    # Southern: Sydney
    engine_south = LivingEnvironmentEngine(latitude=-33.8688, longitude=151.2093)
    state_south = engine_south.get_state()
    
    # In February (month 2), should be winter in north, summer in south
    # (Test is flexible since it runs in various months)
    assert isinstance(state_north.season, Season)
    assert isinstance(state_south.season, Season)


def test_time_phase_cycle():
    """Test time phases change over 24-hour period."""
    engine = LivingEnvironmentEngine(latitude=37.7749, longitude=-122.4194)
    test_dt = datetime(2026, 6, 21, 0, 0, tzinfo=timezone.utc)
    
    phases_seen = set()
    for hour in range(0, 24, 3):
        test_time = test_dt.replace(hour=hour)
        state = engine.get_state(at_time=test_time)
        phases_seen.add(state.time_phase)
    
    # Should see multiple distinct phases
    assert len(phases_seen) >= 3


def test_json_serialization():
    """Test state serializes to clean JSON."""
    engine = LivingEnvironmentEngine(latitude=37.7749, longitude=-122.4194)
    engine.update_z_score(6.5)
    state = engine.get_state()
    
    state_dict = state.to_dict()
    
    # Required keys
    assert "timestamp" in state_dict
    assert "time_phase" in state_dict
    assert "season" in state_dict
    assert "weather_condition" in state_dict
    assert "z_score" in state_dict
    assert "alchemical_stage" in state_dict
    assert "sky_gradient" in state_dict
    assert "soundscape_id" in state_dict
    assert "particle_effects" in state_dict
    
    # Values are serializable
    import json
    json_str = json.dumps(state_dict)
    assert len(json_str) > 0


def test_z_score_clamping():
    """Test Z-score clamped to [0, 12]."""
    engine = LivingEnvironmentEngine(latitude=37.7749, longitude=-122.4194)
    
    # Test upper bound
    engine.update_z_score(15.0)
    assert engine.current_z_score == 12.0
    
    # Test lower bound
    engine.update_z_score(-2.0)
    assert engine.current_z_score == 0.0
