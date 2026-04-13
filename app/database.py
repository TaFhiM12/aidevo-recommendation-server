from pymongo import MongoClient
from typing import Optional
from app.config import settings

class MongoDBConnection:
    """MongoDB connection manager."""
    
    _client: Optional[MongoClient] = None
    
    @classmethod
    def connect(cls):
        """Establish MongoDB connection."""
        if cls._client is None:
            cls._client = MongoClient(settings.MONGODB_URI)
        return cls._client
    
    @classmethod
    def disconnect(cls):
        """Close MongoDB connection."""
        if cls._client is not None:
            cls._client.close()
            cls._client = None
    
    @classmethod
    def get_database(cls):
        """Get database instance."""
        if cls._client is None:
            cls.connect()
        return cls._client[settings.DB_NAME]
    
    @classmethod
    def get_collection(cls, collection_name: str):
        """Get collection from database."""
        db = cls.get_database()
        return db[collection_name]

db = MongoDBConnection()
