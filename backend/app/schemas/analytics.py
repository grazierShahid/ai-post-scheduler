from pydantic import BaseModel
from typing import List, Optional
from datetime import datetime

class PostSummaryResponse(BaseModel):
    total_posts: int
    published_count: int
    scheduled_count: int
    failed_count: int
    draft_count: int
    # Add other statuses if needed

class AiInsightResponse(BaseModel):
    insight_text: str
