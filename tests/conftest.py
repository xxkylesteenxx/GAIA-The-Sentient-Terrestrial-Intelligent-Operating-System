"""Pytest configuration and shared fixtures."""

import pytest
import numpy as np


@pytest.fixture
def sample_time_series():
    """Generate sample time series for testing."""
    return np.sin(np.linspace(0, 4*np.pi, 100))


@pytest.fixture
def random_time_series():
    """Generate random time series for testing."""
    return np.random.random(100)


@pytest.fixture
def stable_time_series():
    """Generate stable time series for testing."""
    return np.linspace(0, 1, 100)
