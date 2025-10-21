"""
Token Service Port
Interface for JWT token operations.
"""

from abc import ABC, abstractmethod
from app.auth.domain.value_objects import (
    AccessToken,
)
from app.common.value_objects import EntityId


class TokenServicePort(ABC):
    """Interface for token generation and validation."""

    @abstractmethod
    async def create_access_token(
        self, user_id: EntityId
    ) -> AccessToken:
        """
        Create an access token.
        """
        pass

    @abstractmethod
    async def verify_access_token(self, token: str) -> EntityId:
        """
        Verify and decode access token.
        """
        pass
