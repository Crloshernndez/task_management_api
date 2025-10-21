from typing import Annotated
from fastapi import Depends, HTTPException, status
from fastapi.security import HTTPBearer, HTTPAuthorizationCredentials
from sqlalchemy.ext.asyncio import AsyncSession

from app.core.database import get_async_session
from app.auth.application import RegisterUserUseCase, LoginUseCase
from app.auth.infrastructure.repositories import (
    UserRepository
)
from app.auth.infrastructure.presentation.controllers import (
    AuthController
)
from app.auth.infrastructure.adapters import JWTTokenService
from app.auth.domain.exeptions import InvalidTokenException, TokenExpiredException
from app.common.value_objects import EntityId

security = HTTPBearer()

# ============================================================================
# Service Dependencies
# ============================================================================


async def get_user_repository(
    session: Annotated[AsyncSession, Depends(get_async_session)],
) -> UserRepository:
    """Get UserRepository instance."""
    return UserRepository(session)


async def get_token_service() -> JWTTokenService:
    """Get JWTTokenService instance."""
    return JWTTokenService()


# ============================================================================
# Service Dependencies
# ============================================================================


async def get_register_user_use_case(
    user_repository: Annotated[
        UserRepository, Depends(get_user_repository)
    ]
) -> RegisterUserUseCase:
    return RegisterUserUseCase(user_repository)


async def get_login_use_case(
    user_repository: Annotated[
        UserRepository, Depends(get_user_repository)
    ],
    token_service: Annotated[
        JWTTokenService, Depends(get_token_service)
    ]
) -> LoginUseCase:
    return LoginUseCase(
        user_repository=user_repository,
        token_service=token_service
    )

# ============================================================================
# Controller Dependencies
# ============================================================================


async def get_auth_controller(
    register_use_case: Annotated[
        RegisterUserUseCase, Depends(get_register_user_use_case)
    ],
    login_use_case: Annotated[
        LoginUseCase, Depends(get_login_use_case)
    ]
) -> AuthController:
    """
    Create auth controller with all dependencies.
    """
    return AuthController(
        register_use_case=register_use_case,
        login_use_case=login_use_case
    )


# ============================================================================
# Authentication Dependencies
# ============================================================================


async def get_current_user_id(
    credentials: Annotated[HTTPAuthorizationCredentials, Depends(security)],
    token_service: Annotated[JWTTokenService, Depends(get_token_service)]
) -> EntityId:
    try:
        user_id = await token_service.verify_access_token(credentials.credentials)
        return user_id

    except TokenExpiredException:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail={
                "status": "error",
                "error": {
                    "code": "TOKEN_EXPIRED",
                    "message": "Token expirado.",
                    "details": "El token de autenticación ha expirado."
                }
            },
            headers={"WWW-Authenticate": "Bearer"},
        )

    except InvalidTokenException:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail={
                "status": "error",
                "error": {
                    "code": "INVALID_TOKEN",
                    "message": "Token inválido.",
                    "details": "El token de autenticación es inválido."
                }
            },
            headers={"WWW-Authenticate": "Bearer"},
        )

    except Exception as e:
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail={
                "status": "error",
                "error": {
                    "code": "INTERNAL_SERVER_ERROR",
                    "message": "Error interno del servidor.",
                    "details": str(e)
                }
            }
        )
