from typing import Optional
from pydantic import BaseModel, Field


class RegisterTaskRequest(BaseModel):
    """Request for task registration."""

    title: str = Field(..., description="task title")
    description: str = Field(
        ...,
        description="task description",
    )

    class Config:
        json_schema_extra = {
            "example": {
                "title": "example title",
                "description": "This is a example description"
            }
        }
