from fastapi import FastAPI
from contextlib import asynccontextmanager
from app.database import init_db
from app.config import settings
from fastapi.staticfiles import StaticFiles

print("CURRENT SECRET_KEY:", settings.SECRET_KEY)

# ✅ Import all routers
from app.routes import (
    auth_router,
    user_router,
    category_router,
    product_router,
    cart_router,
    order_router,
)

from fastapi.middleware.cors import CORSMiddleware

# ✅ Lifespan event (recommended way in FastAPI)
@asynccontextmanager
async def lifespan(app: FastAPI):
    # 🚀 Startup:  Create tables
    print("🔄 Connecting to database...")
    init_db()
    print("✅ Database connected!")
    yield
    # 🛑 Shutdown:  Cleanup (if needed)
    print("👋 Shutting down...")

# ✅ Create FastAPI app with lifespan
app = FastAPI(
    title="E-Commerce API",
    description="College E-Commerce Project",
    version="1.0.0",
    lifespan=lifespan
)

app.mount("/static", StaticFiles(directory="static"), name="static")

# ✅ Add CORS middleware AFTER the app is created!
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],           # For local dev, allow everything. Use only your frontend's domain in production!
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# ✅ Root endpoint
@app.get("/")
def root():
    return {"message": "Welcome to E-Commerce API!  🛒"}

# ✅ Health check endpoint
@app.get("/health")
def health_check():
    return {"status": "healthy", "database":  "connected"}

# ----------------------------------------
# 📦 Include all routers
# ----------------------------------------

app.include_router(
    auth_router,
    prefix="/api/auth",
    tags=["Authentication"]
)

app.include_router(
    user_router,
    prefix="/api/users",
    tags=["Users"]
)

app.include_router(
    category_router,
    prefix="/api/categories",
    tags=["Categories"]
)

app.include_router(
    product_router,
    prefix="/api/products",
    tags=["Products"]
)

app.include_router(
    cart_router,
    prefix="/api/cart",
    tags=["Cart"]
)

app.include_router(
    order_router,
    prefix="/api/orders",
    tags=["Orders"]
)