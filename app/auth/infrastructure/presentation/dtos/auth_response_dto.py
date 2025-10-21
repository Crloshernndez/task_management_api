from pydantic import BaseModel, EmailStr, Field
from datetime import datetime
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
