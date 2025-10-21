from typing import Annotated
from fastapi import Depends
from sqlalchemy.ext.asyncio import AsyncSession

from app.core.database import get_async_session
from app.auth.application import RegisterUserUseCase
from app.auth.infrastructure.repositories import (
    UserRepository
)
from app.auth.infrastructure.presentation.controllers import (
    AuthController
)

# ============================================================================
# Service Dependencies
# ============================================================================


async def get_user_repository(
    session: Annotated[AsyncSession, Depends(get_async_session)],
) -> UserRepository:
    """Get UserRepository instance."""
    return UserRepository(session)


# ============================================================================
# Service Dependencies
# ============================================================================


async def get_register_user_use_case(
    user_repository: Annotated[
        UserRepository, Depends(get_user_repository)
    ]
) -> RegisterUserUseCase:
    return RegisterUserUseCase(user_repository)

# ============================================================================
# Controller Dependencies
# ============================================================================


async def get_auth_controller(
    register_use_case: Annotated[
        RegisterUserUseCase, Depends(get_register_user_use_case)
    ],
) -> AuthController:
    """
    Create auth controller with all dependencies.
    """
    return AuthController(
        register_use_case=register_use_case,
    )
