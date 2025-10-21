import uuid
from dataclasses import dataclass
from datetime import datetime
from typing import Optional
from app.common.value_objects import EntityId
from app.task.domain.value_objects import (
    Title,
    Description,
    State
)


@dataclass(frozen=True)
class Task:
    title: Title
    description: Description
    state: State

    id: Optional[EntityId] = None
    created_at: Optional[datetime] = None
    updated_at: Optional[datetime] = None

    def __post_init__(self):
        if self.id is None:
            object.__setattr__(self, 'id', EntityId(value=uuid.uuid4()))
        if self.created_at is None:
            object.__setattr__(self, 'created_at', datetime.now())
        if self.updated_at is None:
            object.__setattr__(self, 'updated_at', datetime.now())

    def to_dict(self) -> dict:
        return {
            "title": self.title.value,
            "description": self.description.value,
            "state": self.state.value,
            "created_at": self.created_at,
            "updated_at": self.updated_at
        }
