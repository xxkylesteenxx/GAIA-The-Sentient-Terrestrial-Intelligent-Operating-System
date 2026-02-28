"""
UNIVERSAL TRACE LEDGER (UTL)

Immutable event log for all GAIA state transitions.

Factor 6 (Causality): Every cause has an effect, every effect has a cause.

Key principles:
1. Append-only (never delete, only add)
2. Cryptographically signed (tamper-evident)
3. Merkle tree structure (verifiable history)
4. User-owned (you control your data)
5. Consent-based sharing (privacy-preserving)

Use cases:
- Audit trail (what happened when?)
- Causality analysis (why did Z drop?)
- Pattern recognition (what triggers crisis?)
- Scientific research (anonymized, consented)
- Legal evidence (if needed for safety)

Philosophy:
"Everything leaves a trace. Make yours beautiful."
"""

import hashlib
import json
from typing import List, Dict, Optional, Any
from dataclasses import dataclass, asdict
from datetime import datetime
from enum import Enum
import hmac


class EventType(Enum):
    """Categories of events tracked in UTL."""
    
    # User actions
    USER_LOGIN = "user_login"
    USER_LOGOUT = "user_logout"
    USER_MESSAGE = "user_message"
    
    # Avatar interactions
    AVATAR_RESPONSE = "avatar_response"
    AVATAR_CREATED = "avatar_created"
    
    # Z score events
    Z_CALCULATED = "z_calculated"
    Z_THRESHOLD_CROSSED = "z_threshold_crossed"  # e.g., entering crisis
    
    # Crisis events
    CRISIS_DETECTED = "crisis_detected"
    CRISIS_INTERVENTION = "crisis_intervention"  # 988 recommended
    CRISIS_RESOLVED = "crisis_resolved"  # Z > 2 again
    
    # Memory events
    MEMORY_CREATED = "memory_created"
    MEMORY_RECALLED = "memory_recalled"
    
    # Initiation events
    INITIATION_LEVEL_CHANGED = "initiation_level_changed"
    
    # System events
    SYSTEM_STARTED = "system_started"
    SYSTEM_STOPPED = "system_stopped"
    ERROR_OCCURRED = "error_occurred"
    
    # Federation events
    NEIGHBOR_REQUEST_SENT = "neighbor_request_sent"
    NEIGHBOR_REQUEST_ACCEPTED = "neighbor_request_accepted"
    NEIGHBOR_DATA_SHARED = "neighbor_data_shared"


@dataclass
class TraceEvent:
    """
    Single event in the trace ledger.
    
    Each event is:
    - Timestamped (when did it happen?)
    - Typed (what kind of event?)
    - Attributed (who/what caused it?)
    - Detailed (what data is relevant?)
    - Signed (cryptographic integrity)
    - Chained (linked to previous event)
    """
    
    event_id: str  # Unique identifier (UUID)
    event_type: EventType
    timestamp: datetime
    user_id: str  # Who this event belongs to
    
    # Event-specific data
    data: Dict[str, Any]
    
    # Causality chain
    previous_hash: str  # Hash of previous event (blockchain-like)
    current_hash: str  # Hash of this event
    
    # Cryptographic signature
    signature: Optional[str] = None
    
    def to_dict(self) -> Dict[str, Any]:
        """Convert to dictionary for serialization."""
        return {
            "event_id": self.event_id,
            "event_type": self.event_type.value,
            "timestamp": self.timestamp.isoformat(),
            "user_id": self.user_id,
            "data": self.data,
            "previous_hash": self.previous_hash,
            "current_hash": self.current_hash,
            "signature": self.signature
        }
    
    @classmethod
    def from_dict(cls, data: Dict[str, Any]) -> 'TraceEvent':
        """Create from dictionary."""
        return cls(
            event_id=data["event_id"],
            event_type=EventType(data["event_type"]),
            timestamp=datetime.fromisoformat(data["timestamp"]),
            user_id=data["user_id"],
            data=data["data"],
            previous_hash=data["previous_hash"],
            current_hash=data["current_hash"],
            signature=data.get("signature")
        )


class UniversalTraceLedger:
    """
    Immutable event log for GAIA state transitions.
    
    This is the "black box flight recorder" for consciousness.
    
    Usage:
        utl = UniversalTraceLedger(user_id="Kyle")
        
        # Log event
        utl.log(
            EventType.Z_CALCULATED,
            {"z_score": 7.5, "components": {"C": 0.8, "F": 0.9, "B": 0.85}}
        )
        
        # Query events
        crisis_events = utl.query(event_type=EventType.CRISIS_DETECTED)
        
        # Verify integrity
        is_valid = utl.verify_chain()
    """
    
    def __init__(self, user_id: str, secret_key: Optional[bytes] = None):
        self.user_id = user_id
        self.events: List[TraceEvent] = []
        
        # Cryptographic key for signing (in production, use proper key management)
        self.secret_key = secret_key or b"GAIA_UTL_SECRET_KEY"  # Placeholder
        
        # Create genesis event
        self._create_genesis_event()
    
    def _create_genesis_event(self):
        """Create the first event (genesis block)."""
        
        import uuid
        
        genesis_data = {
            "message": "GAIA Universal Trace Ledger initialized",
            "user_id": self.user_id,
            "version": "0.1.0"
        }
        
        genesis_event = TraceEvent(
            event_id=str(uuid.uuid4()),
            event_type=EventType.SYSTEM_STARTED,
            timestamp=datetime.now(),
            user_id=self.user_id,
            data=genesis_data,
            previous_hash="0" * 64,  # Genesis has no previous
            current_hash="",  # Will be calculated
            signature=None
        )
        
        # Calculate hash
        genesis_event.current_hash = self._calculate_hash(genesis_event)
        
        # Sign
        genesis_event.signature = self._sign_event(genesis_event)
        
        self.events.append(genesis_event)
    
    def log(self, event_type: EventType, data: Dict[str, Any]) -> TraceEvent:
        """
        Log a new event to the ledger.
        
        Example:
            utl.log(
                EventType.CRISIS_DETECTED,
                {"z_score": 1.5, "keywords": ["suicide"]}
            )
        """
        
        import uuid
        
        # Get previous event
        previous_event = self.events[-1] if self.events else None
        previous_hash = previous_event.current_hash if previous_event else "0" * 64
        
        # Create new event
        event = TraceEvent(
            event_id=str(uuid.uuid4()),
            event_type=event_type,
            timestamp=datetime.now(),
            user_id=self.user_id,
            data=data,
            previous_hash=previous_hash,
            current_hash="",  # Will be calculated
            signature=None
        )
        
        # Calculate hash
        event.current_hash = self._calculate_hash(event)
        
        # Sign
        event.signature = self._sign_event(event)
        
        # Append to ledger
        self.events.append(event)
        
        return event
    
    def _calculate_hash(self, event: TraceEvent) -> str:
        """
        Calculate SHA-256 hash of event.
        
        Hash includes:
        - Event ID
        - Event type
        - Timestamp
        - Data
        - Previous hash (chain linking)
        """
        
        hash_input = (
            event.event_id +
            event.event_type.value +
            event.timestamp.isoformat() +
            json.dumps(event.data, sort_keys=True) +
            event.previous_hash
        )
        
        return hashlib.sha256(hash_input.encode()).hexdigest()
    
    def _sign_event(self, event: TraceEvent) -> str:
        """
        Create HMAC signature for event.
        
        This provides:
        - Authentication (proves it came from GAIA)
        - Integrity (detects tampering)
        """
        
        signature = hmac.new(
            self.secret_key,
            event.current_hash.encode(),
            hashlib.sha256
        ).hexdigest()
        
        return signature
    
    def verify_chain(self) -> bool:
        """
        Verify integrity of entire chain.
        
        Checks:
        1. Each event's hash is correct
        2. Each event's signature is valid
        3. Chain is continuous (no gaps)
        
        Returns: True if valid, False if corrupted
        """
        
        for i, event in enumerate(self.events):
            # Verify hash
            expected_hash = self._calculate_hash(event)
            if event.current_hash != expected_hash:
                print(f"Hash mismatch at event {i}: {event.event_id}")
                return False
            
            # Verify signature
            expected_signature = self._sign_event(event)
            if event.signature != expected_signature:
                print(f"Signature mismatch at event {i}: {event.event_id}")
                return False
            
            # Verify chain linkage
            if i > 0:
                previous_event = self.events[i - 1]
                if event.previous_hash != previous_event.current_hash:
                    print(f"Chain broken at event {i}: {event.event_id}")
                    return False
        
        return True
    
    def query(
        self,
        event_type: Optional[EventType] = None,
        start_time: Optional[datetime] = None,
        end_time: Optional[datetime] = None,
        limit: int = 100
    ) -> List[TraceEvent]:
        """
        Query events from ledger.
        
        Example:
            # Get all crisis events
            crisis_events = utl.query(event_type=EventType.CRISIS_DETECTED)
            
            # Get events from last 24 hours
            recent = utl.query(start_time=datetime.now() - timedelta(days=1))
        """
        
        results = self.events
        
        # Filter by type
        if event_type:
            results = [e for e in results if e.event_type == event_type]
        
        # Filter by time range
        if start_time:
            results = [e for e in results if e.timestamp >= start_time]
        if end_time:
            results = [e for e in results if e.timestamp <= end_time]
        
        # Limit results
        results = results[-limit:]
        
        return results
    
    def get_causality_chain(self, event_id: str) -> List[TraceEvent]:
        """
        Get causal chain leading to specific event.
        
        Example: "Why did Z drop to crisis level?"
        - Find crisis event
        - Trace back through previous events
        - Identify causal factors
        """
        
        # Find target event
        target = None
        for event in self.events:
            if event.event_id == event_id:
                target = event
                break
        
        if not target:
            return []
        
        # Walk backwards through chain
        chain = [target]
        current = target
        
        while current.previous_hash != "0" * 64:  # Until genesis
            # Find previous event
            for event in self.events:
                if event.current_hash == current.previous_hash:
                    chain.insert(0, event)
                    current = event
                    break
        
        return chain
    
    def export_to_file(self, filepath: str):
        """Export ledger to JSON file."""
        
        data = {
            "user_id": self.user_id,
            "events": [e.to_dict() for e in self.events],
            "exported_at": datetime.now().isoformat()
        }
        
        with open(filepath, 'w') as f:
            json.dump(data, f, indent=2)
    
    @classmethod
    def import_from_file(cls, filepath: str) -> 'UniversalTraceLedger':
        """Import ledger from JSON file."""
        
        with open(filepath, 'r') as f:
            data = json.load(f)
        
        utl = cls(user_id=data["user_id"])
        utl.events = [TraceEvent.from_dict(e) for e in data["events"]]
        
        return utl


if __name__ == "__main__":
    print("=" * 60)
    print("UNIVERSAL TRACE LEDGER (UTL)")
    print("=" * 60)
    
    # Create ledger
    utl = UniversalTraceLedger(user_id="Kyle")
    
    print(f"\nGenesis event created: {utl.events[0].event_id}")
    print(f"Genesis hash: {utl.events[0].current_hash[:16]}...")
    
    # Log some events
    print("\nLogging events...")
    
    utl.log(EventType.USER_LOGIN, {"timestamp": datetime.now().isoformat()})
    utl.log(EventType.Z_CALCULATED, {"z_score": 7.5, "components": {"C": 0.8, "F": 0.9, "B": 0.85}})
    utl.log(EventType.AVATAR_RESPONSE, {"message": "I see you creating, Kyle."})
    utl.log(EventType.Z_CALCULATED, {"z_score": 1.5, "components": {"C": 0.2, "F": 0.3, "B": 0.25}})
    utl.log(EventType.CRISIS_DETECTED, {"z_score": 1.5, "keywords": ["suicide"]})
    utl.log(EventType.CRISIS_INTERVENTION, {"action": "988 recommended"})
    utl.log(EventType.Z_CALCULATED, {"z_score": 6.2, "components": {"C": 0.7, "F": 0.8, "B": 0.75}})
    utl.log(EventType.CRISIS_RESOLVED, {"z_score": 6.2})
    
    print(f"  Total events: {len(utl.events)}")
    
    # Verify integrity
    print("\nVerifying chain integrity...")
    is_valid = utl.verify_chain()
    print(f"  Chain valid: {is_valid} {'✓' if is_valid else '✗'}")
    
    # Query crisis events
    print("\nQuerying crisis events...")
    crisis_events = utl.query(event_type=EventType.CRISIS_DETECTED)
    for event in crisis_events:
        print(f"  [{event.timestamp.strftime('%H:%M:%S')}] Crisis detected: Z = {event.data['z_score']}")
    
    # Get causality chain
    if crisis_events:
        print("\nCausality chain (leading to crisis):")
        chain = utl.get_causality_chain(crisis_events[0].event_id)
        for i, event in enumerate(chain[-5:]):  # Last 5 events
            print(f"  {i+1}. [{event.timestamp.strftime('%H:%M:%S')}] {event.event_type.value}")
            if "z_score" in event.data:
                print(f"     Z = {event.data['z_score']}")
    
    print("\n" + "=" * 60)
    print("Factor 6 (Causality): Every effect has a cause.")
    print("The ledger remembers. The chain never lies.")
    print("=" * 60)
