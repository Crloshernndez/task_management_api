from pydantic import BaseModel, Field
from typing import Optional
from uuid import UUID


class UserResponse(BaseModel):
    """User information response."""

    id: UUID
    email: str
    username: Optional[str] = None

    class Config:
        from_attributes = True
        json_schema_extra = {
            "example": {
                "id": "123e4567-e89b-12d3-a456-426614174000",
                "email": "user@example.com",
                "username": "John",
            }
        }


class RegisterResponse(BaseModel):
    """Registration success response."""

    message: str = Field(..., description="Success message")
    user: UserResponse = Field(..., description="Created user information")

    class Config:
        json_schema_extra = {
            "example": {
                "message": "User registered successfully. Please verify your email.",
                "user": {
                    "id": "123e4567-e89b-12d3-a456-426614174000",
                    "email": "user@example.com",
                    "username": "John",
                },
            }
        }


class TokenResponse(BaseModel):
    """Token pair response."""

    access_token: str = Field(..., description="JWT access token")
    token_type: str = Field(default="Bearer", description="Token type")
    expires_in: int = Field(
        ..., description="Access token expiration in seconds"
    )

    class Config:
        json_schema_extra = {
            "example": {
                "access_token": "eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9...",
                "token_type": "Bearer",
                "expires_in": 1800,
            }
        }


class LoginResponse(BaseModel):
    """Login success response."""

    message: str = Field(..., description="Success message")
    token: TokenResponse = Field(..., description="Authentication tokens")

    class Config:
        json_schema_extra = {
            "example": {
                "message": "Login successful",
                "token": {
                    "access_token": "eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9...",
                    "token_type": "Bearer",
                    "expires_in": 1800,
                },
            }
        }
