"""
JWT Token Service Implementation
Handles JWT creation, validation, and refresh token storage.
"""

import logging
from datetime import datetime, timedelta

import jwt
from sqlalchemy.ext.asyncio import AsyncSession

from app.auth.domain.exeptions import (
    InvalidTokenException,
    TokenExpiredException
)
from app.auth.domain.ports import TokenServicePort
from app.auth.domain.value_objects import (
    AccessToken,
)
from app.common.value_objects import EntityId
from app.core.config import get_settings

logger = logging.getLogger(__name__)
settings = get_settings()


class JWTTokenService(TokenServicePort):
    """JWT implementation of token service with refresh token rotation."""

    # Token configuration
    ACCESS_TOKEN_EXPIRE_MINUTES = settings.ACCESS_TOKEN_EXPIRE_MINUTES
    ALGORITHM = settings.JWT_ALGORITHM
    TOKEN_TYPE = settings.TOKEN_TYPE

    def __init__(self):

        # Get secrets from settings
        self.access_secret = settings.SECRET_KEY

    async def create_access_token(
        self, user_id: EntityId
    ) -> AccessToken:
        """Create new access tokens."""
        try:
            # Generate Access Token
            access_token = self._create_token(user_id)

            logger.info(f"Token pair created for user: {user_id}")

            return access_token

        except Exception as e:
            logger.error(f"Error creating token pair: {str(e)}", exc_info=True)
            raise

    def _create_token(self, user_id: EntityId) -> AccessToken:
        """Create JWT access token."""
        now = datetime.utcnow()
        expires_at = now + timedelta(minutes=self.ACCESS_TOKEN_EXPIRE_MINUTES)

        payload = {
            "sub": str(user_id),  # Subject (user ID)
            "type": "access",  # Token type
            "iat": now,  # Issued at
            "exp": expires_at,  # Expiration
        }

        token = jwt.encode(
            payload, self.access_secret, algorithm=self.ALGORITHM
        )

        return AccessToken(
            token=token,
            token_type=self.TOKEN_TYPE,
            expires_at=expires_at
        )

    async def verify_access_token(self, token: str) -> EntityId:
        """Verify and decode access token."""
        try:
            payload = jwt.decode(
                token, self.access_secret, algorithms=[self.ALGORITHM]
            )

            # Check token type
            if payload.get("type") != "access":
                raise InvalidTokenException("Invalid token type")

            user_id = EntityId(payload["sub"])
            return user_id

        except jwt.ExpiredSignatureError:
            logger.warning("Access token expired")
            raise TokenExpiredException("Access token")
        except jwt.InvalidTokenError as e:
            logger.warning(f"Invalid access token: {str(e)}")
            raise InvalidTokenException(f"Invalid access token: {str(e)}")
        except Exception as e:
            logger.error(f"Error verifying access token: {str(e)}")
            raise InvalidTokenException("Token verification failed")
