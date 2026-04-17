from typing import Annotated

from fastapi import Depends, HTTPException, status
from fastapi.security import OAuth2PasswordBearer
from sqlalchemy.ext.asyncio import AsyncSession

from app.core.security import decode_token
from app.db.session import AsyncSessionLocal
from app.repositories.chat_messages import ChatMessageRepository
from app.repositories.users import UserRepository
from app.services.openrouter_client import OpenRouterClient
from app.usecases.auth import AuthUseCase
from app.usecases.chat import ChatUseCase

# Схема OAuth2 для Swagger
oauth2_scheme = OAuth2PasswordBearer(tokenUrl="/auth/login")


async def get_db() -> AsyncSession:
    """Зависимость для получения сессии БД."""
    async with AsyncSessionLocal() as session:
        yield session


async def get_user_repo(db: Annotated[AsyncSession, Depends(get_db)]) -> UserRepository:
    """Зависимость для получения репозитория пользователей."""
    return UserRepository(db)


async def get_chat_repo(db: Annotated[AsyncSession, Depends(get_db)]) -> ChatMessageRepository:
    """Зависимость для получения репозитория сообщений."""
    return ChatMessageRepository(db)


def get_llm_client() -> OpenRouterClient:
    """Зависимость для получения клиента OpenRouter."""
    return OpenRouterClient()


async def get_current_user_id(
    token: Annotated[str, Depends(oauth2_scheme)],
) -> int:
    """
    Извлечь ID текущего пользователя из JWT токена.
    В случае невалидного токена выбрасывает HTTP 401.
    """
    try:
        payload = decode_token(token)
        user_id_str: str = payload.get("sub")
        if user_id_str is None:
            raise HTTPException(
                status_code=status.HTTP_401_UNAUTHORIZED,
                detail="Invalid token payload",
                headers={"WWW-Authenticate": "Bearer"},
            )
        return int(user_id_str)
    except (ValueError, TypeError) as e:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Could not validate credentials",
            headers={"WWW-Authenticate": "Bearer"},
        ) from e


async def get_auth_usecase(
    user_repo: Annotated[UserRepository, Depends(get_user_repo)],
) -> AuthUseCase:
    """Зависимость для получения usecase аутентификации."""
    return AuthUseCase(user_repo)


async def get_chat_usecase(
    chat_repo: Annotated[ChatMessageRepository, Depends(get_chat_repo)],
    llm_client: Annotated[OpenRouterClient, Depends(get_llm_client)],
) -> ChatUseCase:
    """Зависимость для получения usecase чата."""
    return ChatUseCase(chat_repo, llm_client)
