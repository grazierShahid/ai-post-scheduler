from sqlalchemy import Column, String, Integer, BigInteger, Boolean, DateTime, Text, JSON, Numeric, Enum as SQLEnum, ForeignKey
from sqlalchemy.orm import relationship
from sqlalchemy import func
import enum
from typing import Optional
from datetime import datetime

from .base_model import BaseModel
from .enums import ImageType


class Image(BaseModel):
    __tablename__ = "images"

    type = Column(SQLEnum(ImageType), nullable=False)
    path = Column(String(512), nullable=False)

    # Relationships
    posts = relationship("Post", back_populates="image")
    products = relationship("Product", back_populates="image")

