from pydantic_settings import BaseSettings
from typing import Optional

class Settings(BaseSettings):
    # API Settings
    PROJECT_NAME: str = "Jarvis AI"
    API_V1_PREFIX: str = "/api/v1"
    DEBUG: bool = True
    
    # Security
    SECRET_KEY: str
    ACCESS_TOKEN_EXPIRE_MINUTES: int = 30
    
    # LLM Settings
    OPENAI_API_KEY: str
    MODEL_NAME: str = "gpt-3.5-turbo"
    TEMPERATURE: float = 0.7
    
    # Database
    DATABASE_URL: str
    
    # Vector Database
    VECTOR_DB_PATH: str = "./data/vectordb"
    
    class Config:
        env_file = ".env"
        case_sensitive = True

settings = Settings() 