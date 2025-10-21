from .base import BaseApplicationException


class InfrastructureException(BaseApplicationException):
    """
    Base exception for all infrastructure-related errors.
    """
    def __init__(
            self,
            message: str,
            detail: Exception = None,
            code: str = "INFRASTRUCTURE_ERROR"
            ):
        self.detail = detail
        super().__init__(message, code)


class DatabaseConnectionError(InfrastructureException):
    """
    Exception raised when there's an issue connecting to the database.
    """
    def __init__(
            self,
            message: str = "Error de conexión a la base de datos.",
            detail: Exception = None
            ):
        super().__init__(message, detail)


class DatabaseOperationError(InfrastructureException):
    """
    Exception raised when a database operation
    (e.g., insert, update, delete, query) fails.
    """
    def __init__(
            self,
            message: str = "Error en operación de base de datos.",
            detail: Exception = None,
            code: str = "DATABASE_OPERATION_ERROR"):
        super().__init__(message, detail, code)


class RateLimitException(InfrastructureException):
    """Raised when rate limit is exceeded."""

    def __init__(self, message: str = "Rate limit exceeded", **kwargs):
        kwargs.setdefault("status_code", 429)
        kwargs.setdefault("error_code", "RATE_LIMIT_ERROR")
        super().__init__(message, **kwargs)
