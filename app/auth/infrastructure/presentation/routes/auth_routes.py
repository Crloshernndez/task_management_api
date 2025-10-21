from typing import Annotated


from fastapi import APIRouter, Depends, Request, status
from app.auth.infrastructure.presentation.dtos import (
    RegisterResponse,
    RegisterRequest,
    LoginResponse,
    LoginRequest
)
from app.auth.infrastructure.presentation.controllers import (
    AuthController
)
from app.auth.infrastructure.dependencies import get_auth_controller

router = APIRouter(prefix="/auth", tags=["Authentication"])


@router.post(
    "/register",
    response_model=RegisterResponse,
    status_code=status.HTTP_201_CREATED,
    summary="Register a new user",
    description="Create a new user account with email and password",
    responses={
        201: {"description": "User registered successfully"},
        400: {"description": "Invalid input data"},
        409: {"description": "Email already exists"},
    },
)
async def register(
    request: RegisterRequest,
    controller: Annotated[AuthController, Depends(get_auth_controller)],
) -> RegisterResponse:
    """
    Register a new user account.
    """
    return await controller.register(request)


@router.post(
    "/login",
    response_model=LoginResponse,
    status_code=status.HTTP_200_OK,
    summary="User login",
    description="Authenticate user and generate access/refresh tokens",
    responses={
        200: {"description": "Login successful"},
        401: {"description": "Invalid credentials or account locked"},
    },
)
async def login(
    request: LoginRequest,
    http_request: Request,
    controller: Annotated[AuthController, Depends(get_auth_controller)],
) -> LoginResponse:
    """
    Authenticate user with email and password.
    """
    return await controller.login(request, http_request)
