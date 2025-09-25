from pydantic import BaseModel, Field
from typing import Optional, List
from datetime import datetime, timezone
from fastapi import Form, UploadFile, File
import json

from app.schemas.enums import PlatformType, ProductCategory, PostStatus, PostTone
from app.utils.logger import get_logger

logger = get_logger(__name__)

class PostSubmitRequest(BaseModel):
    user_id: int
    content_text: str
    platforms: List[PlatformType]
    product_id: Optional[int] = None
    schedule_time: Optional[datetime] = None
    hashtags: List[str] = Field(default_factory=list)
    target_audience: Optional[str] = None
    call_to_action: Optional[str] = None
    content_tone: PostTone = PostTone.CASUAL
    api_ids: Optional[List[int]] = None # Added api_ids

    @classmethod
    def as_form(
        cls,
        user_id: int = Form(...),
        content_text: str = Form(...),
        platform_list: List[str] = Form(..., alias="platform_list"),
        product_id: Optional[int] = Form(None),
        schedule_time: Optional[str] = Form(None),
        hashtags: str = Form(""),
        target_audience: Optional[str] = Form(None),
        call_to_action: Optional[str] = Form(None),
        content_tone: str = Form("casual"),
        api_ids: str = Form(""), # Added api_ids as string
    ):
        # Parse platforms from "platform_name:id" format
        platforms_parsed = []
        for p_str in platform_list:
            platform_name = p_str.split(':')[0]
            try:
                platforms_parsed.append(PlatformType(platform_name))
            except ValueError:
                pass

        # Parse hashtags from comma-separated string
        hashtags_list = [h.strip() for h in hashtags.split(',') if h.strip()] if hashtags else []
        
        # Parse api_ids from comma-separated string
        api_ids_list = [int(i.strip()) for i in api_ids.split(',') if i.strip()] if api_ids else None

        # Parse schedule_time - handle both with and without seconds
        schedule_time_dt = None
        if schedule_time:
            logger.info(f"Received schedule_time from form: '{schedule_time}'")
            try:
                # The frontend sends a UTC ISO string (e.g., ...Z). Replace Z with +00:00 for python parser
                schedule_time_dt = datetime.fromisoformat(schedule_time.replace("Z", "+00:00"))
            except (ValueError, TypeError):
                logger.warning(f"Could not parse schedule_time: '{schedule_time}'")
                schedule_time_dt = None

        return cls(
            user_id=user_id,
            content_text=content_text,
            platforms=platforms_parsed,
            product_id=product_id,
            schedule_time=schedule_time_dt,
            hashtags=hashtags_list,
            target_audience=target_audience,
            call_to_action=call_to_action,
            content_tone=PostTone(content_tone.lower()),
            api_ids=api_ids_list, # Assign parsed api_ids
        )

def get_post_submit_form(
    user_id: int = Form(...),
    content_text: str = Form(...),
    platform_list: List[str] = Form(..., alias="platform_list"),
    product_id: Optional[int] = Form(None),
    schedule_time: Optional[str] = Form(None),
    hashtags: str = Form(""),
    target_audience: Optional[str] = Form(None),
    call_to_action: Optional[str] = Form(None),
    content_tone: str = Form("casual"),
    api_ids: str = Form(""), # Added api_ids as string
) -> PostSubmitRequest:
    return PostSubmitRequest.as_form(
        user_id=user_id,
        content_text=content_text,
        platform_list=platform_list,
        product_id=product_id,
        schedule_time=schedule_time,
        hashtags=hashtags,
        target_audience=target_audience,
        call_to_action=call_to_action,
        content_tone=content_tone,
        api_ids=api_ids,
    )

class ImageResponse(BaseModel):
    id: int
    path: str

class PostSubmitResData(BaseModel):
    platforms: List[PlatformType]
    product_id: Optional[int] = None
    schedule_time: Optional[datetime] = None
    status: PostStatus
    hashtags: List[str]
    target_audience: Optional[str] = None

class PostSubmitResponse(BaseModel):
    status_code: int
    status_type: str
    message: str
    data: PostSubmitResData

class AISuggestionsRequest(BaseModel):
    user_id: int
    content_text: str
    product_category: Optional[ProductCategory] = None
    platform_types: List[PlatformType]
    target_audience: Optional[str] = None
    brand_tone: PostTone = PostTone.CASUAL

class ContentReview(BaseModel):
    score: int = Field(..., ge=0, le=100)
    suggestions: List[str]

class AISuggestionsResponse(BaseModel):
    hashtag_suggestions: List[str]
    content_review: ContentReview
    optimized_content: str

class AIBestTimeRequest(BaseModel):
    user_id: int
    platform_types: List[PlatformType]
    target_audience: Optional[str] = None

class AIBestTimeResponse(BaseModel):
    suggestions: List[str]

class ProductInfo(BaseModel):
    id: int
    name: str
    category: ProductCategory
    price: float

class PostListItem(BaseModel):
    id: int
    content_text: str
    image: Optional[ImageResponse] = None
    platforms: List[PlatformType]
    product_id: Optional[int] = None
    schedule_time: Optional[datetime] = None
    status: PostStatus
    hashtags: List[str]
    created_at: datetime

class PostListResponse(BaseModel):
    posts: List[PostListItem]
    total: int
    limit: int
    offset: int

class PostDetailResponse(BaseModel):
    id: int
    user_id: int
    content_text: str
    image: Optional[ImageResponse] = None
    platforms: List[PlatformType]
    product: Optional[ProductInfo] = None
    schedule_time: Optional[datetime] = None
    published_at: Optional[datetime] = None
    status: PostStatus
    hashtags: List[str]
    target_audience: Optional[str] = None
    call_to_action: Optional[str] = None
    content_tone: PostTone
    created_at: datetime
    modified_at: datetime
