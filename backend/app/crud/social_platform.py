from sqlalchemy.orm import Session
from typing import Optional, List
from app.models.social_platform import SocialPlatform
from app.models.enums import PlatformType
from app.crud.base import BaseCRUD

class SocialPlatformCRUD(BaseCRUD):
    def get_by_user_and_type(self, user_id: int, platform_type: str) -> Optional[SocialPlatform]:
        return self.db.query(SocialPlatform).filter(
            SocialPlatform.user_id == user_id,
            SocialPlatform.type == platform_type
        ).first()

    def get_by_ids(self, platform_ids: List[int]) -> List[SocialPlatform]:
        """Fetches all social platforms for a given list of IDs."""
        if not platform_ids:
            return []
        return self.db.query(SocialPlatform).filter(SocialPlatform.id.in_(platform_ids)).all()

    def create(self, platform: SocialPlatform) -> SocialPlatform:
        return self.commit_and_refresh(platform) 