from typing import Annotated
from fastapi import Depends
from sqlalchemy.ext.asyncio import AsyncSession

from app.core.database import get_async_session
from app.task.application import (
    RegisterTaskUseCase,
    GetAllTasksUseCase,
    GetTaskUseCase,
    DeleteTaskUseCase,
    UpdateTaskUseCase,
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


async def get_get_task_use_case(
    task_repository: Annotated[
        TaskRepository, Depends(get_task_repository)
    ]
) -> GetTaskUseCase:
    return GetTaskUseCase(task_repository)


async def get_delete_task_use_case(
    task_repository: Annotated[
        TaskRepository, Depends(get_task_repository)
    ]
) -> DeleteTaskUseCase:
    return DeleteTaskUseCase(task_repository)


async def get_update_task_use_case(
    task_repository: Annotated[
        TaskRepository, Depends(get_task_repository)
    ]
) -> UpdateTaskUseCase:
    return UpdateTaskUseCase(task_repository)


# ============================================================================
# Controller Dependencies
# ============================================================================


async def get_task_controller(
    register_task_use_case: Annotated[
        RegisterTaskUseCase, Depends(get_register_task_use_case)
    ],
    get_all_tasks_use_case: Annotated[
        GetAllTasksUseCase, Depends(get_get_all_tasks_use_case)
    ],
    get_task_use_case: Annotated[
        GetTaskUseCase, Depends(get_get_task_use_case)
    ],
    delete_task_use_case: Annotated[
        DeleteTaskUseCase, Depends(get_delete_task_use_case)
    ],
    update_task_use_case: Annotated[
        UpdateTaskUseCase, Depends(get_update_task_use_case)
    ]
) -> TaskController:
    """
    Create auth controller with all dependencies.
    """
    return TaskController(
        register_task_use_case=register_task_use_case,
        get_all_tasks_use_case=get_all_tasks_use_case,
        get_task_use_case=get_task_use_case,
        delete_task_use_case=delete_task_use_case,
        update_task_use_case=update_task_use_case
    )
