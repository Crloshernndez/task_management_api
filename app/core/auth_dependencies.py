from fastapi import Depends, HTTPException, status
from app.core.security import oauth2_scheme, verify_token
from app.services.user_service import UserService, get_user_service
from app.domain.exceptions import DomainValidationException
from app.domain.entities.user import User as DomainUser


async def get_current_user(
    token: str = Depends(oauth2_scheme),
    user_service: UserService = Depends(get_user_service)
) -> DomainUser:

    credentials_exception = HTTPException(
        status_code=status.HTTP_401_UNAUTHORIZED,
        detail={
            "status": "error",
            "error": {
                "code": "INVALID_AUTHENTICATION_TOKEN",
                "message": "No se pudieron validar las credenciales.",
                "details": "Token de autenticación inválido o expirado."
            }
        },
        headers={"WWW-Authenticate": "Bearer"},
    )

    payload = verify_token(token)
    if payload is None:
        raise credentials_exception

    user_id: str = payload.get("sub")
    if user_id is None:
        raise credentials_exception

    try:
        user = user_service.get_user_by_id(user_id)
        if user is None:
            raise credentials_exception
        return user
    except DomainValidationException:
        raise credentials_exception
    except Exception:
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail={
                "status": "error",
                "error": {
                    "code": "INTERNAL_SERVER_ERROR",
                    "message": "Error interno al recuperar el "
                    "usuario autenticado.",
                    "details": None
                }
            }
        )
