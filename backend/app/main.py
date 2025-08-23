# FastAPI app

from fastapi import FastAPI
from app.routes import auth, habits
from app.database import Base, engine

# Create tables
Base.metadata.create_all(bind=engine)

app = FastAPI()

# Include routers
app.include_router(auth.router)
app.include_router(habits.router)