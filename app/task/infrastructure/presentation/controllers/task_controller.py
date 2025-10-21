"""
Authentication Controller
Handles HTTP layer for authentication endpoints.
"""

from fastapi import Request
import logging

from app.core.decorators.exception_routes_handlers import handle_api_exceptions
from app.task.application import (
    RegisterTaskUseCase
)
from app.task.infrastructure.presentation.dtos import (
    RegisterTaskResponse,
    RegisterTaskRequest,
    TaskResponse
)

logger = logging.getLogger(__name__)


class TaskController:
    """Controller for authentication operations."""

    def __init__(
        self,
        register_task_use_case: RegisterTaskUseCase,
    ):
        self.register_task_use_case = register_task_use_case

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

    @staticmethod
    def _task_to_response(task) -> TaskResponse:
        return TaskResponse(
            id=task.id.value,
            title=task.title.value,
            description=task.description.value,
            state=task.state.value,
        )
