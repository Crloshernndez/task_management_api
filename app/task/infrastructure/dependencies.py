from typing import Annotated
from fastapi import Depends
from sqlalchemy.ext.asyncio import AsyncSession

from app.core.database import get_async_session
from app.task.application import RegisterTaskUseCase
from app.task.infrastructure.repositories import (
    TaskRepository
)
from app.task.infrastructure.presentation.controllers import (
    TaskController
)
from app.auth.infrastructure.adapters import JWTTokenService

# ============================================================================
# Service Dependencies
# ============================================================================


async def get_task_repository(
    session: Annotated[AsyncSession, Depends(get_async_session)],
) -> TaskRepository:
    """Get TaskRepository instance."""
    return TaskRepository(session)


# ============================================================================
# Service Dependencies
# ============================================================================


async def get_register_task_use_case(
    user_repository: Annotated[
        TaskRepository, Depends(get_task_repository)
    ]
) -> RegisterTaskUseCase:
    return RegisterTaskUseCase(user_repository)


# ============================================================================
# Controller Dependencies
# ============================================================================


async def get_task_controller(
    register_task_use_case: Annotated[
        RegisterTaskUseCase, Depends(get_register_task_use_case)
    ],
) -> TaskController:
    """
    Create auth controller with all dependencies.
    """
    return TaskController(
        register_task_use_case=register_task_use_case,
    )
