from sqlalchemy import create_engine
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker
from app.config import settings


# ✅ Create engine using config
engine = create_engine(settings.DATABASE_URL)

# ✅ Create session factory
SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)

# ✅ Base class for models
Base = declarative_base()


# ✅ Dependency to get database session
def get_db():
    db = SessionLocal()
    try:
        yield db
    finally: 
        db.close()


# ✅ Initialize database (create tables)
def init_db():
    from app.models import User, Product, Category, Cart, CartItem, Order, OrderItem
    Base.metadata.create_all(bind=engine)
    print("✅ All tables created!")