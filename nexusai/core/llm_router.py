"""
Multi-LLM Provider Engine for NexusAI OS.
Provides a unified, provider-agnostic async interface for Gemini 2.5 Flash, Ollama, DeepSeek, Qwen, Mistral, and Phi.
Includes failover fallback strategy and structured output generation.
"""
from abc import ABC, abstractmethod
import json
import logging
from typing import Any, Dict, List, Optional
import httpx

from nexusai.core.config import settings

logger = logging.getLogger("nexusai.llm_router")


class BaseLLMProvider(ABC):
    """Abstract base class for all LLM providers."""

    @abstractmethod
    async def generate_completion(
        self,
        prompt: str,
        system_prompt: Optional[str] = None,
        temperature: float = 0.7,
        max_tokens: int = 2048,
    ) -> str:
        """Generate text completion from the LLM provider."""
        pass


class GeminiProvider(BaseLLMProvider):
    """Gemini 2.5 Flash Free Tier provider via Direct REST API."""

    def __init__(self, api_key: Optional[str] = None, model: str = "gemini-2.5-flash"):
        self.api_key = api_key or settings.GEMINI_API_KEY
        self.model = model
        self.base_url = f"https://generativelanguage.googleapis.com/v1beta/models/{self.model}:generateContent"

    async def generate_completion(
        self,
        prompt: str,
        system_prompt: Optional[str] = None,
        temperature: float = 0.7,
        max_tokens: int = 2048,
    ) -> str:
        if not self.api_key:
            raise ValueError("GEMINI_API_KEY is not configured.")

        url = f"{self.base_url}?key={self.api_key}"
        contents = []
        if system_prompt:
            contents.append({"role": "user", "parts": [{"text": f"System Instructions: {system_prompt}"}]})
            contents.append({"role": "model", "parts": [{"text": "Understood. I will follow your instructions."}]})

        contents.append({"role": "user", "parts": [{"text": prompt}]})

        payload = {
            "contents": contents,
            "generationConfig": {
                "temperature": temperature,
                "maxOutputTokens": max_tokens,
            }
        }

        async with httpx.AsyncClient(timeout=60.0) as client:
            response = await client.post(url, json=payload)
            response.raise_for_status()
            data = response.json()
            try:
                return data["candidates"][0]["content"]["parts"][0]["text"]
            except (KeyError, IndexError) as e:
                raise RuntimeError(f"Unexpected response structure from Gemini API: {data}") from e


class OllamaProvider(BaseLLMProvider):
    """Local open-source provider (Llama 3 / Mistral / Qwen / Phi via Ollama)."""

    def __init__(self, base_url: Optional[str] = None, model: Optional[str] = None):
        self.base_url = base_url or settings.OLLAMA_BASE_URL
        self.model = model or settings.OLLAMA_MODEL

    async def generate_completion(
        self,
        prompt: str,
        system_prompt: Optional[str] = None,
        temperature: float = 0.7,
        max_tokens: int = 2048,
    ) -> str:
        url = f"{self.base_url.rstrip('/')}/api/generate"
        full_prompt = f"System: {system_prompt}\n\nUser: {prompt}" if system_prompt else prompt

        payload = {
            "model": self.model,
            "prompt": full_prompt,
            "stream": False,
            "options": {
                "temperature": temperature,
                "num_predict": max_tokens,
            }
        }

        async with httpx.AsyncClient(timeout=90.0) as client:
            response = await client.post(url, json=payload)
            response.raise_for_status()
            data = response.json()
            return data.get("response", "")


class DeepSeekProvider(BaseLLMProvider):
    """DeepSeek Coder / LLM Provider via OpenAI-compatible endpoint."""

    def __init__(self, api_key: Optional[str] = None, model: str = "deepseek-coder"):
        self.api_key = api_key or settings.DEEPSEEK_API_KEY
        self.model = model

    async def generate_completion(
        self,
        prompt: str,
        system_prompt: Optional[str] = None,
        temperature: float = 0.7,
        max_tokens: int = 2048,
    ) -> str:
        if not self.api_key:
            raise ValueError("DEEPSEEK_API_KEY is not configured.")

        url = "https://api.deepseek.com/chat/completions"
        messages = []
        if system_prompt:
            messages.append({"role": "system", "content": system_prompt})
        messages.append({"role": "user", "content": prompt})

        headers = {"Authorization": f"Bearer {self.api_key}", "Content-Type": "application/json"}
        payload = {
            "model": self.model,
            "messages": messages,
            "temperature": temperature,
            "max_tokens": max_tokens,
        }

        async with httpx.AsyncClient(timeout=60.0) as client:
            response = await client.post(url, headers=headers, json=payload)
            response.raise_for_status()
            data = response.json()
            return data["choices"][0]["message"]["content"]


class MockDevLLMProvider(BaseLLMProvider):
    """Development/Testing fallback mock provider when external services are unconfigured."""

    async def generate_completion(
        self,
        prompt: str,
        system_prompt: Optional[str] = None,
        temperature: float = 0.7,
        max_tokens: int = 2048,
    ) -> str:
        logger.warning("Using MockDevLLMProvider fallback response.")
        return json.dumps({
            "status": "mock_response",
            "message": f"Autonomous NexusAI OS response generated for prompt: {prompt[:50]}...",
            "tasks": [
                {"id": 1, "title": "Setup System Architecture", "agent": "CEO Agent"},
                {"id": 2, "title": "Design Relational Schema", "agent": "Database Agent"},
                {"id": 3, "title": "Generate Async FastAPI Endpoint", "agent": "Developer Agent"}
            ]
        })


class LLMRouter:
    """Dynamic LLM Router with primary selection and automatic failover strategy."""

    def __init__(self):
        self.providers: Dict[str, BaseLLMProvider] = {
            "gemini": GeminiProvider(),
            "ollama": OllamaProvider(),
            "deepseek": DeepSeekProvider(),
            "mock": MockDevLLMProvider(),
        }

    def get_provider(self, provider_name: Optional[str] = None) -> BaseLLMProvider:
        target = provider_name or settings.DEFAULT_LLM_PROVIDER
        return self.providers.get(target.lower(), self.providers["mock"])

    async def generate(
        self,
        prompt: str,
        system_prompt: Optional[str] = None,
        provider_preference: Optional[str] = None,
        temperature: float = 0.7,
    ) -> str:
        """Executes LLM request with priority list and fallback resilience."""
        priority_chain = [
            provider_preference or settings.DEFAULT_LLM_PROVIDER,
            "gemini",
            "ollama",
            "mock"
        ]

        seen = set()
        chain = [p.lower() for p in priority_chain if not (p.lower() in seen or seen.add(p.lower()))]

        for p_name in chain:
            provider = self.providers.get(p_name)
            if not provider:
                continue
            try:
                logger.info(f"Attempting completion with LLM provider: {p_name}")
                return await provider.generate_completion(
                    prompt=prompt,
                    system_prompt=system_prompt,
                    temperature=temperature
                )
            except Exception as exc:
                logger.warning(f"Provider '{p_name}' failed with error: {exc}. Trying next fallback...")

        return await self.providers["mock"].generate_completion(prompt, system_prompt)


llm_router = LLMRouter()
