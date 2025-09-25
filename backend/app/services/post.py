from typing import List, Optional, Union
from datetime import datetime, timezone
from sqlalchemy.orm import Session
from sqlalchemy import event
import asyncio
import json

from app.models.post import Post
from app.models.image import Image
from app.models.social_platform import SocialPlatform
from app.models.enums import PlatformType, PostStatus, PostTone, ImageType, PostType
from app.schemas.post import (
    PostSubmitRequest, PostSubmitResData, PostSubmitResponse, PostListResponse, PostListItem,
    PostDetailResponse, ImageResponse, AISuggestionsRequest, AISuggestionsResponse, ContentReview,
    AIBestTimeRequest, AIBestTimeResponse
)
from app.crud.post import PostCRUD
from app.crud.image import ImageCRUD
from app.crud.social_platform import SocialPlatformCRUD
from app.crud.api import ApiCRUD
from app.services.ai_providers import AIProviderFactory
from app.services.ai_prompt_factory import (
    create_hashtag_suggestion_prompt, create_content_analysis_prompt, create_best_posting_time_prompt
)
from app.tasks.services.schedule_post import publish_post_task
from app.utils.logger import get_logger

logger = get_logger(__name__)

def _extract_json(response_str: str, expect_type: str = 'dict') -> Optional[dict or list]:
    """Extracts a JSON object or array from a string, even if it's embedded in other text."""
    if expect_type == 'dict':
        start_char, end_char = '{', '}'
    else: # expect_type == 'list'
        start_char, end_char = '[', ']'

    try:
        start_index = response_str.find(start_char)
        end_index = response_str.rfind(end_char)
        
        if start_index != -1 and end_index != -1:
            json_str = response_str[start_index : end_index + 1]
            return json.loads(json_str)
    except (json.JSONDecodeError, TypeError):
        logger.warning(f"Failed to extract or parse JSON from response: {response_str}")
    
    return None

# Orchestrates post business logic: create/list/detail and AI utilities
class PostService:
    def __init__(self, db: Session):
        self.db = db
        self.post_crud = PostCRUD(db)
        self.image_crud = ImageCRUD(db)
        self.platform_crud = SocialPlatformCRUD(db)
        self.api_crud = ApiCRUD(db)
        self.ai_factory = AIProviderFactory(self.api_crud)

    # ... (no changes to _get_or_create_platform and submit methods)
    def _get_or_create_platform(self, user_id: int, platform_type: PlatformType) -> SocialPlatform:
        logger.debug(f"Getting or creating platform {platform_type} for user {user_id}")
        platform = self.platform_crud.get_by_user_and_type(user_id, platform_type)
        if platform:
            return platform
        platform = SocialPlatform(name=platform_type.value.capitalize(), type=platform_type, user_id=user_id)
        self.platform_crud.create(platform)
        return platform

    def submit(self, payload: Union[PostSubmitRequest, dict], image_file_path: Optional[str] = None) -> PostSubmitResponse:
        logger.info("Starting post submission process")
        if isinstance(payload, dict):
            payload = PostSubmitRequest(**payload)

        logger.info(f"Submitting post for user {payload.user_id}")
        
        image_obj: Optional[Image] = None
        if image_file_path:
            logger.info(f"Creating image from file path: {image_file_path}")
            image_obj = Image(type=ImageType.FILE, path=image_file_path)
            self.image_crud.create(image_obj)
        elif getattr(payload, "image_url", None):
            logger.info(f"Creating image from URL: {payload.image_url}")
            image_obj = Image(type=ImageType.URL, path=payload.image_url)
            self.image_crud.create(image_obj)

        logger.info(f"Image object created: {image_obj}")

        platform_ids = [
            self._get_or_create_platform(payload.user_id, p_type).id
            for p_type in payload.platforms
        ]

        content_json = {
            "text": payload.content_text,
            "hashtags": payload.hashtags or [],
            "target_audience": payload.target_audience,
        }
        status_val = PostStatus.SCHEDULED if payload.schedule_time else PostStatus.PUBLISHED
        published_at = None
        if not payload.schedule_time:
            published_at = datetime.now(timezone.utc)
        
        logger.info(f"Creating single post for platform IDs: {platform_ids}")
        post = Post(
            type=PostType.IMAGE if image_obj else PostType.TEXT,
            content_text=content_json,
            content_tone=payload.content_tone,
            platform_ids=platform_ids,
            product_id=payload.product_id,
            image_id=image_obj.id if image_obj else None,
            user_id=payload.user_id,
            schedule_time=payload.schedule_time,
            status=status_val,
            api_ids=payload.api_ids,
            published_at=published_at,
        )
        self.post_crud.create(post)
        logger.info(f"Post created with ID: {post.id}")

        return PostSubmitResponse(
            status_code=200,
            status_type="success",
            message="Post submitted successfully",
            data=PostSubmitResData(
                platforms=payload.platforms,
                product_id=payload.product_id,
                schedule_time=payload.schedule_time,
                status=post.status,
                hashtags=payload.hashtags or [],
                target_audience=payload.target_audience,
            )
        )

    def list(self, limit: int, offset: int) -> PostListResponse:
        items = self.post_crud.list(limit=limit, offset=offset)
        total = self.post_crud.count()
        return PostListResponse(
            posts=[self._to_list_item(p) for p in items],
            total=total,
            limit=limit,
            offset=offset,
        )

    def detail(self, post_id: int) -> Optional[PostDetailResponse]:
        post = self.post_crud.get(post_id)
        if not post:
            return None
        return self._to_detail(post)

    async def suggest_hashtags(self, user_id: int, payload: AISuggestionsRequest) -> AISuggestionsResponse:
        """Generates AI suggestions by running hashtag and analysis prompts concurrently."""
        provider = self.ai_factory.get_provider(user_id)

        hashtag_prompt = create_hashtag_suggestion_prompt(payload.content_text, [p.value for p in payload.platform_types])
        analysis_prompt = create_content_analysis_prompt(payload.content_text)

        logger.info(f"Requesting hashtag and content analysis for user {user_id}")
        try:
            hashtag_response_str, analysis_response_str = await asyncio.gather(
                provider.ask(hashtag_prompt, temperature=0.7, max_tokens=100),
                provider.ask(analysis_prompt, temperature=0.5, max_tokens=200)
            )
        except Exception as e:
            logger.error(f"AI provider failed during asyncio.gather: {e}")
            hashtag_response_str, analysis_response_str = "", ""

        hashtags = _extract_json(hashtag_response_str, expect_type='list') or ["#ai_error"]
        analysis_data = _extract_json(analysis_response_str, expect_type='dict') or {}

        content_review = ContentReview(
            score=analysis_data.get("score", 0),
            suggestions=analysis_data.get("suggestions", ["Could not analyze content."])
        )

        optimized_content = f"{payload.content_text} {' '.join(hashtags[:3])}"

        return AISuggestionsResponse(
            hashtag_suggestions=hashtags,
            content_review=content_review,
            optimized_content=optimized_content,
        )

    async def suggest_best_posting_time(self, payload: AIBestTimeRequest) -> AIBestTimeResponse:
        """Suggests the best time to post based on platform and audience."""
        provider = self.ai_factory.get_provider(payload.user_id)
        prompt = create_best_posting_time_prompt([p.value for p in payload.platform_types], payload.target_audience)

        logger.info(f"Requesting best posting time for user {payload.user_id}")
        response_str = await provider.ask(prompt, temperature=0.6, max_tokens=200)

        data = _extract_json(response_str, expect_type='dict')
        if data and isinstance(data.get("suggestions"), list):
            suggestions = data["suggestions"]
        else:
            suggestions = ["AI response was not in the expected format."]

        return AIBestTimeResponse(suggestions=suggestions)

    # ... (no changes to _to_list_item and _to_detail methods)
    def _to_list_item(self, p: Post) -> PostListItem:
        image = ImageResponse(id=p.image.id, path=p.image.path) if p.image else None
        
        platform_names = []
        if p.platform_ids:
            platforms = self.platform_crud.get_by_ids(p.platform_ids)
            platform_names = [pl.type for pl in platforms]

        return PostListItem(
            id=p.id,
            content_text=p.content_text.get("text") if isinstance(p.content_text, dict) else str(p.content_text),
            image=image,
            platforms=platform_names,
            product_id=p.product_id,
            schedule_time=p.schedule_time,
            status=p.status,
            hashtags=p.content_text.get("hashtags", []) if isinstance(p.content_text, dict) else [],
            created_at=p.created_at,
        )

    def _to_detail(self, p: Post) -> PostDetailResponse:
        image = ImageResponse(id=p.image.id, path=p.image.path) if p.image else None

        platform_names = []
        if p.platform_ids:
            platforms = self.platform_crud.get_by_ids(p.platform_ids)
            platform_names = [pl.type for pl in platforms]

        return PostDetailResponse(
            id=p.id,
            user_id=p.user_id,
            content_text=p.content_text.get("text") if isinstance(p.content_text, dict) else str(p.content_text),
            image=image,
            platforms=platform_names,
            product=None,
            schedule_time=p.schedule_time,
            published_at=p.published_at,
            status=p.status,
            hashtags=p.content_text.get("hashtags", []) if isinstance(p.content_text, dict) else [],
            target_audience=p.content_text.get("target_audience") if isinstance(p.content_text, dict) else None,
            call_to_action=p.content_text.get("call_to_action") if isinstance(p.content_text, dict) else None,
            content_tone=p.content_tone,
            created_at=p.created_at,
            modified_at=p.modified_at,
        )