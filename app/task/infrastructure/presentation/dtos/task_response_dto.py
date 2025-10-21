from pydantic import BaseModel, Field
from uuid import UUID


class TaskResponse(BaseModel):
    """Task information response."""

    id: UUID
    title: str
    description: str
    state: str

    class Config:
        from_attributes = True
        json_schema_extra = {
            "example": {
                "id": "123e4567-e89b-12d3-a456-426614174000",
                "title": "example title",
                "description": "This is an example description",
                "state": "pending"
            }
        }


class RegisterTaskResponse(BaseModel):
    """Registration success response."""

    message: str = Field(..., description="Success message")
    task: TaskResponse = Field(..., description="Created task information")

    class Config:
        json_schema_extra = {
            "example": {
                "message": "Task registered successfully.",
                "task": {
                    "id": "123e4567-e89b-12d3-a456-426614174000",
                    "title": "example title",
                    "description": "This is an example description",
                    "state": "pending"
                },
            }
        }


class GetAllTasksResponse(BaseModel):
    """Get all tasks response."""

    message: str = Field(..., description="Success message")
    tasks: list[TaskResponse] = Field(..., description="List of tasks")

    class Config:
        json_schema_extra = {
            "example": {
                "message": "Tasks retrieved successfully.",
                "tasks": [
                    {
                        "id": "123e4567-e89b-12d3-a456-426614174000",
                        "title": "example title",
                        "description": "This is an example description",
                        "state": "pending"
                    }
                ],
            }
        }
