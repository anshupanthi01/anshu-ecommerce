from os import getenv
from dotenv import load_dotenv, find_dotenv

# SQLAlchemy sync engine (use future=True for 2.0 style behavior)
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker, declarative_base, Session

# load .env if found (ImportError will propagate if package missing)
load_dotenv(find_dotenv())

DATABASE_URL = getenv("DATABASE_URL")
if not DATABASE_URL:
    raise ValueError(
        "DATABASE_URL not found in environment variables. Create a .env file with DATABASE_URL"
    )

engine = create_engine(
    DATABASE_URL,
    echo=getenv("DEBUG", "false").lower() == "true",
    pool_pre_ping=True,
    pool_size=10,        # tune to your DB server
    max_overflow=20,     # tune to your DB server
    future=True,
)

# Use class_=Session and future=True for the sessionmaker
SessionLocal = sessionmaker(
    bind=engine,
    class_=Session,
    autoflush=False,
    expire_on_commit=False,
    future=True,
)

Base = declarative_base()

# For FastAPI dependency injection:
from typing import Generator

def get_db() -> Generator[Session, None, None]:
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()

def init_db():
    import app.models
    Base.metadata.create_all(bind=engine)
    print("✅ Database tables created successfully!")