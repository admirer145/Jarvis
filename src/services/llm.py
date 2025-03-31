from typing import List, Optional
from transformers import AutoModelForCausalLM, AutoTokenizer
import torch
from src.config.settings import settings

class HuggingFaceLLM:
    def __init__(self):
        self.model_name = settings.MODEL_NAME
        self.settings = settings  # Add settings attribute
        self.tokenizer = AutoTokenizer.from_pretrained(
            self.model_name,
            token=settings.HUGGINGFACE_API_KEY
        )
        self.model = AutoModelForCausalLM.from_pretrained(
            self.model_name,
            token=settings.HUGGINGFACE_API_KEY,
            torch_dtype=torch.float16,
            device_map="auto"
        )
        
    async def generate_response(
        self,
        prompt: str,
        max_length: Optional[int] = None,
        temperature: Optional[float] = None,
        top_p: float = 0.95,
        repetition_penalty: float = 1.15,
    ) -> str:
        """
        Generate a response using the Hugging Face model.
        
        Args:
            prompt: The input prompt
            max_length: Maximum length of the generated response
            temperature: Sampling temperature
            top_p: Top-p sampling parameter
            repetition_penalty: Penalty for repetition
            
        Returns:
            Generated response text
        """
        # Set default values from settings if not provided
        max_length = max_length or settings.MAX_LENGTH
        temperature = temperature or settings.TEMPERATURE
        
        # Prepare the input
        inputs = self.tokenizer(prompt, return_tensors="pt").to(self.model.device)
        
        # Generate response
        with torch.no_grad():
            outputs = self.model.generate(
                **inputs,
                max_length=max_length,
                temperature=temperature,
                top_p=top_p,
                repetition_penalty=repetition_penalty,
                do_sample=True,
                pad_token_id=self.tokenizer.eos_token_id
            )
        
        # Decode and return the response
        response = self.tokenizer.decode(outputs[0], skip_special_tokens=True)
        return response.replace(prompt, "").strip()
    
    async def generate_chat_response(
        self,
        messages: List[dict],
        max_length: Optional[int] = None,
        temperature: Optional[float] = None,
    ) -> str:
        """
        Generate a chat response using the Hugging Face model.
        
        Args:
            messages: List of message dictionaries with 'role' and 'content' keys
            max_length: Maximum length of the generated response
            temperature: Sampling temperature
            
        Returns:
            Generated response text
        """
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
        
        # Generate response
        return await self.generate_response(
            formatted_prompt,
            max_length=max_length,
            temperature=temperature
        )

# Create a singleton instance
llm = HuggingFaceLLM() 