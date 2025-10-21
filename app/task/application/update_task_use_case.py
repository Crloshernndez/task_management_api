"""
Update Task Use Case
Handles task update logic.
"""

import logging
from typing import Dict, Any, Optional

from app.task.domain.entities import Task
from app.common.value_objects import EntityId
from app.task.domain.ports import TaskRepositoryPort
from app.task.domain.value_objects import Title, Description, State

logger = logging.getLogger(__name__)


class UpdateTaskUseCase:
    """Use case for updating a task."""

    def __init__(
        self,
        task_repository: TaskRepositoryPort
    ):
        self.task_repository = task_repository

    async def execute(
        self,
        task_id: str,
        data: Dict[str, Any]
    ) -> Optional[Task]:
        """
        Update a task.

        Args:
            task_id: The task ID to update
            data: Dictionary with updated task data (title, description, state)

        Returns:
            Task: The updated task entity if found, None otherwise
        """
        logger.info(f"Updating task with id: {task_id}")

        task_id_vo = EntityId(value=task_id)

        existing_task = await self.task_repository.get_task_by_id(task_id_vo)

        if not existing_task:
            logger.warning(f"Task not found for update: {task_id}")
            return None

        # Create value objects with updated data or keep existing
        title = Title(value=data.get("title", existing_task.title.value))
        description = Description(value=data.get("description", existing_task.description.value))
        state = State(value=data.get("state", existing_task.state.value))

        # Create updated task entity
        updated_task = Task(
            title=title,
            description=description,
            state=state,
            id=existing_task.id,
            created_at=existing_task.created_at,
            updated_at=existing_task.updated_at
        )

        # Save updated task
        result = await self.task_repository.update_task(updated_task)

        logger.info(f"Task updated successfully: {task_id}")

        return result
