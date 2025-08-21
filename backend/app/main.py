# FastAPI app

from fastapi import FastAPI
from app.routes import auth
from app.database import Base, engine

# Create tables
Base.metadata.create_all(bind=engine)

app = FastAPI()
app.include_router(auth.router)