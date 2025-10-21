import uuid
from dataclasses import dataclass
from datetime import datetime
from typing import Optional
from app.common.value_objects import EntityId
from app.auth.domain.value_objects import (
    Email,
    Username,
    PasswordHash
)


@dataclass(frozen=True)
class User:
    email: Email
    username: Username
    password_hash: PasswordHash

    id: Optional[EntityId] = None
    created_at: Optional[datetime] = None
    updated_at: Optional[datetime] = None

    def __post_init__(self):
        if self.id is None:
            object.__setattr__(self, 'id', uuid.uuid4())
        if self.created_at is None:
            object.__setattr__(self, 'created_at', datetime.now())
        if self.updated_at is None:
            object.__setattr__(self, 'updated_at', datetime.now())

    def to_dict(self) -> dict:
        return {
            "email": str(self.email),
            "username": self.username.value,
        }
