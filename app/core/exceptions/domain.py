from .base import BaseApplicationException


class DomainValidationException(BaseApplicationException, ValueError):
    """
    Base exception for validation errors within the domain layer.
    """
    def __init__(
            self,
            message: str,
            detail: str = None,
            code: str = "DOMAIN_VALIDATION_ERROR"
            ):
        self.message = message
        self.detail = detail
        self.code = code
        super().__init__(
            self.message,
            self.detail,
            self.code
        )


class RequiredFieldException(DomainValidationException):
    """
    Exception raised when a required field is missing or empty in the domain.
    """
    def __init__(self, detail: str, message: str = None):
        super().__init__(message, detail=detail)
        self.code = "REQUIRED_FIELD"


class InvalidUUIDException(DomainValidationException):
    """
    Exception raised when a value is not a valid UUID format in the domain.
    """
    def __init__(self):
        self.code = "INVALID_FORMAT"
        self.message = "Formato de ID invalido."
        self.detail = "El valor del ID no es un formato de \
uuid válido."
