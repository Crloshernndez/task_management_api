from dataclasses import dataclass
import re
from app.core.exceptions import (
    DomainValidationException,
    RequiredFieldException
)


@dataclass(frozen=True)
class Email:
    value: str

    def __post_init__(self):
        if not self.value:
            raise RequiredFieldException(
                message="El campo de email es requerido.",
                detail="El campo de email no puede ser nulo."
                )

        self._validate()

    def _validate(self) -> None:
        email_regex = r"^[a-zA-Z0-9._%+-]+@[a-zA-Z0-9.-]+\.[a-zA-Z]{2,}$"

        if not re.match(email_regex, self.value):
            raise DomainValidationException(
                message="Formato de email invalido.",
                detail="El email no es un formato válido.",
                code="INVALID_FORMAT"
                )

    def __str__(self):
        return self.value
