# app/config.py
"""
Application configuration
Loads from .env file
"""
from pydantic_settings import BaseSettings
from typing import List
import os

class Settings(BaseSettings):
    """Application settings"""
    
    # App Info
    APP_NAME: str = "GreenChain API"
    DEBUG: bool = True
    VERSION: str = "1.0.0"
    
    # API
    API_V1_PREFIX: str = "/api/v1"
    
    # Database
    DATABASE_URL: str = "sqlite:///./greenchain.db"
    
    # Security
    SECRET_KEY: str = "greenchain-secret-key-change-in-production"
    
    # CORS
    CORS_ORIGINS: List[str] = [
        "http://localhost:8501",  # Streamlit
        "http://localhost:3000",  # React (if needed)
        "http://localhost:8000",  # Self
    ]
    
    # Satellite API
    COPERNICUS_CLIENT_ID: str = ""
    COPERNICUS_CLIENT_SECRET: str = ""
    COPERNICUS_INSTANCE_ID: str = ""
    
    # Blockchain
    BLOCKCHAIN_DIFFICULTY: int = 2
    MINING_REWARD: int = 10
    
    # Demo Mode
    DEMO_MODE: bool = True
    
    class Config:
        env_file = ".env"
        case_sensitive = True

# Create settings instance
settings = Settings()
