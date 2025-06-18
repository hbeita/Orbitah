import os
import sys

import pytest
from api.database import Base, get_db
from api.main import api
from fastapi.testclient import TestClient
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker

sys.path.append(os.path.join(os.path.dirname(__file__), '../api'))
from api.database import Base, get_db
from api.main import api

SQLALCHEMY_DATABASE_URL = "sqlite:///./test_test.db"
engine = create_engine(SQLALCHEMY_DATABASE_URL, connect_args={"check_same_thread": False})
TestingSessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)

@pytest.fixture(scope="module")
def test_db():
    Base.metadata.create_all(bind=engine)
    db = TestingSessionLocal()
    try:
        yield db
    finally:
        db.close()
    Base.metadata.drop_all(bind=engine)

@pytest.fixture(scope="module")
def client(test_db):
    def override_get_db():
        try:
            yield test_db
        finally:
            pass
    api.dependency_overrides[get_db] = override_get_db
    with TestClient(api) as c:
        yield c

def test_create_exploration_state(client):
    response = client.post("/exploration/", json={
        "user_id": "user-uuid",
        "unlocked_locations": ["Planet Earth"],
        "current_location": "Planet Earth",
        "lore_progress": "chapter_1",
        "achievements": ["first_launch"]
    })
    assert response.status_code == 200
    data = response.json()
    assert data["user_id"] == "user-uuid"
    assert "Planet Earth" in data["unlocked_locations"]

def test_get_exploration_state(client):
    response = client.get("/exploration/user-uuid")
    assert response.status_code == 200
    data = response.json()
    assert data["user_id"] == "user-uuid"

def test_update_exploration_state(client):
    response = client.put("/exploration/user-uuid", json={"current_location": "Moon Base"})
    assert response.status_code == 200
    data = response.json()
    assert data["current_location"] == "Moon Base"

def test_delete_exploration_state(client):
    response = client.delete("/exploration/user-uuid")
    assert response.status_code == 200
    response = client.get("/exploration/user-uuid")
    assert response.status_code == 404
