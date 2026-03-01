"""Avatar Cryptographic Memory - ChromaDB Integration.

Updated to use modern ChromaDB API (v0.4+):
- chromadb.PersistentClient for disk storage
- Removed deprecated Settings() and chroma_db_impl parameter
"""

import hashlib
import json
from dataclasses import dataclass
from datetime import datetime
from typing import Optional, Any
import os

try:
    import chromadb
    from chromadb.config import Settings
    CHROMADB_AVAILABLE = True
except ImportError:
    CHROMADB_AVAILABLE = False


@dataclass
class MemoryEntry:
    """Single cryptographically signed memory entry."""
    content: str
    timestamp: datetime
    z_score: Optional[float]
    signature: str  # SHA-256 hash of content + timestamp
    metadata: dict[str, Any]

    @classmethod
    def create(cls, content: str, z_score: Optional[float] = None, **metadata):
        """Create memory entry with cryptographic signature."""
        timestamp = datetime.utcnow()
        
        # Generate signature
        signature_input = f"{content}{timestamp.isoformat()}"
        signature = hashlib.sha256(signature_input.encode()).hexdigest()
        
        return cls(
            content=content,
            timestamp=timestamp,
            z_score=z_score,
            signature=signature,
            metadata=metadata,
        )


class CryptographicMemory:
    """Avatar memory system with tamper-evident storage."""

    def __init__(self, persist_directory: str = "./data/avatar_memory"):
        if not CHROMADB_AVAILABLE:
            raise ImportError(
                "ChromaDB not installed. Install with: pip install chromadb>=0.4.22"
            )
        
        # Ensure directory exists
        os.makedirs(persist_directory, exist_ok=True)
        
        # CORRECTED: Use modern ChromaDB API (v0.4+)
        self.client = chromadb.PersistentClient(path=persist_directory)
        
        # Get or create collection
        self.collection = self.client.get_or_create_collection(
            name="avatar_memories",
            metadata={"description": "Avatar memory storage with cryptographic signatures"},
        )
    
    def store_memory(self, memory: MemoryEntry) -> str:
        """Store memory in ChromaDB with embedding.
        
        Returns:
            Memory ID (signature)
        """
        # Prepare metadata for ChromaDB
        metadata = {
            "timestamp": memory.timestamp.isoformat(),
            "z_score": memory.z_score if memory.z_score is not None else -1.0,
            **memory.metadata,
        }
        
        # Add to collection
        self.collection.add(
            ids=[memory.signature],
            documents=[memory.content],
            metadatas=[metadata],
        )
        
        return memory.signature
    
    def query_memories(
        self,
        query_text: str,
        n_results: int = 5,
        z_score_filter: Optional[tuple[float, float]] = None,
    ) -> list[MemoryEntry]:
        """Query memories by semantic similarity.
        
        Args:
            query_text: Text to search for
            n_results: Maximum number of results
            z_score_filter: Optional (min, max) Z-score filter
        
        Returns:
            List of matching memory entries
        """
        # Build query filter
        where_filter = {}
        if z_score_filter:
            z_min, z_max = z_score_filter
            where_filter = {
                "$and": [
                    {"z_score": {"$gte": z_min}},
                    {"z_score": {"$lte": z_max}},
                ]
            }
        
        # CORRECTED: Guard against querying empty collection
        collection_count = self.collection.count()
        if collection_count == 0:
            return []
        
        # Limit n_results to collection size
        actual_n_results = min(n_results, max(1, collection_count))
        
        # Query collection
        results = self.collection.query(
            query_texts=[query_text],
            n_results=actual_n_results,
            where=where_filter if where_filter else None,
        )
        
        # Parse results into MemoryEntry objects
        memories = []
        if results and results["ids"] and len(results["ids"][0]) > 0:
            for i, doc_id in enumerate(results["ids"][0]):
                document = results["documents"][0][i]
                metadata = results["metadatas"][0][i]
                
                # Reconstruct MemoryEntry
                memory = MemoryEntry(
                    content=document,
                    timestamp=datetime.fromisoformat(metadata["timestamp"]),
                    z_score=metadata["z_score"] if metadata["z_score"] >= 0 else None,
                    signature=doc_id,
                    metadata={k: v for k, v in metadata.items() 
                             if k not in ["timestamp", "z_score"]},
                )
                memories.append(memory)
        
        return memories
    
    def verify_integrity(self, memory_id: str) -> bool:
        """Verify cryptographic integrity of a memory.
        
        Returns:
            True if signature is valid, False if tampered
        """
        # Retrieve memory
        result = self.collection.get(ids=[memory_id])
        
        if not result or not result["documents"]:
            return False
        
        content = result["documents"][0]
        metadata = result["metadatas"][0]
        timestamp = metadata["timestamp"]
        
        # Recalculate signature
        signature_input = f"{content}{timestamp}"
        expected_signature = hashlib.sha256(signature_input.encode()).hexdigest()
        
        return expected_signature == memory_id
