# Database connection

from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker, declarative_base
import os
from dotenv import load_dotenv

load_dotenv()

# Taking URL from .env, fallback for SQLite
DATABASE_URL = os.getenv("DATABASE_URL", "sqlite:///./test.db")

# connect_args only for SQLite
connect_args = {}
if DATABASE_URL.startswith("sqlite"):
    connect_args = {"check_same_thread": False}

# Engine
engine = create_engine(
    DATABASE_URL,
    connect_args=connect_args,  # work for SQLite
)

# Session
SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)

# Base for models
Base = declarative_base()


# Dependency for FastAPI
def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()
