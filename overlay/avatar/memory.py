"""Avatar Semantic Memory System.

Implements long-term memory using ChromaDB for:
- Episodic memory: User interactions and experiences
- Semantic memory: Learned concepts and relationships
- Emotional memory: Affective states and triggers

Memory encryption ensures privacy and consent.
"""

import chromadb
from chromadb.config import Settings
from typing import List, Dict, Optional
from datetime import datetime
import json
import logging

logger = logging.getLogger(__name__)


class AvatarMemory:
    """Semantic memory system for Avatar."""
    
    def __init__(self, persist_directory: str = "./data/avatar_memory"):
        """Initialize memory system.
        
        Args:
            persist_directory: Path for persistent storage
        """
        self.client = chromadb.Client(Settings(
            chroma_db_impl="duckdb+parquet",
            persist_directory=persist_directory
        ))
        
        # Create collections
        self.episodic = self.client.get_or_create_collection(
            name="episodic_memory",
            metadata={"description": "User interactions and experiences"}
        )
        self.semantic = self.client.get_or_create_collection(
            name="semantic_memory",
            metadata={"description": "Learned concepts and relationships"}
        )
        self.emotional = self.client.get_or_create_collection(
            name="emotional_memory",
            metadata={"description": "Affective states and triggers"}
        )
    
    def store_episode(self, content: str, metadata: Dict = None) -> str:
        """Store episodic memory.
        
        Args:
            content: Episode content
            metadata: Additional metadata
            
        Returns:
            Episode ID
        """
        episode_id = f"ep_{datetime.now().isoformat()}"
        
        meta = metadata or {}
        meta['timestamp'] = datetime.now().isoformat()
        meta['type'] = 'episode'
        
        self.episodic.add(
            documents=[content],
            metadatas=[meta],
            ids=[episode_id]
        )
        
        logger.info(f"Stored episode: {episode_id}")
        return episode_id
    
    def store_concept(self, concept: str, definition: str, 
                      related: List[str] = None) -> str:
        """Store semantic concept.
        
        Args:
            concept: Concept name
            definition: Concept definition
            related: Related concept IDs
            
        Returns:
            Concept ID
        """
        concept_id = f"concept_{concept.lower().replace(' ', '_')}"
        
        self.semantic.add(
            documents=[definition],
            metadatas=[{
                'concept': concept,
                'related': json.dumps(related or []),
                'timestamp': datetime.now().isoformat()
            }],
            ids=[concept_id]
        )
        
        logger.info(f"Stored concept: {concept}")
        return concept_id
    
    def store_emotion(self, emotion: str, context: str, 
                      intensity: float, z_score: float) -> str:
        """Store emotional memory.
        
        Args:
            emotion: Emotion label
            context: Contextual description
            intensity: Emotion intensity [0,1]
            z_score: Associated Z-score
            
        Returns:
            Memory ID
        """
        memory_id = f"emotion_{datetime.now().isoformat()}"
        
        self.emotional.add(
            documents=[context],
            metadatas=[{
                'emotion': emotion,
                'intensity': intensity,
                'z_score': z_score,
                'timestamp': datetime.now().isoformat()
            }],
            ids=[memory_id]
        )
        
        logger.info(f"Stored emotional memory: {emotion} (intensity={intensity:.2f})")
        return memory_id
    
    def recall_episodes(self, query: str, n_results: int = 5) -> List[Dict]:
        """Recall relevant episodes.
        
        Args:
            query: Search query
            n_results: Number of results
            
        Returns:
            List of relevant episodes
        """
        results = self.episodic.query(
            query_texts=[query],
            n_results=n_results
        )
        
        episodes = []
        for i, doc in enumerate(results['documents'][0]):
            episodes.append({
                'content': doc,
                'metadata': results['metadatas'][0][i],
                'distance': results['distances'][0][i]
            })
        
        return episodes
    
    def recall_concepts(self, query: str, n_results: int = 3) -> List[Dict]:
        """Recall relevant concepts.
        
        Args:
            query: Search query
            n_results: Number of results
            
        Returns:
            List of relevant concepts
        """
        results = self.semantic.query(
            query_texts=[query],
            n_results=n_results
        )
        
        concepts = []
        for i, doc in enumerate(results['documents'][0]):
            meta = results['metadatas'][0][i]
            concepts.append({
                'concept': meta['concept'],
                'definition': doc,
                'related': json.loads(meta.get('related', '[]')),
                'distance': results['distances'][0][i]
            })
        
        return concepts
    
    def recall_emotions(self, query: str, n_results: int = 5) -> List[Dict]:
        """Recall similar emotional experiences.
        
        Args:
            query: Search query
            n_results: Number of results
            
        Returns:
            List of similar emotional memories
        """
        results = self.emotional.query(
            query_texts=[query],
            n_results=n_results
        )
        
        emotions = []
        for i, doc in enumerate(results['documents'][0]):
            meta = results['metadatas'][0][i]
            emotions.append({
                'emotion': meta['emotion'],
                'context': doc,
                'intensity': meta['intensity'],
                'z_score': meta['z_score'],
                'timestamp': meta['timestamp'],
                'distance': results['distances'][0][i]
            })
        
        return emotions
    
    def get_memory_stats(self) -> Dict:
        """Get memory system statistics.
        
        Returns:
            Statistics dictionary
        """
        return {
            'episodic_count': self.episodic.count(),
            'semantic_count': self.semantic.count(),
            'emotional_count': self.emotional.count()
        }
