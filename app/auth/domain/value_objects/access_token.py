"""
Token Value Objects
Represents access and refresh tokens.
"""

from typing import Dict, Any
from dataclasses import dataclass
from datetime import datetime


@dataclass(frozen=True)
class AccessToken:
    """Access token value object."""

    token: str
    expires_at: datetime
    token_type: str = "Bearer"

    def is_expired(self) -> bool:
        """Check if token is expired."""
        return datetime.utcnow() >= self.expires_at

    def to_dict(self) -> Dict[str, Any]:
        expires_in = int((self.expires_at - datetime.utcnow()).total_seconds())
        return {
            "access_token": self.token,
            "token_type": self.token_type,
            "expires_in": expires_in
        }

    def __str__(self) -> str:
        return self.token
