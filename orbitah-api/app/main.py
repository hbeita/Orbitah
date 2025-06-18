from app.database import Base, engine
from app.routers import (achievements, exploration, focus_sessions, goals,
                         groups, users)
from fastapi import FastAPI

# Create all tables
Base.metadata.create_all(bind=engine)

app = FastAPI(title="Orbitah API")

app.include_router(users.router)
app.include_router(groups.router)
app.include_router(goals.router)
app.include_router(exploration.router)
app.include_router(achievements.router)
app.include_router(focus_sessions.router)

@app.get("/")
def root():
    return {"message": "Welcome to the Orbitah API"}
