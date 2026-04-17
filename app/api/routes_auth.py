from typing import Annotated

from fastapi import APIRouter, Depends, HTTPException, status
from fastapi.security import OAuth2PasswordRequestForm

from app.api.deps import get_auth_usecase, get_current_user_id
from app.core.errors import ConflictError, NotFoundError, UnauthorizedError
from app.schemas.auth import RegisterRequest, TokenResponse
from app.schemas.user import UserPublic
from app.usecases.auth import AuthUseCase

router = APIRouter(prefix="/auth", tags=["Authentication"])


@router.post("/register", response_model=UserPublic, status_code=status.HTTP_201_CREATED)
async def register(
    request: RegisterRequest,
    auth_usecase: Annotated[AuthUseCase, Depends(get_auth_usecase)],
):
    """Регистрация нового пользователя."""
    try:
        return await auth_usecase.register(request.email, request.password)
    except ConflictError as e:
        raise HTTPException(status_code=status.HTTP_409_CONFLICT, detail=str(e))


@router.post("/login", response_model=TokenResponse)
async def login(
    form_data: Annotated[OAuth2PasswordRequestForm, Depends()],
    auth_usecase: Annotated[AuthUseCase, Depends(get_auth_usecase)],
):
    """
    Вход в систему.
    Используется форма OAuth2 (username=email, password).
    """
    try:
        access_token = await auth_usecase.login(form_data.username, form_data.password)
        return TokenResponse(access_token=access_token)
    except UnauthorizedError as e:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail=str(e),
            headers={"WWW-Authenticate": "Bearer"},
        )


@router.get("/me", response_model=UserPublic)
async def get_me(
    current_user_id: Annotated[int, Depends(get_current_user_id)],
    auth_usecase: Annotated[AuthUseCase, Depends(get_auth_usecase)],
):
    """Получить профиль текущего пользователя."""
    try:
        return await auth_usecase.get_profile(current_user_id)
    except NotFoundError as e:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=str(e))