"""
Authentication Controller
Handles HTTP layer for authentication endpoints.
"""

from fastapi import Request
import logging

from app.core.decorators.exception_routes_handlers import handle_api_exceptions
from app.auth.application import (
    RegisterUserUseCase,
)
from app.auth.domain.entities.user import User
from app.auth.infrastructure.presentation.dtos import (
    RegisterRequest,
    RegisterResponse,
    UserResponse
)

logger = logging.getLogger(__name__)


class AuthController:
    """Controller for authentication operations."""

    def __init__(
        self,
        register_use_case: RegisterUserUseCase,
    ):
        self.register_use_case = register_use_case

    @handle_api_exceptions
    async def register(
        self,
        request: RegisterRequest,
    ) -> RegisterResponse:
        """
        Register a new user.
        """
        logger.info(f"Registration request for: {request.email}")

        # Execute use case
        user = await self.register_use_case.execute({
            "email": request.email,
            "password": request.password,
            "username": request.username,
        })

        # Convert to response
        return RegisterResponse(
            message="User registered successfully. Please verify your email.",
            user=self._user_to_response(user),
        )

    @staticmethod
    def _user_to_response(user: User) -> UserResponse:
        """Convert User entity to UserResponse DTO."""
        return UserResponse(
            id=user.id.value,
            email=user.email.value,
            username=user.username.value,
        )
