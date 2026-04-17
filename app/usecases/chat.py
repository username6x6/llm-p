from typing import List, Optional

from app.repositories.chat_messages import ChatMessageRepository
from app.schemas.chat import ChatMessagePublic
from app.services.openrouter_client import OpenRouterClient


class ChatUseCase:
    """Бизнес-логика взаимодействия с LLM."""

    def __init__(self, chat_repo: ChatMessageRepository, llm_client: OpenRouterClient):
        self.chat_repo = chat_repo
        self.llm_client = llm_client

    async def ask(
        self,
        user_id: int,
        prompt: str,
        system: Optional[str] = None,
        max_history: int = 10,
        temperature: float = 0.7,
    ) -> str:
        """
        Обработать запрос пользователя к LLM.
        Сохраняет запрос и ответ в историю.
        Возвращает ответ модели.
        """
        # 1. Сохраняем запрос пользователя
        await self.chat_repo.add_message(user_id, "user", prompt)

        # 2. Формируем сообщения для контекста
        messages = []
        if system:
            messages.append({"role": "system", "content": system})

        # Получаем последние сообщения из истории (включая только что сохранённое)
        history = await self.chat_repo.get_last_messages(user_id, max_history)
        for msg in history:
            messages.append({"role": msg.role, "content": msg.content})

        # 3. Запрос к LLM
        answer = await self.llm_client.chat_completion(messages, temperature)

        # 4. Сохраняем ответ модели
        await self.chat_repo.add_message(user_id, "assistant", answer)

        return answer

    async def get_history(self, user_id: int) -> List[ChatMessagePublic]:
        """Получить полную историю диалога пользователя."""
        messages = await self.chat_repo.get_all_messages(user_id)
        return [
            ChatMessagePublic(
                id=m.id,
                role=m.role,
                content=m.content,
                created_at=m.created_at.isoformat(),
            )
            for m in messages
        ]

    async def clear_history(self, user_id: int) -> int:
        """Очистить всю историю пользователя."""
        return await self.chat_repo.delete_all_messages(user_id)