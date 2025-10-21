from typing import Annotated


from fastapi import APIRouter, Depends, status
from app.task.infrastructure.presentation.dtos import (
    RegisterTaskResponse,
    RegisterTaskRequest,
)
from app.task.infrastructure.presentation.controllers import (
    TaskController
)
from app.task.infrastructure.dependencies import get_task_controller

router = APIRouter(prefix="/tasks", tags=["Tasks"])


@router.post(
    "/",
    response_model=RegisterTaskResponse,
    status_code=status.HTTP_201_CREATED,
    summary="Register a new task",
    description="Register a new task",
    responses={
        201: {"description": "Task registered successfully"},
        400: {"description": "Invalid input data"},
    },
)
async def register(
    request: RegisterTaskRequest,
    controller: Annotated[TaskController, Depends(get_task_controller)],
) -> RegisterTaskResponse:
    """
    Register a new task.
    """
    return await controller.register(request)
