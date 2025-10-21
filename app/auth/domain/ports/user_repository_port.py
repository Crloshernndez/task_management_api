from abc import ABC, abstractmethod
from typing import Optional
from app.auth.domain.entities import User
from app.auth.domain.value_objects import (
    Email,
    Username
)


class UserRepositoryPort(ABC):
    @abstractmethod
    def create_user(self, user: User) -> User:
        pass

    @abstractmethod
    def get_user_by_id(self, user_id: str) -> Optional[User]:
        pass

    @abstractmethod
    def get_user_by_email(self, email: Email) -> Optional[User]:
        pass

    @abstractmethod
    def get_user_by_username(self, username: Username) -> Optional[User]:
        pass
