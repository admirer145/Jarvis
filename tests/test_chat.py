import pytest
from httpx import AsyncClient
from src.main import app

@pytest.mark.asyncio
async def test_chat_endpoint():
    async with AsyncClient(app=app, base_url="http://test") as ac:
        response = await ac.post(
            "/api/v1/chat",
            json={
                "message": "Hello Jarvis!",
                "conversation_id": None
            }
        )
    assert response.status_code == 200
    assert "response" in response.json() 