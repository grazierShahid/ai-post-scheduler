from typing import Optional, List
from sqlalchemy.orm import Session
from sqlalchemy import asc
from app.models.api import Api
from app.models.enums import ApiType
from app.crud.base import BaseCRUD

class ApiCRUD(BaseCRUD):
    def get_by_user_and_type(self, user_id: int, api_type: ApiType) -> Optional[Api]:
        return (
            self.db.query(Api)
            .filter(Api.user_id == user_id, Api.type == api_type)
            .first()
        )

    def list_by_user(self, user_id: int) -> List[Api]:
        return self.db.query(Api).filter(Api.user_id == user_id).all()

    def get_best_api_by_load(self, user_id: int) -> Optional[Api]:
        """Finds the API with the lowest load for a given user."""
        return (
            self.db.query(Api)
            .filter(Api.user_id == user_id)
            .order_by(asc(Api.load))
            .first()
        )