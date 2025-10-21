"""
Get Task Use Case
Handles retrieving a specific task.
"""

import logging
from typing import Optional

from app.common.value_objects import EntityId
from app.task.domain.entities import Task
from app.task.domain.ports import TaskRepositoryPort

logger = logging.getLogger(__name__)


class GetTaskUseCase:
    """Use case for retrieving a specific task."""

    def __init__(
        self,
        task_repository: TaskRepositoryPort
    ):
        self.task_repository = task_repository

    async def execute(self, task_id: str) -> Optional[Task]:
        logger.info(f"Retrieving task with id: {task_id}")

        task_id_vo = EntityId(value=task_id)
        task = await self.task_repository.get_task_by_id(task_id_vo)

        if task:
            logger.info(f"Task found: {task_id}")
        else:
            logger.warning(f"Task not found: {task_id}")

        return task
