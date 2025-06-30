import os

from api.database import Base, engine
from api.routers import (achievements, auth, exploration, focus_sessions,
                         goals, groups, users)
from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from fastapi.middleware.trustedhost import TrustedHostMiddleware

# Create all tables
Base.metadata.create_all(bind=engine)

app = FastAPI(title="Orbitah API")

# Security middleware for production
if os.getenv("ENVIRONMENT") == "production":
    app.add_middleware(
        TrustedHostMiddleware,
        allowed_hosts=["yourdomain.com"]  # Single domain for Option A
    )

# CORS configuration - production ready
origins = [
    "http://localhost:5173",  # Frontend dev server
    "http://127.0.0.1:5173",  # Frontend dev server alternative
    "http://localhost:3001",  # Alternative dev port
]

# Add production origins from environment variable
if os.getenv("FRONTEND_URL"):
    origins.append(os.getenv("FRONTEND_URL"))

# Add CORS middleware
app.add_middleware(
    CORSMiddleware,
    allow_origins=origins,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

app.include_router(auth.router)
app.include_router(users.router)
app.include_router(groups.router)
app.include_router(goals.router)
app.include_router(exploration.router)
app.include_router(achievements.router)
app.include_router(focus_sessions.router)

@app.get("/")
def root():
    return {"message": "Welcome to the Orbitah API"}
