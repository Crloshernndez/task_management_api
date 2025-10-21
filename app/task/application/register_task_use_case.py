"""
Create Task Use Case
Handles task creation logic.
"""

import logging
from typing import Dict, Any

from app.task.domain.entities import Task
from app.task.domain.ports import TaskRepositoryPort
from app.task.domain.value_objects import Title, Description, State, TaskStatus

logger = logging.getLogger(__name__)


class RegisterTaskUseCase:
    """Use case for creating a new task."""

    def __init__(
        self,
        task_repository: TaskRepositoryPort
    ):
        self.task_repository = task_repository

    async def execute(self, data: Dict[str, Any]) -> Task:
        logger.info(f"Creating new task with title: {data.get('title')}")

        title = Title(value=data["title"])
        description = Description(value=data["description"])
        state = State(value=TaskStatus.PENDING.value)

        task = Task(
            title=title,
            description=description,
            state=state
        )

        created_task = await self.task_repository.create_task(task)

        logger.info(f"Task created successfully with id: {created_task.id}")

        return created_task
