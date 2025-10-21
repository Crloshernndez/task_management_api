"""
Get All Tasks Use Case
Handles retrieving all tasks.
"""

import logging
from typing import List

from app.task.domain.entities import Task
from app.task.domain.ports import TaskRepositoryPort

logger = logging.getLogger(__name__)


class GetAllTasksUseCase:
    """Use case for retrieving all tasks."""

    def __init__(
        self,
        task_repository: TaskRepositoryPort
    ):
        self.task_repository = task_repository

    async def execute(self) -> List[Task]:
        """
        Get all tasks.

        Returns:
            List[Task]: List of all task entities
        """
        logger.info("Retrieving all tasks")

        tasks = await self.task_repository.get_all_tasks()

        logger.info(f"Retrieved {len(tasks)} tasks")

        return tasks
