from typing import Annotated, List

from fastapi import APIRouter, Depends, HTTPException, status

from app.api.deps import get_chat_usecase, get_current_user_id
from app.core.errors import ExternalServiceError
from app.schemas.chat import ChatMessagePublic, ChatRequest, ChatResponse
from app.usecases.chat import ChatUseCase

router = APIRouter(prefix="/chat", tags=["Chat"])


@router.post("", response_model=ChatResponse)
async def send_message(
    request: ChatRequest,
    current_user_id: Annotated[int, Depends(get_current_user_id)],
    chat_usecase: Annotated[ChatUseCase, Depends(get_chat_usecase)],
):
    """
    Отправить сообщение LLM и получить ответ.
    Сохраняет диалог в истории.
    """
    try:
        answer = await chat_usecase.ask(
            user_id=current_user_id,
            prompt=request.prompt,
            system=request.system,
            max_history=request.max_history,
            temperature=request.temperature,
        )
        return ChatResponse(answer=answer)
    except ExternalServiceError as e:
        raise HTTPException(
            status_code=status.HTTP_502_BAD_GATEWAY,
            detail=f"LLM service error: {str(e)}",
        )


@router.get("/history", response_model=List[ChatMessagePublic])
async def get_history(
    current_user_id: Annotated[int, Depends(get_current_user_id)],
    chat_usecase: Annotated[ChatUseCase, Depends(get_chat_usecase)],
):
    """Получить полную историю диалога текущего пользователя."""
    return await chat_usecase.get_history(current_user_id)


@router.delete("/history", status_code=status.HTTP_204_NO_CONTENT)
async def clear_history(
    current_user_id: Annotated[int, Depends(get_current_user_id)],
    chat_usecase: Annotated[ChatUseCase, Depends(get_chat_usecase)],
):
    """Очистить всю историю диалога текущего пользователя."""
    await chat_usecase.clear_history(current_user_id)
    return