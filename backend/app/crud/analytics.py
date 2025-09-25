from sqlalchemy.orm import Session
from sqlalchemy import func
from typing import Dict, Optional
from datetime import datetime

from app.models.post import Post
from app.models.social_platform import SocialPlatform # Import SocialPlatform for join
from app.models.enums import PostStatus, PlatformType
from app.crud.base import BaseCRUD

class AnalyticsCRUD(BaseCRUD):
    def get_post_counts_by_status(
        self,
        user_id: Optional[int] = None,
        platform_type: Optional[PlatformType] = None,
        start_date: Optional[datetime] = None,
        end_date: Optional[datetime] = None
    ) -> Dict[PostStatus, int]:
        query = self.db.query(Post.status, func.count(Post.id))

        if user_id:
            query = query.filter(Post.user_id == user_id)
        
        if platform_type:
            query = query.join(SocialPlatform).filter(SocialPlatform.type == platform_type)

        if start_date:
            query = query.filter(Post.schedule_time >= start_date)
        if end_date:
            query = query.filter(Post.schedule_time <= end_date)

        results = query.group_by(Post.status).all()
        
        # Initialize all possible statuses to 0 to ensure all are present in the response
        counts = {status: 0 for status in PostStatus}
        for status, count in results:
            counts[status] = count
            
        return counts
