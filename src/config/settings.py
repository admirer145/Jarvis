from pydantic_settings import BaseSettings
from typing import Optional
from functools import lru_cache

class Settings(BaseSettings):
    # API Settings
    PROJECT_NAME: str = "Jarvis AI"
    API_V1_PREFIX: str = "/api/v1"
    DEBUG: bool = True
    
    # Security
    SECRET_KEY: str
    ACCESS_TOKEN_EXPIRE_MINUTES: int = 30
    
    # LLM Settings
    HUGGINGFACE_API_KEY: str
    MODEL_NAME: str = "facebook/opt-350m"  # Changed to a completely open model
    TEMPERATURE: float = 0.7
    MAX_LENGTH: int = 2048
    
    # Database
    DATABASE_URL: str
    
    # Vector Database
    VECTOR_DB_PATH: str = "./data/vectordb"
    
    class Config:
        env_file = ".env"
        case_sensitive = True

@lru_cache()
def get_settings() -> Settings:
    return Settings()

settings = get_settings() 