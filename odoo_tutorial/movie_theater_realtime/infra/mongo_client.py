"""
name: mongo_client.py
description: Infrastructure module for MongoDB Atlas connection and client initialization.
"""
from pymongo import MongoClient
from config.config import settings

def get_mongo_client() -> MongoClient:
    """
    Initializes and returns a MongoDB client connected to Atlas.
    
    Returns:
        MongoClient: A MongoDB connection client instance.
    """
    if not settings.MONGO_URI:
        raise ValueError("MONGO_URI not found in configuration environment.")
    
    try:
        # Create MongoDB Atlas client
        client = MongoClient(settings.MONGO_URI)
        # Verify connection (optional but recommended for robustness)
        client.admin.command('ping')
        return client
    except Exception as e:
        print(f"Error connecting to MongoDB Atlas: {e}")
        raise

# Singleton instance of the client for application reuse
mongo_client = get_mongo_client()
