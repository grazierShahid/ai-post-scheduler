from fastapi import APIRouter
from app.api.v1.endpoints import post as post_endpoints
from app.api.v1.endpoints import product_customization as product_endpoints
from app.api.v1.endpoints import analytics as analytics_endpoints


api_router = APIRouter()

api_router.include_router(post_endpoints.router, tags=["Post"])
api_router.include_router(product_endpoints.router, tags=["Product"])
api_router.include_router(analytics_endpoints.router, tags=["Analytics"])
