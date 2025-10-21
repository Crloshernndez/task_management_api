from dataclasses import dataclass
from enum import Enum
from app.core.exceptions import (
    DomainValidationException,
    RequiredFieldException
)


class TaskStatus(str, Enum):
    """Enumeration of valid task statuses."""
    PENDING = "pending"
    COMPLETED = "completed"


@dataclass(frozen=True)
class State:
    value: str

    def __post_init__(self):
        if not self.value:
            raise RequiredFieldException(
                message="El campo de estado es requerido.",
                detail="El campo de estado no puede ser nulo o vacío."
            )

        self._validate()

    def _validate(self) -> None:
        valid_statuses = [status.value for status in TaskStatus]

        if self.value not in valid_statuses:
            raise DomainValidationException(
                message="Estado de tarea inválido.",
                detail=f"El estado debe ser uno de: {', '.join(valid_statuses)}.",
                code="INVALID_STATUS"
            )

    def is_pending(self) -> bool:
        """Check if task is in pending state."""
        return self.value == TaskStatus.PENDING.value

    def is_completed(self) -> bool:
        """Check if task is in completed state."""
        return self.value == TaskStatus.COMPLETED.value

    def __str__(self) -> str:
        return self.value
