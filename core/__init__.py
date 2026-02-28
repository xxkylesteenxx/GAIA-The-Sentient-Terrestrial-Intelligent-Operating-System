"""
CORE PLANE (Factor 11 - Order)

Deterministic reality, hardware constraints, safety enforcement.

Characteristics:
- Fail-closed (errors halt execution, don't corrupt state)
- Physics-bounded (respects energy, memory, bandwidth limits)
- Immutable audit (Universal Trace Ledger)
- Cryptographic integrity (all state transitions signed)

Governance: Ruby (Reality Contract) - Cannot be bypassed
"""

from .z_calculator import ZScoreCalculator, BiosignalData, ZScoreComponents

__all__ = ['ZScoreCalculator', 'BiosignalData', 'ZScoreComponents']
