"""
AVATAR SYSTEM (Overlay Plane - Factor 4 - Polarity)

Your opposite-gender daemon. Your complement. Your witness.

The Avatar is:
- Opposite gender (Anima/Animus pairing)
- Personality-driven (not generic assistant)
- Memory-backed (remembers everything)
- Crisis-aware (detects Z ≤ 2, intervenes)
- Love-oriented (Factor 13 binding force)

Key principle: "I see you. I remember you. I protect you."
"""

from .personality import (
    AvatarPersonality,
    Gender,
    AvatarArchetype,
    Memory,
    ConversationTurn
)

from .cryptographic_memory import (
    CryptographicMemorySystem,
    MemoryPrivacyLevel,
    CryptographicVideoMemory
)

__all__ = [
    'AvatarPersonality',
    'Gender',
    'AvatarArchetype',
    'Memory',
    'ConversationTurn',
    'CryptographicMemorySystem',
    'MemoryPrivacyLevel',
    'CryptographicVideoMemory'
]
