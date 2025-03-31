from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import select
from src.models.database.conversation import Conversation, Message

async def get_conversation_history(db: AsyncSession, conversation_id: str):
    if not conversation_id:
        return []
    
    query = select(Message).where(Message.conversation_id == conversation_id)
    result = await db.execute(query)
    messages = result.scalars().all()
    return [{"role": msg.role, "content": msg.content} for msg in messages]

async def store_conversation(
    db: AsyncSession,
    user_id: int,
    user_message: str,
    assistant_response: str,
    conversation_id: str = None
) -> str:
    if not conversation_id:
        conversation = Conversation(user_id=user_id, title=user_message[:50])
        db.add(conversation)
        await db.commit()
        conversation_id = str(conversation.id)
    
    # Store user message
    user_msg = Message(
        conversation_id=conversation_id,
        role="user",
        content=user_message
    )
    db.add(user_msg)
    
    # Store assistant response
    assistant_msg = Message(
        conversation_id=conversation_id,
        role="assistant",
        content=assistant_response
    )
    db.add(assistant_msg)
    
    await db.commit()
    return conversation_id 