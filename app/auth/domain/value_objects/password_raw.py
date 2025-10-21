from dataclasses import dataclass
import re
from app.core.exceptions import (
    DomainValidationException,
    RequiredFieldException
)


@dataclass(frozen=True)
class PasswordRaw:
    value: str

    def __post_init__(self):
        if not self.value:
            raise RequiredFieldException(
                message="El campo password es requerido.",
                detail="El campo password no puede estar vacío."
                )

        self._validate()

    def _validate(self) -> None:
        if len(self.value) < 6:
            raise DomainValidationException(
                message="Formato de password inválido.",
                detail="La contraseña debe tener al menos 6 caracteres.",
                code="INVALID_FORMAT"
            )
        if len(self.value) > 128:
            raise DomainValidationException(
                message="Formato de password inválido.",
                detail="La contraseña no puede tener más de 128 caracteres.",
                code="INVALID_FORMAT"
            )
        if not re.search(r'[A-Z]', self.value):
            raise DomainValidationException(
                message="Formato de password inválido.",
                detail="La contraseña debe contener al menos una mayúscula.",
                code="INVALID_FORMAT"
            )
        if not re.search(r'[a-z]', self.value):
            raise DomainValidationException(
                message="Formato de password inválido.",
                detail="La contraseña debe contener al menos una minúscula.",
                code="INVALID_FORMAT"
            )
        if not re.search(r'\d', self.value):
            raise DomainValidationException(
                message="Formato de password inválido.",
                detail="La contraseña debe contener al menos un número.",
                code="INVALID_FORMAT"
            )
