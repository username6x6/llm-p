from pydantic import BaseModel, EmailStr, Field, field_validator


class RegisterRequest(BaseModel):
    """Схема запроса на регистрацию."""

    email: EmailStr
    password: str = Field(..., min_length=6, max_length=128, description="Пароль от 6 до 128 символов")

    @field_validator("password")
    def validate_password_length(cls, v: str) -> str:
        if len(v) < 6:
            raise ValueError("Пароль должен содержать минимум 6 символов")
        return v


class TokenResponse(BaseModel):
    """Схема ответа с JWT токеном."""

    access_token: str
    token_type: str = "bearer"