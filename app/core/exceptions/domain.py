from .base import BaseApplicationException


class DomainValidationException(BaseApplicationException):
    """
    Base exception for validation errors within the domain layer.
    """
    def __init__(
            self,
            message: str,
            code: str = "DOMAIN_VALIDATION_ERROR",
            detail: str = None
            ):
        self.detail = detail
        super().__init__(message, code)


class RequiredFieldException(DomainValidationException):
    """
    Exception raised when a required field is missing or empty in the domain.
    """
    def __init__(self, message: str = None):
        super().__init__(message)
        self.code = "REQUIRED_FIELD"


class InvalidUUIDException(DomainValidationException):
    """
    Exception raised when a value is not a valid UUID format in the domain.
    """
    def __init__(self):
        super().__init__(
            message="Formato de ID invalido.",
            code="INVALID_FORMAT"
        )
