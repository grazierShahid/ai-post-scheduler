from pydantic import BaseModel, Field
from typing import Optional, List
from datetime import datetime
from .enums import ProductCategory

class ProductCreate(BaseModel):
    name: str
    category: ProductCategory
    price: float
    image_id: Optional[int] = None
    description: Optional[str] = None

class ProductResponse(BaseModel):
    id: int
    name: str
    category: ProductCategory
    price: float
    image_id: Optional[int] = None
    description: Optional[str] = None

class ProductDesignCreateRequest(BaseModel):
    user_id: int
    product_id: int
    custom_text: str
    font_style: Optional[str] = "Arial"
    text_color: Optional[str] = "#000000"
    text_position_x: Optional[int] = 0
    text_position_y: Optional[int] = 0

class ProductDesignItem(BaseModel):
    id: int
    user_id: int
    product_id: int
    custom_text: str
    font_style: Optional[str] = None
    text_color: Optional[str] = None
    text_position_x: Optional[int] = None
    text_position_y: Optional[int] = None
    preview_image_path: Optional[str] = None
    created_at: datetime
    modified_at: datetime

class ProductDesignListResponse(BaseModel):
    items: List[ProductDesignItem]
    total: int

class ProductDesignDetailResponse(ProductDesignItem):
    # Inherits all fields from ProductDesignItem
    pass