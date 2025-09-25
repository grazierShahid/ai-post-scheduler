from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session
from typing import List, Optional
from app.schemas.product import (
    ProductDesignCreateRequest,
    ProductDesignDetailResponse,
    ProductDesignListResponse,
    ProductDesignItem
)
from app.schemas.post import ImageResponse # Import ImageResponse
from app.dependencies import get_db
from app.services.product_customization import ProductDesignService # Renamed service


router = APIRouter()

@router.post("/product-designs", response_model=ProductDesignDetailResponse)
def create_product_design(payload: ProductDesignCreateRequest, db: Session = Depends(get_db)):
    service = ProductDesignService(db)
    design = service.create_design(payload)
    if not design:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Product not found or design creation failed")
    return design

@router.get("/product-designs", response_model=ProductDesignListResponse)
def list_product_designs(user_id: int, db: Session = Depends(get_db)):
    service = ProductDesignService(db)
    items = service.list_designs(user_id)
    return ProductDesignListResponse(items=items, total=len(items))

@router.get("/product-designs/{design_id}", response_model=ProductDesignDetailResponse)
def get_product_design(design_id: int, db: Session = Depends(get_db)):
    service = ProductDesignService(db)
    design = service.get_design(design_id)
    if not design:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Product design not found")
    return design

@router.get("/product-images/{product_id}", response_model=ImageResponse)
def get_product_image(product_id: int, db: Session = Depends(get_db)):
    service = ProductDesignService(db)
    image = service.get_product_image(product_id)
    if not image:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Product image not found")
    return image