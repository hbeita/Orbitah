import os
import sys

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

def test_create_user(client):
    response = client.post("/users/", json={
        "username": "testuser",
        "email": "test@example.com",
        "password": "testpass123"
    })
    assert response.status_code == 200
    data = response.json()
    assert data["username"] == "testuser"
    assert data["email"] == "test@example.com"
    assert "id" in data

def test_get_user(client):
    response = client.get("/users/")
    assert response.status_code == 200
    data = response.json()
    assert isinstance(data, list)
    assert len(data) > 0
    user_id = data[0]["id"]
    response = client.get(f"/users/{user_id}")
    assert response.status_code == 200
    user = response.json()
    assert user["id"] == user_id

def test_update_user(client):
    response = client.get("/users/")
    user_id = response.json()[0]["id"]
    response = client.put(f"/users/{user_id}", json={"username": "updateduser"})
    assert response.status_code == 200
    data = response.json()
    assert data["username"] == "updateduser"

def test_delete_user(client):
    response = client.get("/users/")
    user_id = response.json()[0]["id"]
    response = client.delete(f"/users/{user_id}")
    assert response.status_code == 200
    response = client.get(f"/users/{user_id}")
    assert response.status_code == 404
