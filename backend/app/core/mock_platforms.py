from typing import Dict, Optional, Any
import random
import time
from datetime import datetime
import asyncio
from enum import Enum
import json
from app.utils.logger import get_logger

logger = get_logger(__name__)

class PlatformError(Exception):
    """Base exception for platform-related errors"""
    def __init__(self, platform: str, message: str, code: str = None):
        self.platform = platform
        self.message = message
        self.code = code
        super().__init__(f"{platform}: {message} (code: {code})")

class RateLimitError(PlatformError):
    """Raised when rate limit is exceeded"""
    pass

class ValidationError(PlatformError):
    """Raised when content validation fails"""
    pass

class NetworkError(PlatformError):
    """Raised when network/connection issues occur"""
    pass

class MockPlatformResponse:
    def __init__(self, success: bool, data: Optional[Dict] = None, error: Optional[str] = None):
        self.success = success
        self.data = data or {}
        self.error = error
        self.timestamp = datetime.utcnow()

    def to_dict(self) -> Dict:
        return {
            "success": self.success,
            "data": self.data,
            "error": self.error,
            "timestamp": self.timestamp.isoformat()
        }

class BaseMockPlatform:
    def __init__(self, platform_name: str, rate_limit: int = 100, error_rate: float = 0.1):
        self.platform_name = platform_name
        self.rate_limit = rate_limit
        self.error_rate = error_rate
        self.requests_count = 0
        self.last_reset = datetime.utcnow()
        self.logger = get_logger(f"platform.{platform_name.lower()}")

    async def post_content(self, content: Dict[str, Any]) -> MockPlatformResponse:
        try:
            # Log the attempt
            self.logger.info(f"Attempting to post content to {self.platform_name}", 
                           extra={"content": json.dumps(content)})

            # Validate rate limits
            await self._check_rate_limit()
            
            # Validate content
            self._validate_content(content)
            
            # Simulate network latency
            await self._simulate_latency()
            
            # Simulate random failures
            await self._simulate_failures()
            
            # Process the post
            result = await self._process_post(content)
            
            self.logger.info(f"Successfully posted to {self.platform_name}", 
                           extra={"post_id": result.data.get("post_id")})
            
            return result

        except Exception as e:
            self.logger.error(f"Error posting to {self.platform_name}: {str(e)}", 
                            extra={"error_type": type(e).__name__},
                            exc_info=True)
            raise

    async def _check_rate_limit(self):
        current_time = datetime.utcnow()
        if (current_time - self.last_reset).total_seconds() >= 3600:
            self.requests_count = 0
            self.last_reset = current_time

        self.requests_count += 1
        if self.requests_count > self.rate_limit:
            self.logger.warning(f"Rate limit exceeded for {self.platform_name}")
            raise RateLimitError(
                self.platform_name,
                f"Rate limit of {self.rate_limit} requests/hour exceeded",
                "RATE_LIMIT_EXCEEDED"
            )

    def _validate_content(self, content: Dict[str, Any]):
        """Platform-specific content validation"""
        raise NotImplementedError

    async def _simulate_latency(self):
        """Simulate random network latency"""
        latency = random.uniform(0.1, 2.0)
        self.logger.debug(f"Simulating latency of {latency:.2f}s")
        await asyncio.sleep(latency)

    async def _simulate_failures(self):
        """Simulate random failures"""
        if random.random() < self.error_rate:
            error_types = [
                ("Network timeout", NetworkError),
                ("Internal server error", PlatformError),
                ("Service unavailable", NetworkError)
            ]
            error_msg, error_class = random.choice(error_types)
            self.logger.error(f"Simulated error: {error_msg}")
            raise error_class(self.platform_name, error_msg, "SIMULATED_ERROR")

    async def _process_post(self, content: Dict[str, Any]) -> MockPlatformResponse:
        """Process the post and return response"""
        raise NotImplementedError

class TwitterMock(BaseMockPlatform):
    def __init__(self):
        super().__init__("Twitter", rate_limit=300, error_rate=0.05)

    def _validate_content(self, content: Dict[str, Any]):
        text = content.get("text", "")
        if len(text) > 280:
            raise ValidationError(
                self.platform_name,
                f"Text length {len(text)} exceeds maximum of 280 characters",
                "TEXT_TOO_LONG"
            )
        
        if content.get("image") and len(content["text"]) > 260:
            raise ValidationError(
                self.platform_name,
                "Text length with image must not exceed 260 characters",
                "TEXT_TOO_LONG_WITH_IMAGE"
            )

    async def _process_post(self, content: Dict[str, Any]) -> MockPlatformResponse:
        return MockPlatformResponse(
            success=True,
            data={
                "post_id": f"tw_{int(time.time())}_{random.randint(1000, 9999)}",
                "platform": "twitter",
                "text_length": len(content.get("text", "")),
                "has_media": "image" in content
            }
        )

class LinkedInMock(BaseMockPlatform):
    def __init__(self):
        super().__init__("LinkedIn", rate_limit=100, error_rate=0.03)

    def _validate_content(self, content: Dict[str, Any]):
        text = content.get("text", "")
        if len(text) > 3000:
            raise ValidationError(
                self.platform_name,
                f"Text length {len(text)} exceeds maximum of 3000 characters",
                "TEXT_TOO_LONG"
            )

    async def _process_post(self, content: Dict[str, Any]) -> MockPlatformResponse:
        return MockPlatformResponse(
            success=True,
            data={
                "post_id": f"li_{int(time.time())}_{random.randint(1000, 9999)}",
                "platform": "linkedin",
                "content_type": "ARTICLE" if len(content.get("text", "")) > 1300 else "POST",
                "has_media": "image" in content
            }
        )

class FacebookMock(BaseMockPlatform):
    def __init__(self):
        super().__init__("Facebook", rate_limit=200, error_rate=0.04)

    def _validate_content(self, content: Dict[str, Any]):
        text = content.get("text", "")
        if len(text) > 63206:
            raise ValidationError(
                self.platform_name,
                f"Text length {len(text)} exceeds maximum of 63,206 characters",
                "TEXT_TOO_LONG"
            )

    async def _process_post(self, content: Dict[str, Any]) -> MockPlatformResponse:
        return MockPlatformResponse(
            success=True,
            data={
                "post_id": f"fb_{int(time.time())}_{random.randint(1000, 9999)}",
                "platform": "facebook",
                "reach_estimate": random.randint(100, 1000),
                "has_media": "image" in content
            }
        )

class InstagramMock(BaseMockPlatform):
    def __init__(self):
        super().__init__("Instagram", rate_limit=150, error_rate=0.06)

    def _validate_content(self, content: Dict[str, Any]):
        text = content.get("text", "")
        if len(text) > 2200:
            raise ValidationError(
                self.platform_name,
                f"Text length {len(text)} exceeds maximum of 2,200 characters",
                "TEXT_TOO_LONG"
            )
        
        if not content.get("image"):
            raise ValidationError(
                self.platform_name,
                "Image is required for Instagram posts",
                "IMAGE_REQUIRED"
            )

    async def _process_post(self, content: Dict[str, Any]) -> MockPlatformResponse:
        return MockPlatformResponse(
            success=True,
            data={
                "post_id": f"ig_{int(time.time())}_{random.randint(1000, 9999)}",
                "platform": "instagram",
                "filter_applied": random.choice(["Normal", "Clarendon", "Gingham", "Moon"]),
                "aspect_ratio": "1:1"
            }
        )

class MockPlatformFactory:
    _instances = {}

    @classmethod
    def get_platform(cls, platform_type: str) -> BaseMockPlatform:
        if platform_type not in cls._instances:
            platform_map = {
                "twitter": TwitterMock,
                "linkedin": LinkedInMock,
                "facebook": FacebookMock,
                "instagram": InstagramMock
            }
            if platform_type not in platform_map:
                raise ValueError(f"Unsupported platform: {platform_type}")
            
            cls._instances[platform_type] = platform_map[platform_type]()
            
        return cls._instances[platform_type]