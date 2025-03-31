import chromadb
from chromadb.config import Settings
from src.config.settings import settings
from typing import List, Dict
from datetime import datetime


class MemoryService:
    def __init__(self):
        self.client = chromadb.PersistentClient(path=settings.VECTOR_DB_PATH)
        
        # Create collection for user memory
        self.memory_collection = self.client.get_or_create_collection(
            name="user_memories",
            metadata={"hnsw:space": "cosine"}
        )

    async def store_memory(self, user_id: str, memory: str, metadata: Dict = None):
        self.memory_collection.add(
            documents=[memory],
            metadatas=[metadata or {}],
            ids=[f"{user_id}-{datetime.utcnow().timestamp()}"]
        )

    async def retrieve_relevant_memories(self, user_id: str, query: str, limit: int = 5) -> List[str]:
        results = self.memory_collection.query(
            query_texts=[query],
            n_results=limit,
            where={"user_id": user_id}
        )
        return results["documents"][0] 