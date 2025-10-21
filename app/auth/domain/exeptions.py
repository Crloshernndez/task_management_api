from app.core.exceptions import BaseApplicationException


class AuthenticationException(BaseApplicationException):
    """Raised when authentication fails."""

    def __init__(self, message: str = "Authentication failed", **kwargs):
        kwargs.setdefault("code", "AUTHENTICATION_ERROR")
        super().__init__(message, **kwargs)


class InvalidCredentialsException(AuthenticationException):
    """Raised when login credentials are invalid."""

    def __init__(self):
        super().__init__(
            message="Invalid email or password",
            code="INVALID_CREDENTIALS",
        )


class InvalidTokenException(AuthenticationException):
    """Raised when token format or signature is invalid."""

    def __init__(self, reason: str = "Invalid token"):
        super().__init__(message=reason, code="INVALID_TOKEN")


class TokenExpiredException(AuthenticationException):
    """Raised when token has expired."""

    def __init__(self, token_type: str = "Token"):
        super().__init__(
            message=f"{token_type} has expired", code="TOKEN_EXPIRED"
        )
