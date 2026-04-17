import json
from typing import Dict, List, Optional

import httpx

from app.core.config import settings
from app.core.errors import ExternalServiceError


class OpenRouterClient:
    """Клиент для взаимодействия с OpenRouter API."""

    def __init__(self):
        self.base_url = settings.openrouter_base_url.rstrip("/")
        self.api_key = settings.openrouter_api_key
        self.model = settings.openrouter_model
        self.referer = settings.openrouter_referer
        self.title = settings.openrouter_title

    async def chat_completion(
        self,
        messages: List[Dict[str, str]],
        temperature: float = 0.7,
        max_tokens: Optional[int] = None,
    ) -> str:
        """
        Отправить запрос на /chat/completions и вернуть текст ответа.
        В случае ошибки выбрасывается ExternalServiceError.
        """
        headers = {
            "Authorization": f"Bearer {self.api_key}",
            "HTTP-Referer": self.referer,
            "X-Title": self.title,
            "Content-Type": "application/json",
        }

        payload = {
            "model": self.model,
            "messages": messages,
            "temperature": temperature,
        }
        if max_tokens:
            payload["max_tokens"] = max_tokens

        async with httpx.AsyncClient(timeout=60.0) as client:
            try:
                response = await client.post(
                    f"{self.base_url}/chat/completions",
                    headers=headers,
                    json=payload,
                )
                response.raise_for_status()
                data = response.json()
                # Извлекаем текст ответа
                return data["choices"][0]["message"]["content"]
            except httpx.HTTPStatusError as e:
                # Пытаемся получить детали ошибки из тела ответа
                detail = await e.response.aread()
                raise ExternalServiceError(
                    f"OpenRouter returned {e.response.status_code}: {detail.decode()[:200]}"
                )
            except (httpx.RequestError, KeyError, json.JSONDecodeError) as e:
                raise ExternalServiceError(f"OpenRouter request failed: {str(e)}")