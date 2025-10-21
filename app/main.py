import logging
from contextlib import asynccontextmanager
from typing import AsyncGenerator

from fastapi import FastAPI

from app.core.config import get_settings
from app.core.database import (
    check_database_connection,
    close_database_connection,
    init_database,
)
# Import models to register them with SQLAlchemy
from app.auth.infrastructure.repositories.models import UserModel  # noqa: F401
from app.core.middleware import (
    setup_middleware,
)
from app.core.routes import setup_routes

logger = logging.getLogger(__name__)

settings = get_settings()


@asynccontextmanager
async def lifespan(app: FastAPI) -> AsyncGenerator[None, None]:
    """
    Application lifespan context manager.
    Handles startup and shutdown events.
    """
    # Startup
    logger.info(
        "Starting application",
        version=settings.VERSION,
        environment=settings.ENVIRONMENT,
    )

    # Check database connection
    db_connected = await check_database_connection()
    if not db_connected:
        logger.error("Failed to connect to database")
        raise Exception("Database connection failed")

    # Initialize database tables
    await init_database()

    yield

    # Shutdown
    logger.info("Shutting down application")
    await close_database_connection()
    logger.info("Application shutdown completed")


def create_app() -> FastAPI:
    """
    Application factory function.
    Creates and configures the FastAPI application.
    """

    app = FastAPI(
        title=settings.PROJECT_NAME,
        version=settings.VERSION,
        docs_url="/docs" if settings.DEBUG else None,
        redoc_url="/redoc" if settings.DEBUG else None,
        lifespan=lifespan,
    )

    # Middleware setup
    setup_middleware(app)

    # Routes
    setup_routes(app)

    return app


# Create app instance
app = create_app()
