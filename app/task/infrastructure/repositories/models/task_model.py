"""
User ORM Model
SQLAlchemy model for user persistence.
"""

from datetime import datetime
from typing import Optional
from uuid import UUID as UUIDType
from uuid import uuid4

from sqlalchemy import DateTime, String, Text
from sqlalchemy.dialects.postgresql import UUID
from sqlalchemy.orm import Mapped, mapped_column

from app.core.database import Base


class TaskModel(Base):
    """
    User table model.
    Maps to 'users' table in database.
    Note: Does not inherit from BaseModel as it uses UUID as primary key instead of Integer.
    """

    __tablename__ = "tasks"

    # Primary key
    id: Mapped[UUIDType] = mapped_column(
        UUID(as_uuid=True), primary_key=True, default=uuid4, index=True
    )

    title: Mapped[str] = mapped_column(
        String(255), index=True, nullable=False
    )
    description: Mapped[Optional[str]] = mapped_column(Text, nullable=True)

    state: Mapped[str] = mapped_column(
        String(20), index=True, nullable=False
    )

    # Timestamps
    created_at: Mapped[datetime] = mapped_column(
        DateTime(timezone=True), default=datetime.utcnow, nullable=False
    )
    updated_at: Mapped[datetime] = mapped_column(
        DateTime(timezone=True),
        default=datetime.utcnow,
        onupdate=datetime.utcnow,
        nullable=False,
    )

    def __repr__(self) -> str:
        return f"<TaskModel(id={self.id}, title={self.title})>"
