from app.routes.auth import router as auth_router
from app.routes.user import router as user_router
from app.routes.category import router as category_router
from app.routes.product import router as product_router
from app.routes.cart import router as cart_router
from app.routes.order import router as order_router

__all__ = [
    "auth_router",
    "user_router",
    "category_router",
    "product_router",
    "cart_router",
    "order_router",
]