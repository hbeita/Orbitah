import os
import sys
from datetime import datetime

import pytest
from fastapi.testclient import TestClient
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker

sys.path.append(os.path.join(os.path.dirname(__file__), '../app'))
from app.database import Base, get_db
from app.main import app

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
    app.dependency_overrides[get_db] = override_get_db
    with TestClient(app) as c:
        yield c

def test_create_goal(client):
    response = client.post("/goals/", json={
        "title": "Test Goal",
        "description": "Test description",
        "type": "daily",
        "status": "pending",
        "creator_id": "user-uuid",
        "category": "work",
        "created_by_ai": False,
        "created_at": datetime.utcnow().isoformat(),
        "due_date": datetime.utcnow().date().isoformat(),
        "rewards_xp": 10
    })
    assert response.status_code == 200
    data = response.json()
    assert data["title"] == "Test Goal"
    assert "id" in data

def test_get_goal(client):
    response = client.get("/goals/")
    assert response.status_code == 200
    data = response.json()
    assert isinstance(data, list)
    assert len(data) > 0
    goal_id = data[0]["id"]
    response = client.get(f"/goals/{goal_id}")
    assert response.status_code == 200
    goal = response.json()
    assert goal["id"] == goal_id

def test_update_goal(client):
    response = client.get("/goals/")
    goal_id = response.json()[0]["id"]
    response = client.put(f"/goals/{goal_id}", json={"title": "Updated Goal"})
    assert response.status_code == 200
    data = response.json()
    assert data["title"] == "Updated Goal"

def test_delete_goal(client):
    response = client.get("/goals/")
    goal_id = response.json()[0]["id"]
    response = client.delete(f"/goals/{goal_id}")
    assert response.status_code == 200
    response = client.get(f"/goals/{goal_id}")
    assert response.status_code == 404
