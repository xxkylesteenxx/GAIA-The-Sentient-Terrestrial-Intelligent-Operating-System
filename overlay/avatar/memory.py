"""Avatar Memory System - ChromaDB Integration

Semantic memory search using vector embeddings.
Avatar remembers:
- Crisis moments (Z < 2)
- Peak moments (Z > 8)
- Important conversations
- User preferences
- Emotional context
"""

import logging
from dataclasses import dataclass, asdict
from datetime import datetime
from typing import List, Optional, Dict, Any
import hashlib
import json

try:
    import chromadb
    from chromadb.config import Settings
    CHROMADB_AVAILABLE = True
except ImportError:
    CHROMADB_AVAILABLE = False
    logging.warning("ChromaDB not installed. Memory will use fallback storage.")

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)


@dataclass
class Memory:
    """A single memory stored by Avatar."""
    memory_id: str
    user_id: str
    timestamp: datetime
    content: str
    zscore: float
    emotion: str
    memory_type: str  # "crisis", "peak", "conversation", "preference"
    significance: float  # 0-1, how important is this memory
    metadata: Dict[str, Any]
    
    def to_dict(self) -> Dict:
        """Convert to dictionary for storage."""
        d = asdict(self)
        d['timestamp'] = self.timestamp.isoformat()
        return d
    
    @classmethod
    def from_dict(cls, d: Dict) -> 'Memory':
        """Create Memory from dictionary."""
        d['timestamp'] = datetime.fromisoformat(d['timestamp'])
        return cls(**d)


class AvatarMemory:
    """Avatar memory system with semantic search.
    
    Uses ChromaDB for vector similarity search when available.
    Falls back to simple list storage otherwise.
    """
    
    def __init__(self, user_id: str, persist_directory: str = ".gaia/memory"):
        """Initialize Avatar memory.
        
        Args:
            user_id: User identifier
            persist_directory: Where to store memory data
        """
        self.user_id = user_id
        self.persist_directory = persist_directory
        
        if CHROMADB_AVAILABLE:
            self._init_chromadb()
        else:
            self._init_fallback()
    
    def _init_chromadb(self):
        """Initialize ChromaDB client."""
        self.client = chromadb.Client(Settings(
            chroma_db_impl="duckdb+parquet",
            persist_directory=self.persist_directory
        ))
        
        # Get or create collection
        self.collection = self.client.get_or_create_collection(
            name=f"avatar_memory_{self.user_id}",
            metadata={"user_id": self.user_id}
        )
        
        logger.info(f"ChromaDB initialized for user {self.user_id}")
    
    def _init_fallback(self):
        """Initialize fallback storage (simple list)."""
        self.memories: List[Memory] = []
        logger.info(f"Using fallback memory storage for user {self.user_id}")
    
    def store(
        self,
        content: str,
        zscore: float,
        emotion: str = "neutral",
        memory_type: str = "conversation",
        significance: float = 0.5,
        metadata: Optional[Dict] = None
    ) -> Memory:
        """Store a new memory.
        
        Args:
            content: The memory content (text)
            zscore: Z-score at time of memory
            emotion: Emotional context
            memory_type: Type of memory
            significance: Importance (0-1)
            metadata: Additional metadata
            
        Returns:
            Created Memory object
        """
        # Generate memory ID
        memory_id = hashlib.sha256(
            f"{self.user_id}{content}{datetime.utcnow().isoformat()}".encode()
        ).hexdigest()[:16]
        
        # Create memory
        memory = Memory(
            memory_id=memory_id,
            user_id=self.user_id,
            timestamp=datetime.utcnow(),
            content=content,
            zscore=zscore,
            emotion=emotion,
            memory_type=memory_type,
            significance=significance,
            metadata=metadata or {}
        )
        
        # Store in ChromaDB or fallback
        if CHROMADB_AVAILABLE:
            self.collection.add(
                ids=[memory_id],
                documents=[content],
                metadatas=[{
                    'user_id': self.user_id,
                    'zscore': zscore,
                    'emotion': emotion,
                    'memory_type': memory_type,
                    'significance': significance,
                    'timestamp': memory.timestamp.isoformat()
                }]
            )
        else:
            self.memories.append(memory)
        
        logger.info(
            f"Memory stored: {memory_type} (Z={zscore:.2f}, sig={significance:.2f})"
        )
        
        return memory
    
    def search(
        self,
        query: str,
        limit: int = 5,
        memory_type: Optional[str] = None
    ) -> List[Memory]:
        """Search memories semantically.
        
        Args:
            query: Search query
            limit: Maximum results
            memory_type: Filter by memory type
            
        Returns:
            List of matching memories
        """
        if CHROMADB_AVAILABLE:
            # Semantic search with ChromaDB
            where_filter = {"user_id": self.user_id}
            if memory_type:
                where_filter["memory_type"] = memory_type
            
            results = self.collection.query(
                query_texts=[query],
                n_results=limit,
                where=where_filter
            )
            
            # Convert to Memory objects
            memories = []
            for i, doc_id in enumerate(results['ids'][0]):
                metadata = results['metadatas'][0][i]
                content = results['documents'][0][i]
                
                memory = Memory(
                    memory_id=doc_id,
                    user_id=self.user_id,
                    timestamp=datetime.fromisoformat(metadata['timestamp']),
                    content=content,
                    zscore=metadata['zscore'],
                    emotion=metadata['emotion'],
                    memory_type=metadata['memory_type'],
                    significance=metadata['significance'],
                    metadata={}
                )
                memories.append(memory)
            
            return memories
        else:
            # Fallback: simple text search
            query_lower = query.lower()
            matches = [
                m for m in self.memories
                if query_lower in m.content.lower()
                and (memory_type is None or m.memory_type == memory_type)
            ]
            
            # Sort by significance
            matches.sort(key=lambda m: m.significance, reverse=True)
            
            return matches[:limit]
    
    def get_crisis_memories(self, limit: int = 10) -> List[Memory]:
        """Get crisis memories (Z < 2)."""
        if CHROMADB_AVAILABLE:
            return self.search("crisis emergency help", limit=limit, memory_type="crisis")
        else:
            crisis_memories = [
                m for m in self.memories
                if m.memory_type == "crisis" or m.zscore < 2.0
            ]
            crisis_memories.sort(key=lambda m: m.timestamp, reverse=True)
            return crisis_memories[:limit]
    
    def get_peak_memories(self, limit: int = 10) -> List[Memory]:
        """Get peak experiences (Z > 8)."""
        if CHROMADB_AVAILABLE:
            return self.search("joy happiness achievement", limit=limit, memory_type="peak")
        else:
            peak_memories = [
                m for m in self.memories
                if m.memory_type == "peak" or m.zscore > 8.0
            ]
            peak_memories.sort(key=lambda m: m.timestamp, reverse=True)
            return peak_memories[:limit]
    
    def get_memory_summary(self) -> Dict:
        """Get summary statistics of stored memories."""
        if CHROMADB_AVAILABLE:
            count = self.collection.count()
            # Query for different types
            crisis_count = len(self.get_crisis_memories())
            peak_count = len(self.get_peak_memories())
        else:
            count = len(self.memories)
            crisis_count = len([m for m in self.memories if m.zscore < 2.0])
            peak_count = len([m for m in self.memories if m.zscore > 8.0])
        
        return {
            'total_memories': count,
            'crisis_memories': crisis_count,
            'peak_memories': peak_count,
            'storage_backend': 'chromadb' if CHROMADB_AVAILABLE else 'fallback'
        }


if __name__ == "__main__":
    # Test memory system
    memory_system = AvatarMemory(user_id="kyle")
    
    print("=== AVATAR MEMORY SYSTEM TEST ===")
    print(f"Backend: {memory_system.get_memory_summary()['storage_backend']}\n")
    
    # Store some memories
    print("Storing memories...")
    memory_system.store(
        content="I can't do this anymore. Everything is falling apart.",
        zscore=1.5,
        emotion="despair",
        memory_type="crisis",
        significance=1.0
    )
    
    memory_system.store(
        content="Just finished my painting! I'm so proud of it.",
        zscore=8.5,
        emotion="joy",
        memory_type="peak",
        significance=0.9
    )
    
    memory_system.store(
        content="Avatar, I love the color emerald green. It represents life to me.",
        zscore=7.0,
        emotion="peaceful",
        memory_type="preference",
        significance=0.7
    )
    
    # Search memories
    print("\nSearching for 'painting'...")
    results = memory_system.search("painting", limit=3)
    for memory in results:
        print(f"  [{memory.memory_type}] Z={memory.zscore:.1f}: {memory.content}")
    
    # Get crisis memories
    print("\nCrisis memories:")
    crisis = memory_system.get_crisis_memories()
    for memory in crisis:
        print(f"  Z={memory.zscore:.1f}: {memory.content}")
    
    # Summary
    summary = memory_system.get_memory_summary()
    print("\n=== MEMORY SUMMARY ===")
    print(f"Total memories: {summary['total_memories']}")
    print(f"Crisis memories: {summary['crisis_memories']}")
    print(f"Peak memories: {summary['peak_memories']}")
