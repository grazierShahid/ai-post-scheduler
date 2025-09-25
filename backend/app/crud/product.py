from sqlalchemy.orm import Session, joinedload
from typing import Optional, List
from app.models.product import Product, ProductDesign # Import ProductDesign
from app.crud.base import BaseCRUD

class ProductCRUD(BaseCRUD):
    def get(self, product_id: int) -> Optional[Product]:
        return self.db.query(Product).options(joinedload(Product.image)).filter(Product.id == product_id).first()

    def list_by_user(self, user_id: Optional[int] = None) -> List[Product]:
        q = self.db.query(Product)
        if user_id:
            q = q.filter(Product.user_id == user_id)
        return q.order_by(Product.id).all() # Changed ordering as last_customized_at is removed

    def update(self, product: Product) -> Product:
        return self.commit_and_refresh(product)


class ProductDesignCRUD(BaseCRUD):
    def get(self, design_id: int) -> Optional[ProductDesign]:
        return self.db.query(ProductDesign).filter(ProductDesign.id == design_id).first()

    def list_by_user(self, user_id: int) -> List[ProductDesign]:
        return self.db.query(ProductDesign).filter(ProductDesign.user_id == user_id).order_by(ProductDesign.created_at.desc()).all()

    def create(self, design: ProductDesign) -> ProductDesign:
        self.db.add(design)
        self.db.commit()
        self.db.refresh(design)
        return design
 