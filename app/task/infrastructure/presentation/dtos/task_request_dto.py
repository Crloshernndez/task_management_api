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


class UpdateTaskRequest(BaseModel):
    """Request for task update."""

    title: Optional[str] = Field(None, description="task title")
    description: Optional[str] = Field(None, description="task description")
    state: Optional[str] = Field(None, description="task state (pending, completed)")

    class Config:
        json_schema_extra = {
            "example": {
                "title": "updated title",
                "description": "This is an updated description",
                "state": "completed"
            }
        }
