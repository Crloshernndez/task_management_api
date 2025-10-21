from abc import ABC, abstractmethod
from typing import Optional, List
from app.task.domain.entities import Task
from app.common.value_objects import EntityId


class TaskRepositoryPort(ABC):
    @abstractmethod
    async def create_task(self, task: Task) -> Task:
        pass

    @abstractmethod
    async def get_task_by_id(self, task_id: EntityId) -> Optional[Task]:
        pass

    @abstractmethod
    async def get_all_tasks(self) -> List[Task]:
        pass

    @abstractmethod
    async def update_task(self, task: Task) -> Optional[Task]:
        pass

    @abstractmethod
    async def delete_task(self, task_id: EntityId) -> bool:
        pass
