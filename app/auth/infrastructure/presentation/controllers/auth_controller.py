"""
Authentication Controller
Handles HTTP layer for authentication endpoints.
"""

from fastapi import Request
import logging

from app.core.decorators.exception_routes_handlers import handle_api_exceptions
from app.auth.application import (
    RegisterUserUseCase,
    LoginUseCase
)
from app.auth.domain.entities.user import User
from app.auth.infrastructure.presentation.dtos import (
    RegisterRequest,
    RegisterResponse,
    UserResponse,
    LoginRequest,
    LoginResponse,
    TokenResponse
)

logger = logging.getLogger(__name__)


class AuthController:
    """Controller for authentication operations."""

    def __init__(
        self,
        register_use_case: RegisterUserUseCase,
        login_use_case: LoginUseCase,
    ):
        self.register_use_case = register_use_case
        self.login_use_case = login_use_case

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

    @handle_api_exceptions
    async def login(
        self,
        request: LoginRequest,
        http_request: Request,
    ) -> LoginResponse:
        logger.info(f"Login request for: {request.email}")

        # Execute use case
        login_result = await self.login_use_case.execute(
            email=request.email,
            password=request.password,
        )

        # Get user info for response (from token)
        user_id = await self.login_use_case.token_service.verify_access_token(
            str(login_result.token)
        )
        await self.login_use_case.user_repository.get_user_by_id(user_id)

        return LoginResponse(
            message="Login successful",
            token=TokenResponse(**login_result.to_dict()),
        )

    @staticmethod
    def _user_to_response(user: User) -> UserResponse:
        """Convert User entity to UserResponse DTO."""
        return UserResponse(
            id=user.id.value,
            email=user.email.value,
            username=user.username.value,
        )
