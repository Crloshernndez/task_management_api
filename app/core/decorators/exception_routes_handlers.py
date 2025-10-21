from functools import wraps
from fastapi import status, HTTPException
from fastapi.responses import JSONResponse
from app.core.exceptions import (
    DomainValidationException,
    RequiredFieldException
)


def handle_api_exceptions(func):
    @wraps(func)
    async def wrapper(*args, **kwargs):
        try:
            return await func(*args, **kwargs)

        except RequiredFieldException as e:
            return JSONResponse(
                status_code=status.HTTP_400_BAD_REQUEST,
                content=e.to_dict()
            )

        except DomainValidationException as e:
            return JSONResponse(
                status_code=status.HTTP_400_BAD_REQUEST,
                content=e.to_dict()
            )

        except HTTPException as e:
            return JSONResponse(
                status_code=e.status_code,
                content={"detail": e.detail}
            )

        except Exception as e:
            return JSONResponse(
                status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
                content={
                    "status": "error",
                    "error": {
                        "code": "INTERNAL_SERVER_ERROR",
                        "message": "Error interno del servidor",
                        "details": str(e)
                    }
                }
            )

    return wrapper
