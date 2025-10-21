"""
Database configuration and session management.
SQLAlchemy setup for PostgreSQL with async support.
"""

import logging
from typing import AsyncGenerator

from sqlalchemy.ext.asyncio import (
    AsyncSession,
    async_sessionmaker,
    create_async_engine,
)
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.pool import NullPool

from app.core.config import get_settings

logger = logging.getLogger(__name__)
settings = get_settings()


def prepare_database_url(url: str) -> str:
    """Prepare database URL for asyncpg (Neon compatible)."""
    # Remove query parameters
    if "?" in url:
        base_url = url.split("?")[0]
    else:
        base_url = url

    # Convert to asyncpg
    if base_url.startswith("postgres://"):
        base_url = base_url.replace("postgres://", "postgresql+asyncpg://", 1)
    elif base_url.startswith("postgresql://"):
        base_url = base_url.replace(
            "postgresql://", "postgresql+asyncpg://", 1
        )

    return base_url


database_url = prepare_database_url(settings.DATABASE_URL)

# Development/Testing: Use NullPool (simpler, creates new connection each time)
engine = create_async_engine(
    database_url,
    echo=settings.DATABASE_ECHO,
    poolclass=NullPool,
    pool_pre_ping=True,
)
logger.info("Database engine created with NullPool (development mode)")

# Create session factory
async_session_factory = async_sessionmaker(
    engine,
    class_=AsyncSession,
    expire_on_commit=False,
    autocommit=False,
    autoflush=False,
)

# Create declarative base
Base = declarative_base()


async def get_async_session() -> AsyncGenerator[AsyncSession, None]:
    """
    Async session dependency for FastAPI.

    Yields:
        AsyncSession: Database session
    """
    async with async_session_factory() as session:
        try:
            logger.debug("Database session created")
            yield session
        except Exception as e:
            logger.error(f"Database session error: {str(e)}")
            await session.rollback()
            raise
        finally:
            logger.debug("Database session closed")
            await session.close()


async def init_database() -> None:
    """
    Initialize database - create all tables.
    Use only in development or for testing.
    In production, use Alembic migrations.
    """
    try:
        logger.info("Initializing database tables")
        async with engine.begin() as conn:
            await conn.run_sync(Base.metadata.create_all)
        logger.info("Database tables created successfully")
    except Exception as e:
        logger.error("Failed to initialize database", error=str(e))
        raise


async def drop_database() -> None:
    """
    Drop all database tables.
    Use only in development or testing!
    """
    try:
        logger.warning("Dropping all database tables")
        async with engine.begin() as conn:
            await conn.run_sync(Base.metadata.drop_all)
        logger.info("All database tables dropped")
    except Exception as e:
        logger.error("Failed to drop database tables", error=str(e))
        raise


async def check_database_connection() -> bool:
    """
    Check if database connection is working.

    Returns:
        bool: True if connection is successful
    """
    try:
        async with engine.begin() as conn:
            await conn.exec_driver_sql("SELECT 1")
        logger.info("Database connection successful")
        return True
    except Exception as e:
        logger.error("Database connection failed", error=str(e))
        return False


async def close_database_connection() -> None:
    """Close database connection pool."""
    try:
        await engine.dispose()
        logger.info("Database connection pool closed")
    except Exception as e:
        logger.error("Error closing database connection", error=str(e))
