from typing import List

from sqlalchemy import delete, select
from sqlalchemy.ext.asyncio import AsyncSession

from app.db.models import ChatMessage


class ChatMessageRepository:
    """Репозиторий для работы с сообщениями чата."""

    def __init__(self, session: AsyncSession):
        self._session = session

    async def add_message(self, user_id: int, role: str, content: str) -> ChatMessage:
        """Добавить новое сообщение."""
        message = ChatMessage(user_id=user_id, role=role, content=content)
        self._session.add(message)
        await self._session.commit()
        await self._session.refresh(message)
        return message

    async def get_last_messages(self, user_id: int, limit: int = 10) -> List[ChatMessage]:
        """Получить последние N сообщений пользователя (упорядочены по возрастанию времени)."""
        stmt = (
            select(ChatMessage)
            .where(ChatMessage.user_id == user_id)
            .order_by(ChatMessage.created_at.desc())
            .limit(limit)
        )
        result = await self._session.execute(stmt)
        messages = result.scalars().all()
        # Возвращаем в хронологическом порядке (от старых к новым)
        return list(reversed(messages))

    async def get_all_messages(self, user_id: int) -> List[ChatMessage]:
        """Получить все сообщения пользователя в хронологическом порядке."""
        stmt = (
            select(ChatMessage)
            .where(ChatMessage.user_id == user_id)
            .order_by(ChatMessage.created_at.asc())
        )
        result = await self._session.execute(stmt)
        return list(result.scalars().all())

    async def delete_all_messages(self, user_id: int) -> int:
        """Удалить все сообщения пользователя. Возвращает количество удалённых записей."""
        stmt = delete(ChatMessage).where(ChatMessage.user_id == user_id)
        result = await self._session.execute(stmt)
        await self._session.commit()
        return result.rowcount