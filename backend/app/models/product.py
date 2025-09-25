from sqlalchemy import Column, String, Integer, BigInteger, Boolean, DateTime, Text, JSON, Numeric, Enum as SQLEnum, ForeignKey
from sqlalchemy.orm import relationship
from sqlalchemy import func
import enum
from typing import Optional
from datetime import datetime

from .base_model import BaseModel
from .enums import ProductCategory


class Product(BaseModel):
    __tablename__ = "products"

    name = Column(String(255), nullable=False)
    description = Column(Text, nullable=True)
    image_id = Column(BigInteger, ForeignKey("images.id"), nullable=True)
    category = Column(SQLEnum(ProductCategory), nullable=False)
    price = Column(Numeric(10, 2), nullable=False)
    user_id = Column(BigInteger, nullable=False)  # should be fk of user table
    sell_count = Column(Integer, default=0)
    available = Column(Boolean, default=True)
    ongoing_order = Column(Integer, default=0)
    comment_id = Column(BigInteger, nullable=True)  # should be fk of comment table
    click = Column(Integer, default=0)

    # Relationships
    image = relationship("Image", back_populates="products")
    posts = relationship("Post", back_populates="product")
    designs = relationship("ProductDesign", back_populates="product", cascade="all, delete-orphan") # New relationship


class ProductDesign(BaseModel):
    __tablename__ = "product_designs"

    user_id = Column(BigInteger, nullable=False) # FK to users table
    product_id = Column(BigInteger, ForeignKey("products.id"), nullable=False)
    custom_text = Column(String(255), nullable=False)
    font_style = Column(String(50), nullable=True, default="Arial") # e.g., "Arial", "Impact"
    text_color = Column(String(20), nullable=True, default="#000000") # e.g., "#RRGGBB"
    text_position_x = Column(Integer, nullable=True, default=0) # X coordinate for text placement
    text_position_y = Column(Integer, nullable=True, default=0) # Y coordinate for text placement
    preview_image_path = Column(String(255), nullable=True) # Path to the generated preview image
    created_at = Column(DateTime(timezone=True), server_default=func.now())
    modified_at = Column(DateTime(timezone=True), server_default=func.now(), onupdate=func.now())

    # Relationships
    product = relationship("Product", back_populates="designs")

