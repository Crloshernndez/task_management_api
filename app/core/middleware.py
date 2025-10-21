"""
Security and utility middleware for the FastAPI application.
"""

import time
import uuid
import logging
from typing import Callable

from fastapi import Request, Response
from fastapi.middleware.cors import CORSMiddleware
from fastapi.middleware.trustedhost import TrustedHostMiddleware
from starlette.middleware.base import BaseHTTPMiddleware

from app.core.exceptions import RateLimitException
from app.core.config import get_settings

settings = get_settings()
logger = logging.getLogger(__name__)


class RateLimitMiddleware(BaseHTTPMiddleware):
    """Basic rate limiting middleware (in-memory)."""

    def __init__(self, app, calls: int = 100, period: int = 60):
        super().__init__(app)
        self.calls = calls
        self.period = period
        self.clients = {}  # In production, use Redis or similar

    async def dispatch(
        self, request: Request, call_next: Callable
    ) -> Response:
        # Skip rate limiting for health checks
        if request.url.path in ["/health", "/docs"]:
            return await call_next(request)

        # Get client IP
        client_ip = request.client.host
        current_time = time.time()

        # Clean old entries
        self._cleanup_old_entries(current_time)

        # Check rate limit
        if client_ip in self.clients:
            requests = self.clients[client_ip]
            recent_requests = [
                req_time
                for req_time in requests
                if current_time - req_time < self.period
            ]

            if len(recent_requests) >= self.calls:
                from fastapi.responses import JSONResponse

                logger.warning(
                    "Rate limit exceeded",
                    client_ip=client_ip,
                    requests_count=len(recent_requests),
                    limit=self.calls,
                )
                raise RateLimitException(
                    f"Rate limit exceeded. Maximum {self.calls} requests per {self.period} seconds."
                )

            self.clients[client_ip] = recent_requests + [current_time]
        else:
            self.clients[client_ip] = [current_time]

        return await call_next(request)

    def _cleanup_old_entries(self, current_time: float):
        """Remove old entries to prevent memory leak."""
        for client_ip in list(self.clients.keys()):
            self.clients[client_ip] = [
                req_time
                for req_time in self.clients[client_ip]
                if current_time - req_time < self.period
            ]
            if not self.clients[client_ip]:
                del self.clients[client_ip]


def setup_middleware(app):
    """
    Configure all middleware for the application.
    Order matters - middleware is executed top to bottom for requests
    and bottom to top for responses.
    """

    if settings.BACKEND_CORS_ORIGINS:
        app.add_middleware(
            CORSMiddleware,
            allow_origins=settings.BACKEND_CORS_ORIGINS,
            allow_credentials=True,
            allow_methods=["GET", "POST", "PUT", "DELETE", "PATCH", "OPTIONS"],
            allow_headers=["*"],
            expose_headers=["X-Request-ID", "X-Process-Time"],
        )

    if settings.RATE_LIMIT_ENABLED:
        app.add_middleware(
            RateLimitMiddleware,
            calls=settings.RATE_LIMIT_CALLS,
            period=settings.RATE_LIMIT_PERIOD,
        )
