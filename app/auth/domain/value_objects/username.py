from dataclasses import dataclass
import re
from app.core.exceptions import (
    DomainValidationException,
    RequiredFieldException
)


@dataclass(frozen=True)
class Username:
    value: str

    def __post_init__(self):
        if not self.value:
            raise RequiredFieldException(
                message="El campo de username es requerido.",
                detail="El campo de username no puede ser nulo."
            )

        self._validate()

    def _validate(self) -> None:
        if not (3 <= len(self.value) <= 30):
            raise DomainValidationException(
                message="Formato de username invalido.",
                detail=f"El nombre de usuario '{self.value}' debe tener\
entre 3 y 30 caracteres.",
                code="INVALID_FORMAT"
            )

        if not re.match(r"^[a-zA-Z0-9_.]+$", self.value):
            raise DomainValidationException(
                message="Formato de username invalido.",
                detail=f"El nombre de usuario '{self.value}' solo puede \
contener letras, números, guiones bajos y puntos.",
                code="INVALID_FORMAT"
            )

    def __str__(self) -> str:
        return self.value
