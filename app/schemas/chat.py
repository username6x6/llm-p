from typing import Optional

from pydantic import BaseModel, Field, ConfigDict


class ChatRequest(BaseModel):
    """Запрос к чат-модели."""

    prompt: str = Field(..., description="Основной текст запроса пользователя")
    system: Optional[str] = Field(None, description="Системная инструкция (опционально)")
    max_history: int = Field(10, ge=0, le=50, description="Максимальное количество сообщений из истории для контекста")
    temperature: float = Field(0.7, ge=0.0, le=2.0, description="Температура генерации (креативность)")


class ChatResponse(BaseModel):
    """Ответ от LLM."""

    answer: str = Field(..., description="Текст ответа модели")


class ChatMessagePublic(BaseModel):
    """Публичная схема сообщения для истории."""

    id: int
    role: str
    content: str
    created_at: str  # ISO формат

    model_config = ConfigDict(from_attributes=True)