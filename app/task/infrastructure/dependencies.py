from typing import Annotated
from fastapi import Depends
from sqlalchemy.ext.asyncio import AsyncSession

from app.core.database import get_async_session
from app.task.application import (
    RegisterTaskUseCase,
    GetAllTasksUseCase
)
from app.task.infrastructure.repositories import (
    TaskRepository
)
from app.task.infrastructure.presentation.controllers import (
    TaskController
)

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
    task_repository: Annotated[
        TaskRepository, Depends(get_task_repository)
    ]
) -> RegisterTaskUseCase:
    return RegisterTaskUseCase(task_repository)


async def get_get_all_tasks_use_case(
    task_repository: Annotated[
        TaskRepository, Depends(get_task_repository)
    ]
) -> GetAllTasksUseCase:
    return GetAllTasksUseCase(task_repository)


# ============================================================================
# Controller Dependencies
# ============================================================================


async def get_task_controller(
    register_task_use_case: Annotated[
        RegisterTaskUseCase, Depends(get_register_task_use_case)
    ],
    get_all_tasks_use_case: Annotated[
        GetAllTasksUseCase, Depends(get_get_all_tasks_use_case)
    ]
) -> TaskController:
    """
    Create auth controller with all dependencies.
    """
    return TaskController(
        register_task_use_case=register_task_use_case,
        get_all_tasks_use_case=get_all_tasks_use_case
    )
