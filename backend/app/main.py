# FastAPI app

import os
from fastapi import FastAPI
from app.routes import auth, habits, track
from app.database import Base, engine
from fastapi.middleware.cors import CORSMiddleware
from prometheus_fastapi_instrumentator import Instrumentator

# Create tables
Base.metadata.create_all(bind=engine)

app = FastAPI()

# Connect instrumentator
Instrumentator().instrument(app).expose(app)

frontend_url = os.environ.get(
    "FRONTEND_URL", "http://localhost:5173"
)  # fallback for local network

app.add_middleware(
    CORSMiddleware,
    allow_origins=[frontend_url, "https://grindly.vercel.app"],  # dynamic origin
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Include routers
app.include_router(auth.router)
app.include_router(habits.router)
app.include_router(track.router)
