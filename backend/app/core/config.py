from pydantic_settings import BaseSettings
from functools import lru_cache
import os
from pathlib import Path

# Create data directory if it doesn't exist
BASE_DIR = Path(__file__).resolve().parent.parent.parent
DATA_DIR = BASE_DIR / "data"
DATA_DIR.mkdir(exist_ok=True)

class Settings(BaseSettings):
    DATABASE_URL: str = f"sqlite:///{DATA_DIR}/documents.db"
    API_V1_STR: str = "/api"
    PROJECT_NAME: str = "Document Manager"
    BACKEND_CORS_ORIGINS: list[str] = ["http://localhost:5173", "http://localhost:3000"]

    class Config:
        case_sensitive = True

@lru_cache()
def get_settings():
    return Settings()

settings = get_settings()