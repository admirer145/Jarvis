from langchain.chat_models import ChatOpenAI
from langchain.schema import HumanMessage, SystemMessage, AIMessage
from src.config.settings import settings
from src.services.memory_service import MemoryService
from typing import List


class LLMService:
    def __init__(self):
        self.llm = ChatOpenAI(
            temperature=settings.TEMPERATURE,
            model_name=settings.MODEL_NAME,
            openai_api_key=settings.OPENAI_API_KEY
        )
        self.memory_service = MemoryService()
        
    async def generate_response(
        self, 
        user_message: str, 
        user_id: str, 
        conversation_history: List[dict] = None
    ) -> str:
        # Retrieve relevant memories
        relevant_memories = await self.memory_service.retrieve_relevant_memories(
            user_id=user_id,
            query=user_message
        )
        
        # Construct the prompt with context
        system_message = self._construct_system_message(relevant_memories)
        messages = [system_message]
        
        # Add conversation history
        if conversation_history:
            for msg in conversation_history:
                if msg["role"] == "user":
                    messages.append(HumanMessage(content=msg["content"]))
                else:
                    messages.append(AIMessage(content=msg["content"]))
        
        # Add current message
        messages.append(HumanMessage(content=user_message))
        
        # Generate response
        response = await self.llm.agenerate([messages])
        response_text = response.generations[0][0].text
        
        # Store the interaction in memory
        await self.memory_service.store_memory(
            user_id=user_id,
            memory=f"User: {user_message}\nAssistant: {response_text}",
            metadata={"user_id": user_id, "type": "conversation"}
        )
        
        return response_text
    
    def _construct_system_message(self, relevant_memories: List[str]) -> SystemMessage:
        memories_text = "\n".join(relevant_memories) if relevant_memories else ""
        return SystemMessage(content=f"""You are Jarvis, a highly capable AI assistant. 
        You have access to the following relevant memories about our interactions:
        
        {memories_text}
        
        Use this context to provide personalized and consistent responses while maintaining
        a helpful and professional demeanor.""") 