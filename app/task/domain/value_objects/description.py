from dataclasses import dataclass
from app.core.exceptions import (
    DomainValidationException,
    RequiredFieldException
)


@dataclass(frozen=True)
class Description:
    value: str

    def __post_init__(self):
        if self.value is None:
            raise RequiredFieldException(
                message="El campo de descripción es requerido.",
                detail="El campo de descripción no puede ser nulo."
            )

        self._validate()

    def _validate(self) -> None:
        # Permitir descripciones vacías
        if not self.value:
            return

        cleaned_value = self.value.strip()

        # Si tiene contenido, no puede ser solo espacios
        if self.value and not cleaned_value:
            raise DomainValidationException(
                message="Formato de descripción inválido.",
                detail="La descripción no puede contener solo espacios en blanco.",
                code="INVALID_FORMAT"
            )

        if len(cleaned_value) > 1000:
            raise DomainValidationException(
                message="Formato de descripción inválido.",
                detail="La descripción no puede exceder 1000 caracteres.",
                code="INVALID_FORMAT"
            )

    def __str__(self) -> str:
        return self.value
