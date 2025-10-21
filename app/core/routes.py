"""
Application Routes Configuration
Centralizes all route registration for the FastAPI application.
"""

import logging
from fastapi import FastAPI, Request, status

from app.core.config import get_settings

logger = logging.getLogger(__name__)
settings = get_settings()


def setup_routes(app: FastAPI) -> None:
    """
    Configure application routes.

    Registers all API routers and endpoints in a centralized location.
    Routes are organized by:
    - System endpoints (health, root, etc.)
    - Module routers (auth, users, etc.)
    - Development-only routes
    """

    _register_system_endpoints(app)

    # Register module routers
    _register_auth_routes(app)
    _register_task_routes(app)

    logger.info("Routes registered successfully")


def _register_system_endpoints(app: FastAPI) -> None:
    """Register system-level endpoints (health, root, etc.)."""

    @app.get("/health", status_code=status.HTTP_200_OK)
    async def health_check():
        """
        Health check endpoint.

        Returns the current status of the application and its dependencies.
        """
        return {
            "status": "healthy",
            "version": settings.VERSION,
            "environment": settings.ENVIRONMENT,
            "services": {
                "database": "connected",
            },
        }

    @app.get("/", status_code=status.HTTP_200_OK)
    async def root():
        """
        Root endpoint with API information.

        Provides basic information about the API and available endpoints.
        """
        return {
            "message": f"Welcome to {settings.PROJECT_NAME}",
            "version": settings.VERSION,
            "docs_url": "/docs",
            "health_url": "/health",
        }


def _register_auth_routes(app: FastAPI) -> None:
    """Register authentication and authorization routes."""

    # Authentication routes
    from app.auth.infrastructure.presentation.routes.auth_routes import (
        router as auth_router,
    )

    app.include_router(
        auth_router,
        prefix=settings.API_V1_PREFIX,
        tags=["Authentication"],
    )


def _register_task_routes(app: FastAPI) -> None:
    """Register tasks routes."""

    # Authentication routes
    from app.task.infrastructure.presentation.routes.task_routes import (
        router as task_router,
    )

    app.include_router(
        task_router,
        prefix=settings.API_V1_PREFIX,
        tags=["Task"],
    )
