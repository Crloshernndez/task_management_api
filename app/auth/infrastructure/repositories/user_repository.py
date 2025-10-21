"""
User Repository Implementation
Concrete implementation of UserRepository using SQLAlchemy.
"""

from typing import Optional
import logging

from app.core.decorators.exception_repository_handlers import exception_repository_handlers
from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.orm import selectinload

from app.auth.domain.entities import User
from app.auth.domain.ports import UserRepositoryPort
from app.auth.domain.value_objects import Email, PasswordHash, Username
from app.auth.infrastructure.repositories.models import UserModel
from app.auth.domain.entities import User as DomainUser
from app.common.value_objects import EntityId

logger = logging.getLogger(__name__)


class UserRepository(UserRepositoryPort):
    """SQLAlchemy implementation of user repository."""

    def __init__(self, session: AsyncSession):
        self.session = session

    @exception_repository_handlers("register user")
    async def create_user(self, user: DomainUser) -> DomainUser:
        db_user = self._to_model(user)
        self.session.add(db_user)
        await self.session.commit()
        await self.session.refresh(db_user)

        return self._to_entity(db_user)

    @exception_repository_handlers("find by id user")
    async def get_user_by_id(self, user_id: EntityId) -> Optional[User]:
        stmt = (
            select(UserModel)
            .where(UserModel.id == user_id.value)
            .options(selectinload(UserModel.roles))
        )
        result = await self.session.execute(stmt)
        user_model = result.unique().scalar_one_or_none()

        if user_model:
            return self._to_entity(user_model)
        return None

    @exception_repository_handlers("find by email user")
    async def get_user_by_email(self, email: Email) -> Optional[User]:
        stmt = (
            select(UserModel)
            .where(UserModel.email == email.value)
        )
        result = await self.session.execute(stmt)
        user_model = result.unique().scalar_one_or_none()
        if user_model:
            return self._to_entity(user_model)
        return None

    @exception_repository_handlers("exist by username user")
    async def get_user_by_username(self, username: Username) -> bool:
        stmt = select(UserModel.id).where(UserModel.username == username.value)
        result = await self.session.execute(stmt)
        return result.scalar_one_or_none() is not None

    def _to_entity(self, model: UserModel) -> User:
        """Convert ORM model to domain entity."""
        return User(
            id=EntityId(model.id),
            email=Email(value=model.email),
            username=Username(model.username),
            password_hash=PasswordHash(model.hashed_password),
            created_at=model.created_at,
            updated_at=model.updated_at,
        )

    def _to_model(self, entity: User) -> UserModel:
        """Convert domain entity to ORM model."""
        return UserModel(
            id=entity.id.value,
            email=entity.email.value,
            username=entity.username.value,
            hashed_password=entity.password_hash.value,
            created_at=entity.created_at,
            updated_at=entity.updated_at,
        )
