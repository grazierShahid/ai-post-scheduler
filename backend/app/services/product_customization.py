from typing import List, Optional
from datetime import datetime, timezone
from sqlalchemy.orm import Session
import os

from app.models.product import Product, ProductDesign
from app.crud.product import ProductCRUD, ProductDesignCRUD
from app.schemas.product import ProductDesignCreateRequest, ProductDesignDetailResponse, ProductDesignItem
from app.schemas.post import ImageResponse # Import ImageResponse
from app.utils.image_manipulation import overlay_text_on_image
from app.utils.logger import get_logger

logger = get_logger(__name__)

class ProductDesignService:
    def __init__(self, db: Session):
        self.db = db
        self.product_crud = ProductCRUD(db)
        self.product_design_crud = ProductDesignCRUD(db)

    def create_design(self, payload: ProductDesignCreateRequest) -> Optional[ProductDesignDetailResponse]:
        product = self.product_crud.get(payload.product_id)
        if not product:
            logger.warning(f"Product with ID {payload.product_id} not found for design creation.")
            return None

        # Generate preview image
        preview_image_path = None
        if product.image and product.image.path:
            # Define output path for the customized image
            # Example: static/uploads/user_id/product_id/design_id_timestamp.jpg
            output_dir = os.path.join("static", "uploads", str(payload.user_id), str(payload.product_id))
            os.makedirs(output_dir, exist_ok=True)
            timestamp = datetime.now().strftime("%Y%m%d%H%M%S")
            preview_image_filename = f"design_{product.id}_{timestamp}.jpg"
            preview_image_path = os.path.join(output_dir, preview_image_filename)

            try:
                overlay_text_on_image(
                    base_image_path=product.image.path,
                    text=payload.custom_text,
                    font_style=payload.font_style,
                    text_color=payload.text_color,
                    position_x=payload.text_position_x,
                    position_y=payload.text_position_y,
                    output_path=preview_image_path
                )
                logger.info(f"Generated preview image: {preview_image_path}")
            except Exception as e:
                logger.error(f"Error generating preview image for product {product.id}: {e}")
                preview_image_path = None # Reset if generation fails

        design = ProductDesign(
            user_id=payload.user_id,
            product_id=payload.product_id,
            custom_text=payload.custom_text,
            font_style=payload.font_style,
            text_color=payload.text_color,
            text_position_x=payload.text_position_x,
            text_position_y=payload.text_position_y,
            preview_image_path=preview_image_path
        )
        created_design = self.product_design_crud.create(design)
        logger.info(f"Product design created with ID: {created_design.id}")

        return ProductDesignDetailResponse(
            id=created_design.id,
            user_id=created_design.user_id,
            product_id=created_design.product_id,
            custom_text=created_design.custom_text,
            font_style=created_design.font_style,
            text_color=created_design.text_color,
            text_position_x=created_design.text_position_x,
            text_position_y=created_design.text_position_y,
            preview_image_path=created_design.preview_image_path,
            created_at=created_design.created_at,
            modified_at=created_design.modified_at,
        )

    def list_designs(self, user_id: int) -> List[ProductDesignItem]:
        designs = self.product_design_crud.list_by_user(user_id)
        return [
            ProductDesignItem(
                id=d.id,
                user_id=d.user_id,
                product_id=d.product_id,
                custom_text=d.custom_text,
                font_style=d.font_style,
                text_color=d.text_color,
                text_position_x=d.text_position_x,
                text_position_y=d.text_position_y,
                preview_image_path=d.preview_image_path,
                created_at=d.created_at,
                modified_at=d.modified_at,
            ) for d in designs
        ]

    def get_design(self, design_id: int) -> Optional[ProductDesignDetailResponse]:
        design = self.product_design_crud.get(design_id)
        if not design:
            logger.warning(f"Product design with ID {design_id} not found.")
            return None
        return ProductDesignDetailResponse(
            id=design.id,
            user_id=design.user_id,
            product_id=design.product_id,
            custom_text=design.custom_text,
            font_style=design.font_style,
            text_color=design.text_color,
            text_position_x=design.text_position_x,
            text_position_y=design.text_position_y,
            preview_image_path=design.preview_image_path,
            created_at=design.created_at,
            modified_at=design.modified_at,
        )

    def get_product_image(self, product_id: int) -> Optional[ImageResponse]:
        """Fetches a product by ID and returns its associated image details."""
        product = self.product_crud.get(product_id)
        if not product or not product.image:
            logger.warning(f"Product with ID {product_id} or its image not found.")
            return None
        return ImageResponse(id=product.image.id, path=product.image.path)