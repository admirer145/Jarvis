# Jarvis AI

A personal AI assistant with memory capabilities, built with FastAPI and Hugging Face.

## Features

- 🤖 Powered by Hugging Face's Mistral-7B-Instruct model
- 🔒 Secure authentication system
- 💬 Chat interface with streaming support
- 📝 Conversation history
- 🔍 Vector database for memory
- 🚀 FastAPI backend
- 🎯 SQLite database for persistence

## Prerequisites

- Python 3.13+
- Poetry for dependency management
- Hugging Face API key

## Installation

1. Clone the repository:
```bash
git clone https://github.com/admirer145/jarvis.git
cd jarvis
```

2. Install dependencies using Poetry:
```bash
poetry install
```

3. Create a `.env` file in the root directory:
```env
# API Settings
API_V1_PREFIX=/api/v1
PROJECT_NAME=Jarvis AI
DEBUG=true

# Security
SECRET_KEY=your_secret_key_here
ACCESS_TOKEN_EXPIRE_MINUTES=30

# LLM Settings
HUGGINGFACE_API_KEY=your_huggingface_api_key_here
MODEL_NAME=mistralai/Mistral-7B-Instruct-v0.2
TEMPERATURE=0.7
MAX_LENGTH=2048

# Database
DATABASE_URL=sqlite:///./jarvis.db

# Vector Database
VECTOR_DB_PATH=./data/vectordb
```

4. Run database migrations:
```bash
poetry run alembic upgrade head
```

## Usage

1. Start the server:
```bash
poetry run uvicorn src.main:app --reload
```

2. Access the API documentation:
```
http://localhost:8000/docs
```

## API Endpoints

### Authentication
- `POST /api/v1/register` - Register a new user
- `POST /api/v1/token` - Get access token
- `GET /api/v1/me` - Get current user info

### Chat
- `POST /api/v1/chat` - Regular chat endpoint
- `POST /api/v1/chat/stream` - Streaming chat endpoint

### Example Chat Request
```json
{
    "messages": [
        {
            "role": "system",
            "content": "You are a helpful assistant."
        },
        {
            "role": "user",
            "content": "Hello, how are you?"
        }
    ],
    "max_length": 2048,
    "temperature": 0.7
}
```

## Development

1. Install development dependencies:
```bash
poetry install --with dev
```

2. Run tests:
```bash
poetry run pytest
```

3. Format code:
```bash
poetry run black .
poetry run isort .
```

## Project Structure

```
jarvis-ai/
├── alembic/              # Database migrations
├── src/
│   ├── api/             # API routes
│   ├── core/            # Core functionality
│   ├── models/          # Data models
│   ├── services/        # Business logic
│   └── config/          # Configuration
├── tests/               # Test files
├── .env                 # Environment variables
├── pyproject.toml       # Project dependencies
└── README.md           # This file
```

## Contributing

1. Fork the repository
2. Create a feature branch
3. Commit your changes
4. Push to the branch
5. Create a Pull Request

## License

This project is licensed under the MIT License - see the LICENSE file for details. 