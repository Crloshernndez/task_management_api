from functools import wraps
from typing import Callable, Any, Optional
import asyncio
from sqlalchemy.exc import SQLAlchemyError
from app.core.exceptions import DatabaseOperationError


def exception_repository_handlers(
    operation_name: Optional[str] = None,
):
    def decorator(func: Callable) -> Callable:
        @wraps(func)
        async def async_wrapper(self, *args, **kwargs) -> Any:
            try:
                return await func(self, *args, **kwargs)

            except SQLAlchemyError as e:
                raise DatabaseOperationError(
                    message=(
                        f"Fallo al crear {operation_name} en base de datos."
                    ),
                    detail=str(e),
                    code="DATABASE_OPERATION_ERROR",
                )

            except Exception as e:
                raise DatabaseOperationError(
                    message=f"Error inesperado al crear {operation_name}",
                    detail=str(e),
                    code="UNEXPECTED_DATABASE_ERROR",
                )

        @wraps(func)
        def sync_wrapper(self, *args, **kwargs) -> Any:
            try:
                return func(self, *args, **kwargs)

            except SQLAlchemyError as e:
                raise DatabaseOperationError(
                    message=(
                        f"Fallo al crear {operation_name} en base de datos."
                    ),
                    detail=str(e),
                    code="DATABASE_OPERATION_ERROR",
                )

            except Exception as e:
                raise DatabaseOperationError(
                    message=f"Error inesperado al crear {operation_name}",
                    detail=str(e),
                    code="UNEXPECTED_DATABASE_ERROR",
                )

        if asyncio.iscoroutinefunction(func):
            return async_wrapper
        return sync_wrapper
    return decorator
