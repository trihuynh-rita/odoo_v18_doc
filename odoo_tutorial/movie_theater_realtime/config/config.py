"""
name: config.py
description: Configuration module for the movie theater realtime app. Loads environment variables.
"""
import os
from dotenv import load_dotenv

# Load environment variables from .env file
load_dotenv()

class Config:
    """
    Application configuration class.
    
    Attributes:
        MONGO_URI (str): MongoDB Atlas connection string.
    """
    MONGO_URI = os.getenv("MONGO_URI", "")

# Create a singleton instance for global access
settings = Config()
