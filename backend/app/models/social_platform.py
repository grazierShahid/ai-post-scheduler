from sqlalchemy import Column, String, Integer, BigInteger, Boolean, DateTime, Text, JSON, Numeric, Enum as SQLEnum, ForeignKey
from sqlalchemy.orm import relationship
from sqlalchemy import func
import enum
from typing import Optional
from datetime import datetime

from .base_model import BaseModel
from .enums import PlatformType, PlatformStatus


class SocialPlatform(BaseModel):
    __tablename__ = "social_platforms"

    name = Column(String(255), nullable=False)
    type = Column(SQLEnum(PlatformType), nullable=False)
    status = Column(SQLEnum(PlatformStatus), default=PlatformStatus.CONNECTED) # as mock setting CONNECTED as default
    api_id = Column(String(255), nullable=True)
    isVerified = Column(Boolean, default=False)
    isActive = Column(Boolean, default=True)
    user_id = Column(BigInteger, nullable=False)



