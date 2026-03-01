"""
AVATAR SEMANTIC MEMORY SYSTEM
Overlay Plane — Factor 6 (Causality) + Factor 9 (Mentalism)

Long-term memory using ChromaDB for:
    - Episodic memory:   User interactions and experiences
    - Semantic memory:   Learned concepts and relationships
    - Emotional memory:  Affective states and triggers

ChromaDB API note:
    Uses the modern chromadb.PersistentClient (chromadb ≥ 0.4.0).
    The deprecated chromadb.Client(Settings(chroma_db_impl=...)) API
    was removed in 0.4.0 and will raise TypeError on import.

Memory privacy: all content is stored locally. Nothing leaves the device
without explicit user consent (Federation consent protocol, Phase 2).
"""

from __future__ import annotations

import json
import logging
from datetime import datetime
from typing import Dict, List, Optional

import chromadb

logger = logging.getLogger(__name__)


class AvatarMemory:
    """
    Semantic memory system for the Avatar.

    Usage::

        memory = AvatarMemory(persist_directory="./data/avatar_memory")

        # Store
        memory.store_episode("We talked about GAIA architecture today.")
        memory.store_emotion("joy", "Finished the Logos interpreter.", 0.9, 8.5)

        # Recall
        episodes = memory.recall_episodes("GAIA architecture", n_results=3)
        for ep in episodes:
            print(ep["content"])

    Collections:
        episodic   — timestamped interaction records
        semantic   — named concepts with definitions
        emotional  — affective state snapshots keyed to Z-score
    """

    def __init__(self, persist_directory: str = "./data/avatar_memory") -> None:
        """
        Initialise the memory system.

        Args:
            persist_directory: Path for ChromaDB persistent storage.
                               Directory is created if it does not exist.
        """
        # Modern API: PersistentClient replaces the deprecated
        # chromadb.Client(Settings(chroma_db_impl="duckdb+parquet", ...))
        self.client = chromadb.PersistentClient(path=persist_directory)

        # Create (or open) the three memory collections.
        self.episodic = self.client.get_or_create_collection(
            name="episodic_memory",
            metadata={"description": "User interactions and experiences"},
        )
        self.semantic = self.client.get_or_create_collection(
            name="semantic_memory",
            metadata={"description": "Learned concepts and relationships"},
        )
        self.emotional = self.client.get_or_create_collection(
            name="emotional_memory",
            metadata={"description": "Affective states and triggers"},
        )

        logger.info(
            "AvatarMemory initialised at %s  "
            "(episodic=%d, semantic=%d, emotional=%d)",
            persist_directory,
            self.episodic.count(),
            self.semantic.count(),
            self.emotional.count(),
        )

    # ------------------------------------------------------------------ #
    # Store                                                                #
    # ------------------------------------------------------------------ #

    def store_episode(
        self,
        content: str,
        metadata: Optional[Dict] = None,
    ) -> str:
        """
        Store an episodic memory.

        Args:
            content:  Natural language description of the episode.
            metadata: Optional extra metadata dict (will be merged with defaults).

        Returns:
            Unique episode ID.
        """
        episode_id = f"ep_{datetime.now().isoformat()}"

        meta: Dict = metadata.copy() if metadata else {}
        meta.setdefault("timestamp", datetime.now().isoformat())
        meta.setdefault("type", "episode")

        self.episodic.add(
            documents=[content],
            metadatas=[meta],
            ids=[episode_id],
        )

        logger.debug("Stored episode: %s", episode_id)
        return episode_id

    def store_concept(
        self,
        concept: str,
        definition: str,
        related: Optional[List[str]] = None,
    ) -> str:
        """
        Store a semantic concept.

        Args:
            concept:    Human-readable concept name.
            definition: Natural language definition.
            related:    Optional list of related concept IDs.

        Returns:
            Concept ID (deterministic: based on concept name).
        """
        concept_id = f"concept_{concept.lower().replace(' ', '_')}"

        self.semantic.upsert(        # upsert so re-learning a concept works
            documents=[definition],
            metadatas=[{
                "concept": concept,
                "related": json.dumps(related or []),
                "timestamp": datetime.now().isoformat(),
            }],
            ids=[concept_id],
        )

        logger.debug("Stored concept: %s", concept)
        return concept_id

    def store_emotion(
        self,
        emotion: str,
        context: str,
        intensity: float,
        z_score: float,
    ) -> str:
        """
        Store an emotional memory snapshot.

        Args:
            emotion:   Emotion label (e.g. "joy", "grief", "fear").
            context:   Narrative description of the context.
            intensity: Emotion intensity in [0, 1].
            z_score:   Z-score at the moment of experience.

        Returns:
            Unique memory ID.
        """
        memory_id = f"emotion_{datetime.now().isoformat()}"

        self.emotional.add(
            documents=[context],
            metadatas=[{
                "emotion": emotion,
                "intensity": float(intensity),
                "z_score": float(z_score),
                "timestamp": datetime.now().isoformat(),
            }],
            ids=[memory_id],
        )

        logger.debug(
            "Stored emotion: %s (intensity=%.2f, Z=%.2f)",
            emotion, intensity, z_score,
        )
        return memory_id

    # ------------------------------------------------------------------ #
    # Recall                                                               #
    # ------------------------------------------------------------------ #

    def recall_episodes(self, query: str, n_results: int = 5) -> List[Dict]:
        """
        Recall relevant episodic memories via semantic similarity.

        Args:
            query:     Natural language query.
            n_results: Maximum number of results.

        Returns:
            List of dicts with keys: content, metadata, distance.
        """
        # Guard: ChromaDB raises if n_results > collection size
        n = min(n_results, max(1, self.episodic.count()))

        results = self.episodic.query(
            query_texts=[query],
            n_results=n,
        )

        return [
            {
                "content": doc,
                "metadata": meta,
                "distance": dist,
            }
            for doc, meta, dist in zip(
                results["documents"][0],
                results["metadatas"][0],
                results["distances"][0],
            )
        ]

    def recall_concepts(self, query: str, n_results: int = 3) -> List[Dict]:
        """
        Recall relevant semantic concepts.

        Returns list of dicts: concept, definition, related, distance.
        """
        n = min(n_results, max(1, self.semantic.count()))

        results = self.semantic.query(
            query_texts=[query],
            n_results=n,
        )

        return [
            {
                "concept": meta["concept"],
                "definition": doc,
                "related": json.loads(meta.get("related", "[]")),
                "distance": dist,
            }
            for doc, meta, dist in zip(
                results["documents"][0],
                results["metadatas"][0],
                results["distances"][0],
            )
        ]

    def recall_emotions(self, query: str, n_results: int = 5) -> List[Dict]:
        """
        Recall similar emotional experiences.

        Returns list of dicts: emotion, context, intensity, z_score,
        timestamp, distance.
        """
        n = min(n_results, max(1, self.emotional.count()))

        results = self.emotional.query(
            query_texts=[query],
            n_results=n,
        )

        return [
            {
                "emotion": meta["emotion"],
                "context": doc,
                "intensity": meta["intensity"],
                "z_score": meta["z_score"],
                "timestamp": meta["timestamp"],
                "distance": dist,
            }
            for doc, meta, dist in zip(
                results["documents"][0],
                results["metadatas"][0],
                results["distances"][0],
            )
        ]

    # ------------------------------------------------------------------ #
    # Utilities                                                            #
    # ------------------------------------------------------------------ #

    def get_memory_stats(self) -> Dict:
        """Return collection sizes for monitoring / status display."""
        return {
            "episodic_count": self.episodic.count(),
            "semantic_count": self.semantic.count(),
            "emotional_count": self.emotional.count(),
        }

    def clear_all(self) -> None:
        """
        Delete all stored memories.

        WARNING: Irreversible.  Requires explicit user confirmation before
        calling in any UI context.  Never call from automated code.
        """
        for collection in (self.episodic, self.semantic, self.emotional):
            name = collection.name
            self.client.delete_collection(name)

        # Re-create empty collections
        self.episodic = self.client.get_or_create_collection("episodic_memory")
        self.semantic = self.client.get_or_create_collection("semantic_memory")
        self.emotional = self.client.get_or_create_collection("emotional_memory")

        logger.warning("All Avatar memories cleared.")
