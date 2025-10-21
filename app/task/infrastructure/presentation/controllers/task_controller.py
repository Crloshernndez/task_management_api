"""
Authentication Controller
Handles HTTP layer for authentication endpoints.
"""

from fastapi import HTTPException, status
import logging

from app.core.decorators.exception_routes_handlers import handle_api_exceptions
from app.task.application import (
    RegisterTaskUseCase,
    GetAllTasksUseCase,
    GetTaskUseCase,
    DeleteTaskUseCase,
    UpdateTaskUseCase
)
from app.task.infrastructure.presentation.dtos import (
    RegisterTaskResponse,
    RegisterTaskRequest,
    GetAllTasksResponse,
    TaskResponse,
    GetTaskResponse,
    DeleteTaskResponse,
    UpdateTaskRequest,
    UpdateTaskResponse
)

logger = logging.getLogger(__name__)


class TaskController:
    """Controller for authentication operations."""

    def __init__(
        self,
        register_task_use_case: RegisterTaskUseCase,
        get_all_tasks_use_case: GetAllTasksUseCase,
        get_task_use_case: GetTaskUseCase,
        delete_task_use_case: DeleteTaskUseCase,
        update_task_use_case: UpdateTaskUseCase
    ):
        self.register_task_use_case = register_task_use_case
        self.get_all_tasks_use_case = get_all_tasks_use_case
        self.get_task_use_case = get_task_use_case
        self.delete_task_use_case = delete_task_use_case
        self.update_task_use_case = update_task_use_case

    @handle_api_exceptions
    async def register(
        self,
        request: RegisterTaskRequest,
    ) -> RegisterTaskResponse:
        """
        Register a new task.
        """
        logger.info("Task registration request")
        # Execute use case
        task = await self.register_task_use_case.execute({
            "title": request.title,
            "description": request.description,
        })

        # Convert to response
        return RegisterTaskResponse(
            message="Task registered successfully",
            task=self._task_to_response(task),
        )

    @handle_api_exceptions
    async def get_all(
        self
    ) -> GetAllTasksResponse:
        """
        Get all task.
        """
        logger.info("Tasks retrieved request")
        # Execute use case
        tasks = await self.get_all_tasks_use_case.execute()

        # Convert to response
        return GetAllTasksResponse(
            message="Tasks retrieved successfully",
            tasks=[self._task_to_response(task) for task in tasks],
        )

    @handle_api_exceptions
    async def get_task(
        self,
        task_id: str
    ) -> GetTaskResponse:
        """
        Get task by ID.
        """
        logger.info(f"Task retrieve request for id: {task_id}")

        # Execute use case
        task = await self.get_task_use_case.execute(task_id)

        if not task:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail=f"Task with id {task_id} not found"
            )

        # Convert to response
        return GetTaskResponse(
            message="Task retrieved successfully",
            task=self._task_to_response(task),
        )

    @handle_api_exceptions
    async def update_task(
        self,
        task_id: str,
        request: UpdateTaskRequest,
    ) -> UpdateTaskResponse:
        """
        Update task by ID.
        """
        logger.info(f"Task update by id: {task_id}")

        # Prepare data dict from request
        data = {}
        if request.title is not None:
            data["title"] = request.title
        if request.description is not None:
            data["description"] = request.description
        if request.state is not None:
            data["state"] = request.state

        # Execute use case
        task_updated = await self.update_task_use_case.execute(task_id, data)

        if not task_updated:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail=f"Task with id {task_id} not found"
            )

        # Convert to response
        return UpdateTaskResponse(
            message="Task updated successfully.",
            task=self._task_to_response(task_updated),
        )

    @handle_api_exceptions
    async def delete_task(
        self,
        task_id: str
    ) -> DeleteTaskResponse:
        """
        Delete task by ID.
        """
        logger.info(f"Task deleting by id: {task_id}")

        # Execute use case
        task_deleted = await self.delete_task_use_case.execute(task_id)

        if not task_deleted:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail=f"Task with id {task_id} not found"
            )

        # Convert to response
        return DeleteTaskResponse(
            message="Task deleted successfully.",
            task_id=task_id,
        )

    @staticmethod
    def _task_to_response(task) -> TaskResponse:
        return TaskResponse(
            id=task.id.value,
            title=task.title.value,
            description=task.description.value,
            state=task.state.value,
        )
