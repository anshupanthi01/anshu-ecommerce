from fastapi import FastAPI
from contextlib import asynccontextmanager
from app.database import init_db

# ✅ Lifespan event (recommended way in FastAPI)
@asynccontextmanager
async def lifespan(app: FastAPI):
    # 🚀 Startup:  Create tables
    print("🔄 Connecting to database...")
    init_db()
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

# ✅ Root endpoint
@app.get("/")
def root():
    return {"message": "Welcome to E-Commerce API!  🛒"}

# ✅ Health check endpoint
@app.get("/health")
def health_check():
    return {"status":  "healthy", "database": "connected"}


# ----------------------------------------
# 📦 Include your routers here (later)
# ----------------------------------------
# from app.routers import users, products, categories, cart, orders
# app.include_router(users.router)
# app.include_router(products. router)
# app.include_router(categories.router)
# app.include_router(cart.router)
# app.include_router(orders.router)