from sqlalchemy import Column, String, Integer, BigInteger, Boolean, DateTime, Text, JSON, Numeric, Enum as SQLEnum, ForeignKey
from sqlalchemy.orm import relationship
from sqlalchemy import func
import enum
from typing import Optional
from datetime import datetime

from .base_model import BaseModel
from .enums import PostType, PostTone, PostStatus, InsightType


class Post(BaseModel):
    __tablename__ = "posts"

    type = Column(SQLEnum(PostType), nullable=False)
    content_text = Column(JSON, nullable=False)  # main post text
    content_tone = Column(SQLEnum(PostTone), default=PostTone.CASUAL)
    platform_ids = Column(JSON, nullable=False)  # Stores an array of platform identifiers
    product_id = Column(BigInteger, ForeignKey("products.id"), nullable=True)
    image_id = Column(BigInteger, ForeignKey("images.id"), nullable=True)   # post photo, and can be null
    user_id = Column(BigInteger, nullable=False) # this should be a foreign key to users table
    schedule_time = Column(DateTime(timezone=True), server_default=func.now(), nullable=True)
    status = Column(SQLEnum(PostStatus), default=PostStatus.DRAFT)
    published_at = Column(DateTime(timezone=True), nullable=True)
    remarks = Column(Text, nullable=True)
    api_ids = Column(JSON, nullable=True)  # Stores list of API IDs as JSON

    # Relationships
    product = relationship("Product", back_populates="posts")
    image = relationship("Image", back_populates="posts")
    analyses = relationship("PostAnalysis", back_populates="post", cascade="all, delete-orphan")
    insights = relationship("AiInsight", back_populates="post", cascade="all, delete-orphan")


class PostAnalysis(BaseModel):
    __tablename__ = "post_analyses"

    post_id = Column(BigInteger, ForeignKey("posts.id"), nullable=False)
    analysis = Column(JSON, nullable=False)  # Store analysis as JSON
    ai_insight_id = Column(BigInteger, ForeignKey("ai_insights.id"), nullable=True)

    # Relationships
    post = relationship("Post", back_populates="analyses")



class AiInsight(BaseModel):
    __tablename__ = "ai_insights"

    post_id = Column(BigInteger, ForeignKey("posts.id"), nullable=False)
    insight_type = Column(SQLEnum(InsightType), nullable=False)
    insight_text = Column(Text, nullable=False)
    meta_data = Column("metadata", JSON, nullable=True)

    # Relationships
    post = relationship("Post", back_populates="insights")
