from dataclasses import dataclass
from passlib.context import CryptContext
from app.core.exceptions import (
    DomainValidationException,
    RequiredFieldException
)

pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")


@dataclass(frozen=True)
class PasswordHash:
    value: str

    def __post_init__(self):
        if not self.value:
            raise RequiredFieldException(
                message="El campo de password es requerido.",
                detail="El campo de password no puede ser nulo."
                )
        self._validate()

    def _validate(self) -> None:
        if len(self.value) < 60:
            raise DomainValidationException(
                message="Formato de hash de la contraseña inválido.",
                detail="El hash de la contraseña tiene un\
                    formato inválido.",
                code="INVALID_FORMAT"
            )

        if not self.value.startswith('$2b$'):
            raise DomainValidationException(
                message="Formato de hash de la contraseña inválido.",
                detail="El hash de la contraseña no tiene el formato\
                    bcrypt esperado.",
                code="INVALID_FORMAT"
            )

    def verify(self, plain_password: str) -> bool:
        return pwd_context.verify(plain_password, self.value)

    def __str__(self) -> str:
        return self.value
