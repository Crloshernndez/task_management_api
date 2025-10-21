"""
Task Repository Implementation
Concrete implementation of TaskRepository using SQLAlchemy.
"""

from typing import Optional, List
import logging

from app.core.decorators.exception_repository_handlers import exception_repository_handlers
from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession

from app.task.domain.ports import TaskRepositoryPort
from app.task.infrastructure.repositories.models import TaskModel
from app.task.domain.entities import Task as DomainTask
from app.task.domain.value_objects import Title, Description, State
from app.common.value_objects import EntityId

logger = logging.getLogger(__name__)


class TaskRepository(TaskRepositoryPort):
    """SQLAlchemy implementation of task repository."""

    def __init__(self, session: AsyncSession):
        self.session = session

    @exception_repository_handlers("create task")
    async def create_task(self, task: DomainTask) -> DomainTask:
        db_task = self._to_model(task)
        self.session.add(db_task)
        await self.session.commit()
        await self.session.refresh(db_task)

        return self._to_entity(db_task)

    @exception_repository_handlers("get task by id")
    async def get_task_by_id(self, task_id: EntityId) -> Optional[DomainTask]:
        stmt = select(TaskModel).where(TaskModel.id == task_id.value)
        result = await self.session.execute(stmt)
        task_model = result.scalar_one_or_none()

        if task_model:
            return self._to_entity(task_model)
        return None

    @exception_repository_handlers("get all tasks")
    async def get_all_tasks(self) -> List[DomainTask]:
        stmt = select(TaskModel).order_by(TaskModel.created_at.desc())
        result = await self.session.execute(stmt)
        task_models = result.scalars().all()

        return [self._to_entity(task_model) for task_model in task_models]

    @exception_repository_handlers("update task")
    async def update_task(self, task: DomainTask) -> DomainTask:
        stmt = select(TaskModel).where(TaskModel.id == task.id.value)
        result = await self.session.execute(stmt)
        task_model = result.scalar_one_or_none()

        if task_model:
            task_model.title = task.title.value
            task_model.description = task.description.value
            task_model.state = task.state.value

            await self.session.commit()
            await self.session.refresh(task_model)

            return self._to_entity(task_model)
        return None

    @exception_repository_handlers("delete task")
    async def delete_task(self, task_id: EntityId) -> bool:
        stmt = select(TaskModel).where(TaskModel.id == task_id.value)
        result = await self.session.execute(stmt)
        task_model = result.scalar_one_or_none()

        if task_model:
            await self.session.delete(task_model)
            await self.session.commit()
            return True
        return False

    def _to_entity(self, model: TaskModel) -> DomainTask:
        """Convert ORM model to domain entity."""
        return DomainTask(
            title=Title(value=model.title),
            description=Description(value=model.description or ""),
            state=State(value=model.state),
            id=EntityId(value=model.id),
            created_at=model.created_at,
            updated_at=model.updated_at,
        )

    def _to_model(self, entity: DomainTask) -> TaskModel:
        """Convert domain entity to ORM model."""
        return TaskModel(
            id=entity.id.value,
            title=entity.title.value,
            description=entity.description.value,
            state=entity.state.value,
            created_at=entity.created_at,
            updated_at=entity.updated_at,
        )
