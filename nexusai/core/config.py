"""
NexusAI OS Core Configuration Module.
Handles environment variables and system settings using Pydantic Settings.
"""
from typing import List, Optional
from pydantic import Field
from pydantic_settings import BaseSettings, SettingsConfigDict


class Settings(BaseSettings):
    model_config = SettingsConfigDict(
        env_file=".env",
        env_file_encoding="utf-8",
        extra="ignore"
    )

    # System Identification
    APP_NAME: str = "NexusAI OS"
    APP_ENV: str = "development"
    DEBUG: bool = True
    SECRET_KEY: str = "nexusai-super-secret-key-change-in-production-12345"
    ALGORITHM: str = "HS256"
    ACCESS_TOKEN_EXPIRE_MINUTES: int = 1440

    # Async Database Connection
    DATABASE_URL: str = "sqlite+aiosqlite:///./nexusai.db"

    # Redis & Celery Message Broker
    REDIS_URL: str = "redis://localhost:6379/0"
    CELERY_BROKER_URL: str = "redis://localhost:6379/0"
    CELERY_RESULT_BACKEND: str = "redis://localhost:6379/0"

    # Multi-LLM Provider Configuration (FREE ONLY)
    DEFAULT_LLM_PROVIDER: str = Field(default="gemini", description="Default provider: gemini, ollama, deepseek, qwen, mistral")
    GEMINI_API_KEY: Optional[str] = Field(default=None, description="Free tier Gemini API key")
    GEMINI_MODEL: str = "gemini-2.5-flash"
    OLLAMA_BASE_URL: str = "http://localhost:11434"
    OLLAMA_MODEL: str = "llama3:latest"
    DEEPSEEK_API_KEY: Optional[str] = None
    DEEPSEEK_MODEL: str = "deepseek-coder"
    QWEN_API_KEY: Optional[str] = None
    QWEN_MODEL: str = "qwen-max"

    # Human-in-the-Loop Safety Checkpoints
    ENABLE_HITL_APPROVAL: bool = True
    DESTRUCTIVE_COMMAND_KEYWORDS: List[str] = Field(
        default_factory=lambda: [
            "rm -rf", "drop database", "drop table", "git push --force",
            "docker system prune -a", "truncate", "kubectl delete namespace"
        ]
    )


settings = Settings()
