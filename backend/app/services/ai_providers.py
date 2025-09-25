from abc import ABC, abstractmethod
from typing import List, Optional, Dict, Any
import httpx
import json
import asyncio
from app.models.api import Api
from app.models.enums import ApiType
from app.crud.api import ApiCRUD
from app.utils.logger import get_logger
from app.core.config import settings

logger = get_logger(__name__)

# Defines the simplified interface for all AI service providers.
class AIProvider(ABC):
    @abstractmethod
    async def ask(self, prompt: str, temperature: float = 0.7, max_tokens: int = 500) -> str:
        """Sends a prompt to the AI and returns the raw text response."""
        ...

# Base class for AI providers, handling common HTTP requests and error handling.
class BaseAIProvider(AIProvider):
    def __init__(self, endpoint: str, access_key: str, secret_key: Optional[str] = None, extra: Optional[Dict[str, Any]] = None):
        self.endpoint = endpoint.rstrip("/")
        self.access_key = access_key
        self.secret_key = secret_key
        self.extra = extra or {}
        self.model = self.extra.get("model", "default-model")

    async def _make_request(self, payload: Dict[str, Any], headers: Dict[str, str], request_url: Optional[str] = None) -> Dict[str, Any]:
        """Makes an async HTTP POST request and handles responses."""
        url = request_url or self.endpoint
        logger.info(f"Making AI request to {url} with model {self.model}")
        async with httpx.AsyncClient(timeout=30) as client:
            try:
                resp = await client.post(url, json=payload, headers=headers)
                resp.raise_for_status()
                logger.info(f"AI request successful with status {resp.status_code}")
                return resp.json()
            except httpx.HTTPStatusError as e:
                logger.error(f"AI request failed with status {e.response.status_code}: {e.response.text}")
                raise
            except httpx.RequestError as e:
                logger.error(f"AI request failed due to a network error: {e}")
                raise

# AI provider for OpenAI models.
class OpenAIProvider(BaseAIProvider):
    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        self.model = self.extra.get("model", "gpt-3.5-turbo")

    async def ask(self, prompt: str, temperature: float = 0.7, max_tokens: int = 500) -> str:
        headers = {"Authorization": f"Bearer {self.access_key}"}
        payload = {
            "model": self.model,
            "messages": [{"role": "user", "content": prompt}],
            "temperature": temperature,
            "max_tokens": max_tokens,
        }
        
        try:
            response = await self._make_request(payload, headers)
            return response.get("choices", [{}])[0].get("message", {}).get("content", "")
        except Exception as e:
            logger.error(f"OpenAI ask failed: {e}")
            return ""

# AI provider for Google Gemini models.
class GeminiProvider(BaseAIProvider):
    async def ask(self, prompt: str, temperature: float = 0.7, max_tokens: int = 500) -> str:
        url = f"{self.endpoint}?key={self.access_key}"
        headers = {"Content-Type": "application/json"}
        payload = {
            "contents": [{"parts": [{"text": prompt}]}],
            "generationConfig": {
                "temperature": temperature,
                "maxOutputTokens": max_tokens,
            }
        }
        
        try:
            response = await self._make_request(payload, headers, request_url=url)
            return response.get("candidates", [{}])[0].get("content", {}).get("parts", [{}])[0].get("text", "")
        except Exception as e:
            logger.error(f"Gemini ask failed: {e}")
            return ""

# AI provider for Grok models.
class GrokProvider(BaseAIProvider):
    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        self.model = self.extra.get("model", "grok-1")

    async def ask(self, prompt: str, temperature: float = 0.7, max_tokens: int = 500) -> str:
        headers = {
            "Authorization": f"Bearer {self.access_key}",
            "Content-Type": "application/json"
        }
        payload = {
            "model": self.model,
            "messages": [{"role": "user", "content": prompt}],
            "temperature": temperature,
            "max_tokens": max_tokens,
        }
        
        try:
            response = await self._make_request(payload, headers)
            return response.get("choices", [{}])[0].get("message", {}).get("content", "")
        except Exception as e:
            logger.error(f"Grok ask failed: {e}")
            return ""

# Dummy provider for frontend development and testing.
class DummyAIProvider(AIProvider):
    async def ask(self, prompt: str, temperature: float = 0.7, max_tokens: int = 500) -> str:
        """Inspects the prompt and returns a mock, schema-compliant response."""
        logger.info(f"--- DUMMY AI PROVIDER --- Answering prompt: {prompt[:100]}...")
        await asyncio.sleep(0.2) # Simulate network latency

        if "hashtag" in prompt.lower():
            return json.dumps(["#dummydata", "#frontendfun", "#fastapi", "#mockresponse"])
        
        if "analyze" in prompt.lower():
            return json.dumps({
                "score": 88,
                "suggestions": ["This is a dummy suggestion.", "Consider adding more details.", "Great start!"]
            })

        if "best time to post" in prompt.lower():
            return json.dumps({
                "suggestions": ["Weekday mornings (9-11 AM) are great.", "Try evenings after 7 PM."]
            })
        
        if "insight" in prompt.lower():
            return "Dummy insight: Posts with images and clear call-to-actions tend to perform best."

        return "This is a generic dummy response from the AI provider."

# Maps API types to their corresponding provider classes.
PROVIDER_MAP = {
    ApiType.OPENAI: OpenAIProvider,
    ApiType.GEMINI: GeminiProvider,
    ApiType.GROK: GrokProvider,
}

# Factory to select the appropriate AI provider based on load.
class AIProviderFactory:
    def __init__(self, api_crud: ApiCRUD):
        self.api_crud = api_crud

    def get_provider(self, user_id: int) -> AIProvider:
        """
        Selects the best AI provider for a user. If USE_DUMMY_AI_PROVIDER is True,
        it returns a dummy provider. Otherwise, it selects the real provider
        with the lowest load.
        """
        if settings.USE_DUMMY_AI_PROVIDER:
            logger.warning(f"DUMMY AI PROVIDER is active. No real API calls will be made.")
            return DummyAIProvider()

        api = self.api_crud.get_best_api_by_load(user_id)
        
        if not api:
            logger.warning(f"No configured AI provider found for user {user_id}. Using fallback.")
            return OpenAIProvider(endpoint="", access_key="", extra={"model": "fallback"})

        provider_class = PROVIDER_MAP.get(api.type)
        
        if not provider_class:
            logger.error(f"Provider for type '{api.type}' not found. Falling back.")
            return OpenAIProvider(endpoint="", access_key="", extra={"model": "fallback"})

        logger.info(f"Using '{api.type.value}' provider for user {user_id} based on lowest load.")
        kwargs = {
            "endpoint": api.endpoint,
            "access_key": api.access_key,
            "secret_key": api.secret_key,
            "extra": api.extra
        }
        return provider_class(**kwargs)