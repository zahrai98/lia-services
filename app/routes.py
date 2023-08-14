from fastapi import APIRouter, Depends
from product import routes as product_routes

router = APIRouter()

router.include_router(
    product_routes.router,
    dependencies=[],
    prefix="/products",
    tags=["products"]
)