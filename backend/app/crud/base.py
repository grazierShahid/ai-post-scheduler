from sqlalchemy.orm import Session

from app.core.exceptions import DatabaseException
from app.utils.logger import get_logger

logger = get_logger(__name__)

class BaseCRUD:
    def __init__(self, db: Session):
        self.db = db

    def commit_and_refresh(self, instance):
        try:
            self.db.add(instance)
            self.db.commit()
            self.db.refresh(instance)
            return instance
        except Exception as e:
            logger.error(f"Database operation failed: {e}", exc_info=True)
            self.db.rollback()
            raise DatabaseException(operation="BaseCRUD.commit_and_refresh")
