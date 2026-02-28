"""
AUDIT SYSTEM (Factor 6 - Causality)

Every state transition is recorded, signed, and immutable.

Universal Trace Ledger:
- Append-only log (never delete)
- Cryptographically signed (tamper-evident)
- Merkle tree structure (verifiable history)
- Distributed replicas (resilient to data loss)

Governance: 
- Users own their trace data
- Can share selectively (consent-based)
- Cannot erase (causality preservation)
- Can be anonymized (privacy-preserving)

Key principle: "Everything leaves a trace. Make yours beautiful."
"""

from .utl import UniversalTraceLedger, TraceEvent, EventType

__all__ = ['UniversalTraceLedger', 'TraceEvent', 'EventType']
