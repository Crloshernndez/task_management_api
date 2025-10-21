from .base import BaseApplicationException


class InfrastructureException(BaseApplicationException, Exception):
    """
    Base exception for all infrastructure-related errors.
    """
    def __init__(
            self,
            message: str,
            detail: Exception = None,
            code: str = "INFRASTRUCTURE_ERROR"
            ):
        self.message = message
        self.detail = detail
        self.code = code
        super().__init__(
            self.message,
            self.detail,
            self.code
        )


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
            detail: Exception = None):
        super().__init__(message, detail)


class RateLimitException(InfrastructureException):
    """Raised when rate limit is exceeded."""

    def __init__(self, message: str = "Rate limit exceeded", **kwargs):
        kwargs.setdefault("status_code", 429)
        kwargs.setdefault("error_code", "RATE_LIMIT_ERROR")
        super().__init__(message, **kwargs)
