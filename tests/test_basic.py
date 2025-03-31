import pytest
from fastapi.testclient import TestClient
from src.main import app

client = TestClient(app)

def test_read_root():
    response = client.get("/")
    assert response.status_code == 200
    assert response.json() == {"message": "Welcome to Jarvis AI"}

def test_chat_endpoint():
    response = client.post(
        "/api/v1/chat",
        json={
            "message": "Hello Jarvis!",
            "conversation_id": None
        }
    )
    assert response.status_code == 200
    assert "response" in response.json() 