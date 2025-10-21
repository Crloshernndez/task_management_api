"""
Application configuration settings.
"""

from functools import lru_cache
from typing import List, Optional

from dotenv import load_dotenv
from pydantic import ConfigDict, Field
from pydantic_settings import BaseSettings

load_dotenv()


class Settings(BaseSettings):
    """Application settings with environment variable support."""

    # =================================================================
    # APPLICATION SETTINGS
    # =================================================================
    PROJECT_NAME: str = Field(default="Task Management API")
    VERSION: str = Field(default="1.0.0")
    ENVIRONMENT: str = Field(
        default="development"
    )
    DEBUG: bool = Field(default=True)

    # =================================================================
    # SERVER SETTINGS
    # =================================================================
    HOST: str = Field(default="0.0.0.0")
    PORT: int = Field(default=8000)
    ALLOWED_HOSTS: List[str] = Field(
        default=["localhost", "127.0.0.1", "0.0.0.0"]
    )

    # =================================================================
    # API SETTINGS
    # =================================================================
    API_V1_PREFIX: str = Field(default="/api/v1")

    # =================================================================
    # SECURITY SETTINGS
    # =================================================================
    SECRET_KEY: str = Field(..., min_length=32)

    # JWT Configuration
    JWT_SECRET_KEY: str = Field(..., min_length=32)
    JWT_ALGORITHM: str = Field(default="HS256")
    TOKEN_TYPE: str = Field(default="Bearer")
    ACCESS_TOKEN_EXPIRE_MINUTES: int = Field(default=15)

    # =================================================================
    # CORS SETTINGS
    # =================================================================
    BACKEND_CORS_ORIGINS: List[str] = Field(
        default=[
            "http://localhost:3000",
            "http://localhost:8080",
            "http://localhost:3001",
        ]
    )

    # =================================================================
    # DATABASE SETTINGS
    # =================================================================
    DATABASE_URL: str = Field(...)
    DATABASE_ECHO: bool = Field(default=False)
    DATABASE_AUTO_INIT: bool = Field(default=False)

    # Database Connection Pool (Production/Staging)
    DB_POOL_SIZE: int = Field(default=5)
    DB_MAX_OVERFLOW: int = Field(default=10)
    DB_POOL_TIMEOUT: int = Field(default=30)
    DB_POOL_RECYCLE: int = Field(default=300)

    # =================================================================
    # POSTGRESQL DOCKER SETTINGS
    # =================================================================
    POSTGRES_DB: str = Field(...)
    POSTGRES_USER: str = Field(...)
    POSTGRES_PASSWORD: str = Field(...)
    POSTGRES_PORT: str = Field(default="5432")
    POSTGRES_CONTAINER_NAME: str = Field(default="espora_db")

    # =================================================================
    # API DOCKER SETTINGS
    # =================================================================
    API_PORT: str = Field(default="8000")
    API_CONTAINER_NAME: str = Field(default="espora_app")

    # =================================================================
    # RATE LIMITING SETTINGS
    # =================================================================
    RATE_LIMIT_ENABLED: bool = Field(default=True)
    RATE_LIMIT_CALLS: int = Field(default=100)
    RATE_LIMIT_PERIOD: int = Field(default=60)  # seconds

    # =================================================================
    # PYDANTIC CONFIGURATION
    # =================================================================
    model_config = ConfigDict(
        env_file=".env",
        env_file_encoding="utf-8",
        case_sensitive=True,
        extra="forbid",
    )


@lru_cache()
def get_settings() -> Settings:
    """
    Get settings instance.
    Cached for performance.
    """
    return Settings()  # type: ignore[call-arg]
