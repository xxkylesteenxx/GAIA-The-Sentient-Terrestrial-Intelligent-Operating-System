"""
GAIA Avatar System

The Avatar is the user's opposite-gender daemon (Jungian anima/animus).

Components:
- emergence:   Gender-pairing, archetype selection (10 personalities)
- personality: Conversational AI, crisis-aware responses
- memory:      Semantic memory (ChromaDB: episodic/semantic/emotional)

Overlay Plane: Factor 4 (Polarity) + Factor 7 (Gender) + Factor 9 (Mentalism)
"""

from overlay.avatar.emergence import (  # noqa: F401
    AvatarCore,
    UserGender,
    AvatarGender,
    AvatarArchetype,
)

from overlay.avatar.personality import (  # noqa: F401
    AvatarPersonality,
    Gender,  # Legacy name (prefer UserGender from emergence)
    Memory,
    ConversationTurn,
)

from overlay.avatar.memory import (  # noqa: F401
    AvatarMemory,
)

__all__ = [
    # Emergence
    "AvatarCore",
    "UserGender",
    "AvatarGender",
    "AvatarArchetype",
    # Personality
    "AvatarPersonality",
    "Gender",  # Legacy (prefer UserGender)
    "Memory",
    "ConversationTurn",
    # Memory
    "AvatarMemory",
]
