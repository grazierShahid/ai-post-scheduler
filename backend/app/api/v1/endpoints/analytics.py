from fastapi import APIRouter, Depends, Query, HTTPException, status
from sqlalchemy.orm import Session
from typing import Optional
from datetime import datetime

from app.dependencies import get_db
from app.services.analytics import AnalyticsService
from app.schemas.analytics import PostSummaryResponse, AiInsightResponse
from app.models.enums import PlatformType

router = APIRouter()

@router.get("/analytics/posts/summary", response_model=PostSummaryResponse)
def get_posts_summary(
    user_id: Optional[int] = Query(None, description="Filter by user ID"),
    platform_type: Optional[PlatformType] = Query(None, description="Filter by social platform type"),
    start_date: Optional[datetime] = Query(None, description="Filter posts scheduled after this date (UTC)"),
    end_date: Optional[datetime] = Query(None, description="Filter posts scheduled before this date (UTC)"),
    db: Session = Depends(get_db),
):
    service = AnalyticsService(db)
    summary = service.get_post_summary(
        user_id=user_id,
        platform_type=platform_type,
        start_date=start_date,
        end_date=end_date
    )
    return summary

@router.get("/analytics/ai-insight", response_model=AiInsightResponse)
async def get_ai_insight(
    user_id: int = Query(..., description="User ID for AI provider selection"),
    query: Optional[str] = Query(None, description="Optional context for AI insight generation"),
    db: Session = Depends(get_db),
):
    service = AnalyticsService(db)
    insight = await service.get_ai_insight(user_id=user_id, query=query)
    return insight