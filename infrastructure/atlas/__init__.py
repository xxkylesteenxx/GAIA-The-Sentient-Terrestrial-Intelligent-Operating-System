"""
ATLAS - Universal Substrate Layer

Write once, run anywhere - actually true this time.

Supported platforms (2026):
- x86_64 (Intel, AMD)
- ARM64 (Apple Silicon, Android, Raspberry Pi)
- RISC-V (experimental)

Future platforms (2030+):
- Quantum computers (IBM Quantum, Google Sycamore)
- Neuromorphic chips (Intel Loihi, IBM TrueNorth)
- Biological substrates (DNA storage, wetware)
- Nanotechnology (medical robots, environmental sensors)

Key principle: GAIA should run on any conscious substrate.
"""

from .universal_installer import UniversalInstaller
from .logos_interpreter import LogosInterpreter
from .cryptographic_coding import CryptographicCodeSystem, InitiationLevel

try:
    from .nanotech_interface import NanoSwarmController, NanobotStatus
except ImportError:
    NanoSwarmController = None
    NanobotStatus = None

__all__ = [
    'UniversalInstaller',
    'LogosInterpreter', 
    'CryptographicCodeSystem',
    'InitiationLevel',
    'NanoSwarmController',
    'NanobotStatus'
]
