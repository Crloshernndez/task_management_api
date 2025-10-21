from dataclasses import dataclass
from app.core.exceptions import (
    DomainValidationException,
    RequiredFieldException
)


@dataclass(frozen=True)
class Title:
    value: str

    def __post_init__(self):
        if not self.value:
            raise RequiredFieldException(
                message="El campo de título es requerido.",
                detail="El campo de título no puede ser nulo o vacío."
            )

        self._validate()

    def _validate(self) -> None:

        cleaned_value = self.value.strip()

        if not cleaned_value:
            raise DomainValidationException(
                message="Formato de título inválido.",
                detail="El título no puede contener solo espacios en blanco.",
                code="INVALID_FORMAT"
            )

        if len(cleaned_value) < 1:
            raise DomainValidationException(
                message="Formato de título inválido.",
                detail="El título debe tener al menos 1 carácter.",
                code="INVALID_FORMAT"
            )

        if len(cleaned_value) > 200:
            raise DomainValidationException(
                message="Formato de título inválido.",
                detail="El título no puede exceder 200 caracteres.",
                code="INVALID_FORMAT"
            )

    def __str__(self) -> str:
        return self.value
