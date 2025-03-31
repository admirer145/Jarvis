from fastapi import APIRouter, Depends, HTTPException
from src.models.chat import ChatRequest, ChatResponse
from src.services.llm_service import LLMService
from src.core.security import get_current_user
from src.models.database.user import User
from sqlalchemy.ext.asyncio import AsyncSession
from src.database.session import get_db
from src.database.conversation import get_conversation_history, store_conversation

router = APIRouter()

@router.post("/chat", response_model=ChatResponse)
async def chat_with_jarvis(
    chat_request: ChatRequest,
    current_user: User = Depends(get_current_user),
    db: AsyncSession = Depends(get_db),
    llm_service: LLMService = Depends(LLMService)
):
    # Get conversation history
    conversation_history = await get_conversation_history(
        db, 
        chat_request.conversation_id
    )
    
    # Generate response
    response = await llm_service.generate_response(
        user_message=chat_request.message,
        user_id=str(current_user.id),
        conversation_history=conversation_history
    )
    
    # Store conversation in database
    conversation_id = await store_conversation(
        db,
        current_user.id,
        chat_request.message,
        response,
        chat_request.conversation_id
    )
    
    return ChatResponse(
        response=response,
        conversation_id=conversation_id
    ) 