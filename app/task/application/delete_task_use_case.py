"""
Delete Task Use Case
Handles deleting a specific task.
"""

import logging

from app.common.value_objects import EntityId
from app.task.domain.ports import TaskRepositoryPort

logger = logging.getLogger(__name__)


class DeleteTaskUseCase:
    """Use case for deleting a specific task."""

    def __init__(
        self,
        task_repository: TaskRepositoryPort
    ):
        self.task_repository = task_repository

    async def execute(self, task_id: str) -> bool:
        """
        Delete a task by ID.

        Args:
            task_id: The task ID

        Returns:
            bool: True if deleted successfully, False otherwise
        """
        logger.info(f"Deleting task with id: {task_id}")

        task_id_vo = EntityId(value=task_id)
        task_deleted = await self.task_repository.delete_task(task_id_vo)

        if task_deleted:
            logger.info(f"Task deleted: {task_id}")
        else:
            logger.warning(f"Task not found: {task_id}")

        return task_deleted
