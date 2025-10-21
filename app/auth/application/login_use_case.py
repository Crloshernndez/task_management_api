"""
Login Use Case
Handles user authentication logic.
"""

from typing import Optional
import logging

from app.auth.domain.exeptions import (
    InvalidCredentialsException,
)
from app.auth.domain.ports import (
    TokenServicePort,
    UserRepositoryPort,
)
from app.auth.domain.value_objects import Email, AccessToken

logger = logging.getLogger(__name__)


class LoginUseCase:
    """Use case for user login."""

    def __init__(
        self,
        user_repository: UserRepositoryPort,
        token_service: TokenServicePort,
    ):
        self.user_repository = user_repository
        self.token_service = token_service

    async def execute(
        self,
        email: str,
        password: str,
    ) -> AccessToken:

        logger.info(f"Login attempt for email: {email}")

        email_vo = Email(value=email)

        user = await self.user_repository.get_user_by_email(email_vo)

        if not user:
            logger.warning(f"Login failed: user not found - {email}")
            # Don't reveal if email exists or not
            raise InvalidCredentialsException()

        if not user.password_hash.verify(password):
            logger.warning(f"Login failed: invalid password - {str(user.id)}")

            raise InvalidCredentialsException()

        # Successful login
        access_token = await self.token_service.create_access_token(
            user_id=user.id
        )

        logger.info(
            f"Login successful for user: {user.id}"
        )

        return access_token
