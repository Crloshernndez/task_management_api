from typing import Annotated


from fastapi import APIRouter, Depends, status
from app.task.infrastructure.presentation.dtos import (
    RegisterTaskResponse,
    RegisterTaskRequest,
    GetAllTasksResponse,
    GetTaskResponse,
    DeleteTaskResponse,
    UpdateTaskResponse,
    UpdateTaskRequest
)
from app.task.infrastructure.presentation.controllers import (
    TaskController
)
from app.task.infrastructure.dependencies import get_task_controller
from app.auth.infrastructure.dependencies import get_current_user_id
from app.common.value_objects import EntityId

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
        401: {"description": "Unauthorized"},
    },
)
async def register(
    request: RegisterTaskRequest,
    controller: Annotated[TaskController, Depends(get_task_controller)],
    current_user_id: Annotated[EntityId, Depends(get_current_user_id)],
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
        401: {"description": "Unauthorized"},
    },
)
async def get_all(
    controller: Annotated[TaskController, Depends(get_task_controller)],
    current_user_id: Annotated[EntityId, Depends(get_current_user_id)],
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
        401: {"description": "Unauthorized"},
        404: {"description": "Task not found"},
    },
)
async def get_task(
    task_id: str,
    controller: Annotated[TaskController, Depends(get_task_controller)],
    current_user_id: Annotated[EntityId, Depends(get_current_user_id)],
) -> GetTaskResponse:
    """
    Get task by id.
    """
    return await controller.get_task(task_id)


@router.put(
    "/{task_id}",
    response_model=UpdateTaskResponse,
    status_code=status.HTTP_200_OK,
    summary="Update task by id",
    description="Update task by id",
    responses={
        200: {"description": "Task Update successfully"},
        401: {"description": "Unauthorized"},
        404: {"description": "Task not found"},
    },
)
async def update_task(
    task_id: str,
    request: UpdateTaskRequest,
    controller: Annotated[TaskController, Depends(get_task_controller)],
    current_user_id: Annotated[EntityId, Depends(get_current_user_id)],
) -> UpdateTaskResponse:
    """
    Update task by id.
    """
    return await controller.update_task(task_id, request)


@router.delete(
    "/{task_id}",
    response_model=DeleteTaskResponse,
    status_code=status.HTTP_200_OK,
    summary="Delete task by id",
    description="Delete task by id",
    responses={
        200: {"description": "Task deleted successfully"},
        401: {"description": "Unauthorized"},
        404: {"description": "Task not found"},
    },
)
async def delete_task(
    task_id: str,
    controller: Annotated[TaskController, Depends(get_task_controller)],
    current_user_id: Annotated[EntityId, Depends(get_current_user_id)],
) -> DeleteTaskResponse:
    """
    Delete task by id.
    """
    return await controller.delete_task(task_id)
