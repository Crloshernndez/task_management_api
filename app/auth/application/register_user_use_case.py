import uuid
from fastapi import Depends
from passlib.context import CryptContext
from app.auth.domain.entities import User
from app.auth.domain.ports import UserRepositoryPort
from app.common.value_objects import EntityId

from app.auth.domain.value_objects import (
    Email,
    Username,
    PasswordRaw,
    PasswordHash,
)
from app.core.exceptions import DomainValidationException


pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")


class RegisterUserUseCase:
    def __init__(self, user_repository: UserRepositoryPort):
        self._user_repository = user_repository

    async def execute(
        self,
        user_data: dict
    ) -> User:
        # Validate required fields
        required_fields = ['email', 'username', 'password']
        for field in required_fields:
            if not user_data.get(field):
                raise DomainValidationException(
                    message="Datos incompletos",
                    detail=f"El campo '{field}' es requerido.",
                    code="MISSING_REQUIRED_FIELD"
                )

        # Create value objects (will validate format)
        email_vo = Email(user_data.get('email'))
        username_vo = Username(user_data.get('username'))
        password_vo = PasswordRaw(user_data.get('password'))

        # Check for existing user with email
        if await self._user_repository.get_user_by_email(email_vo):
            raise DomainValidationException(
                message="Email ya registrado",
                detail=f"Ya existe un usuario con el email '{email_vo.value}'.",
                code="EMAIL_ALREADY_REGISTERED"
            )

        # Check for existing user with username
        if await self._user_repository.get_user_by_username(username_vo):
            raise DomainValidationException(
                message="Nombre de usuario ya registrado",
                detail=f"Ya existe un usuario con el nombre de usuario '{username_vo.value}'.",
                code="USERNAME_ALREADY_REGISTERED"
            )

        hashed_password_vo = PasswordHash(
            self._get_password_hash(password_vo.value)
        )

        new_user_entity = User(
            id=EntityId(uuid.uuid4()),
            email=email_vo,
            username=username_vo,
            password_hash=hashed_password_vo
        )

        created_user = await self._user_repository.create_user(new_user_entity)
        return created_user

    def _get_password_hash(self, password: str) -> str:
        return pwd_context.hash(password)
