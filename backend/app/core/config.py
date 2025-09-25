from pydantic_settings import BaseSettings
from typing import Optional

from pathlib import Path

BASE_DIR =  Path(__file__).resolve().parent.parent.parent

class Settings(BaseSettings):
    DB_HOST: str
    DB_PORT: int
    DB_NAME: str
    DB_USER: str
    DB_PASSWORD: str
    DATABASE_URL: Optional[str] = None
    JWT_SECRET_KEY: str
    FRONTEND_URL: str
    CELERY_BROKER_URL: str
    CELERY_RESULT_BACKEND: str
    REDIS_URL: str
    USE_DUMMY_AI_PROVIDER: bool = False
    
    def get_database_url(self) -> str:
        if self.DATABASE_URL:
            return self.DATABASE_URL
        return f"mysql+mysqlconnector://{self.DB_USER}:{self.DB_PASSWORD}@{self.DB_HOST}:{self.DB_PORT}/{self.DB_NAME}"
    
    def get_jwt_secret_key(self) -> str:
        return self.JWT_SECRET_KEY
    
    def get_frontend_url(self) -> str:
        return self.FRONTEND_URL

    
    class Config:
        env_file = ".env"
        extra = "allow"


settings = Settings()