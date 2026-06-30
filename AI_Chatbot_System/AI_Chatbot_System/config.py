"""
config.py — [MVP]
Centralized application configuration, loaded from environment variables.

Used by: app.py, database/db_operations.py, models/*, security/*
See: .env.example for the full list of expected variables.
"""

from functools import lru_cache
from pydantic_settings import BaseSettings, SettingsConfigDict


class Settings(BaseSettings):
    # --- App ---
    APP_NAME: str = "AI Chatbot System"
    APP_ENV: str = "development"          # development | staging | production
    DEBUG: bool = True
    API_V1_PREFIX: str = "/api/v1"

    # --- Server ---
    HOST: str = "0.0.0.0"
    PORT: int = 8000

    # --- Security ---
    SECRET_KEY: str = "change-me-in-env"
    ALGORITHM: str = "HS256"
    ACCESS_TOKEN_EXPIRE_MINUTES: int = 60
    CORS_ORIGINS: list[str] = ["*"]       # tighten in security/cors_policy.py for prod

    # --- Database (Postgres) ---
    DATABASE_URL: str = "postgresql://postgres:postgres@localhost:5432/chatbot_db"

    # --- Cache / Broker ---
    REDIS_URL: str = "redis://localhost:6379/0"

    # --- Vector store ---
    QDRANT_URL: str = "http://localhost:6333"
    CHROMA_PERSIST_DIR: str = "./chroma_data"

    # --- LLM Providers ---
    OPENAI_API_KEY: str | None = None
    ANTHROPIC_API_KEY: str | None = None
    HF_API_TOKEN: str | None = None
    DEFAULT_MODEL_PROVIDER: str = "openai"  # openai | anthropic | hf

    model_config = SettingsConfigDict(
        env_file=".env",
        env_file_encoding="utf-8",
        extra="ignore",
    )


@lru_cache
def get_settings() -> Settings:
    """Cached settings instance — import this, not Settings() directly."""
    return Settings()
