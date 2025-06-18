from api.database import Base, engine
from api.routers import (achievements, exploration, focus_sessions, goals,
                         groups, users)
from fastapi import FastAPI

# Create all tables
Base.metadata.create_all(bind=engine)

api = FastAPI(title="Orbitah API")

api.include_router(users.router)
api.include_router(groups.router)
api.include_router(goals.router)
api.include_router(exploration.router)
api.include_router(achievements.router)
api.include_router(focus_sessions.router)

@api.get("/")
def root():
    return {"message": "Welcome to the Orbitah API"}
