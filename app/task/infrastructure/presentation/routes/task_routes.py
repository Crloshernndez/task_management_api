from typing import Annotated


from fastapi import APIRouter, Depends, status
from app.task.infrastructure.presentation.dtos import (
    RegisterTaskResponse,
    RegisterTaskRequest,
    GetAllTasksResponse,
    GetTaskResponse
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


@router.get(
    "/",
    response_model=GetAllTasksResponse,
    status_code=status.HTTP_200_OK,
    summary="Get all tasks",
    description="Retrieve all tasks",
    responses={
        200: {"description": "Tasks retrieved successfully"},
    },
)
async def get_all(
    controller: Annotated[TaskController, Depends(get_task_controller)],
) -> GetAllTasksResponse:
    """
    Get all tasks.
    """
    return await controller.get_all()


@router.get(
    "/{task_id}",
    response_model=GetTaskResponse,
    status_code=status.HTTP_200_OK,
    summary="Get task by id",
    description="Retrieve task by id",
    responses={
        200: {"description": "Task retrieved successfully"},
        404: {"description": "Task not found"},
    },
)
async def get_task(
    task_id: str,
    controller: Annotated[TaskController, Depends(get_task_controller)],
) -> GetTaskResponse:
    """
    Get task by id.
    """
    return await controller.get_task(task_id)
