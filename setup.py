from setuptools import setup, find_packages

setup(
    name="jarvis-ai",
    version="0.1.0",
    packages=find_packages(),
    install_requires=[
        "fastapi>=0.115.12",
        "uvicorn>=0.34.0",
        "pydantic>=2.4",
        "pydantic-settings>=2.0",
        "python-dotenv>=1.0",
        "langchain>=0.3.22",
        "openai>=1.3",
        "sqlalchemy>=2.0",
        "alembic>=1.15.2",
        "python-jose>=3.3",
        "passlib>=1.7",
        "chromadb>=0.6.3",
        "bcrypt>=4.0.1",
        "python-multipart>=0.0.6",
        "asyncpg>=0.30.0",
        "langchain-community>=0.3.20",
        "aiosqlite>=0.21.0",
        "email-validator>=2.2.0",
    ],
)