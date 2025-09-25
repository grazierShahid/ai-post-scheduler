from sqlalchemy.orm import Session
from typing import Optional
from app.models.image import Image
from app.crud.base import BaseCRUD

class ImageCRUD(BaseCRUD):
    def get(self, image_id: int) -> Optional[Image]:
        return self.db.query(Image).filter(Image.id == image_id).first()

    def create(self, image: Image) -> Image:
        return self.commit_and_refresh(image) 