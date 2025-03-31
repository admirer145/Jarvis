from fastapi import APIRouter, Depends, HTTPException, status
from typing import List, Optional
from pydantic import BaseModel
from src.services.llm import llm
from src.core.security import get_current_user
from src.models.database.user import User
import torch
from transformers import TextIteratorStreamer
from threading import Thread

router = APIRouter()

class Message(BaseModel):
    role: str
    content: str

class ChatRequest(BaseModel):
    messages: List[Message]
    max_length: Optional[int] = None
    temperature: Optional[float] = None

class ChatResponse(BaseModel):
    response: str
    model: str

@router.post("/chat", response_model=ChatResponse)
async def chat(
    request: ChatRequest,
    current_user: User = Depends(get_current_user)
):
    """
    Chat endpoint that uses the Hugging Face LLM.
    
    Args:
        request: Chat request containing messages and optional parameters
        current_user: Current authenticated user
        
    Returns:
        ChatResponse containing the model's response
    """
    try:
        # Convert Pydantic models to dictionaries
        messages = [msg.model_dump() for msg in request.messages]
        
        # Generate response
        response = await llm.generate_chat_response(
            messages=messages,
            max_length=request.max_length,
            temperature=request.temperature
        )
        
        return ChatResponse(
            response=response,
            model=llm.model_name
        )
        
    except Exception as e:
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=f"Error generating response: {str(e)}"
        )

@router.post("/chat/stream", response_model=ChatResponse)
async def chat_stream(
    request: ChatRequest,
    current_user: User = Depends(get_current_user)
):
    """
    Streaming chat endpoint that uses the Hugging Face LLM.
    
    Args:
        request: Chat request containing messages and optional parameters
        current_user: Current authenticated user
        
    Returns:
        Streaming response from the model
    """
    try:
        # Convert Pydantic models to dictionaries
        messages = [msg.model_dump() for msg in request.messages]
        
        # Format the conversation history
        formatted_prompt = ""
        for msg in messages:
            role = msg["role"]
            content = msg["content"]
            if role == "system":
                formatted_prompt += f"System: {content}\n"
            elif role == "user":
                formatted_prompt += f"Human: {content}\n"
            elif role == "assistant":
                formatted_prompt += f"Assistant: {content}\n"
        
        # Add the current prompt
        formatted_prompt += "Assistant:"
        
        # Prepare the input
        inputs = llm.tokenizer(formatted_prompt, return_tensors="pt").to(llm.model.device)
        
        # Generate streaming response
        with torch.no_grad():
            streamer = TextIteratorStreamer(
                llm.tokenizer,
                skip_prompt=True,
                skip_special_tokens=True,
                timeout=10
            )
            
            generation_kwargs = dict(
                **inputs,
                max_length=request.max_length or llm.settings.MAX_LENGTH,
                temperature=request.temperature or llm.settings.TEMPERATURE,
                top_p=0.95,
                repetition_penalty=1.15,
                do_sample=True,
                pad_token_id=llm.tokenizer.eos_token_id,
                streamer=streamer
            )
            
            # Start generation in a separate thread
            thread = Thread(target=llm.model.generate, kwargs=generation_kwargs)
            thread.start()
            
            # Yield the generated text
            for text in streamer:
                yield text
                
    except Exception as e:
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=f"Error generating streaming response: {str(e)}"
        ) 