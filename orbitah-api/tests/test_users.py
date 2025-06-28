import os
import sys
import time

import pytest
from api.database import Base, get_db
from api.main import app
from fastapi.testclient import TestClient
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker

sys.path.append(os.path.join(os.path.dirname(__file__), '../api'))
from api.database import Base, get_db
from api.main import app

SQLALCHEMY_DATABASE_URL = "sqlite:///./test_users.db"
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

@pytest.fixture
def test_user_data():
    timestamp = int(time.time())
    return {
        "username": f"testuser_{timestamp}",
        "email": f"test_{timestamp}@example.com",
        "password": "testpassword123"
    }

@pytest.fixture
def auth_headers(client, test_user_data):
    """Create authenticated user and return headers"""
    # Register user
    client.post("/auth/register", json=test_user_data)

    # Login to get token
    login_data = {
        "email": test_user_data["email"],
        "password": test_user_data["password"]
    }
    response = client.post("/auth/login", json=login_data)
    token = response.json()["access_token"]

    return {"Authorization": f"Bearer {token}"}

@pytest.fixture
def current_user_id(client, auth_headers):
    """Get the current user's ID"""
    response = client.get("/auth/me", headers=auth_headers)
    return response.json()["id"]

def test_create_user(client, test_user_data):
    """Test creating a user"""
    response = client.post("/users/", json=test_user_data)
    assert response.status_code == 200
    data = response.json()
    assert data["username"] == test_user_data["username"]
    assert data["email"] == test_user_data["email"]
    assert "password" not in data

def test_get_user(client, auth_headers, current_user_id):
    """Test getting a user"""
    response = client.get(f"/users/{current_user_id}", headers=auth_headers)
    assert response.status_code == 200
    data = response.json()
    assert data["id"] == current_user_id

def test_update_user(client, auth_headers, current_user_id):
    """Test updating a user"""
    update_data = {"username": "updated_username"}
    response = client.put(f"/users/{current_user_id}", json=update_data, headers=auth_headers)
    assert response.status_code == 200
    data = response.json()
    assert data["username"] == "updated_username"

def test_delete_user(client, auth_headers, current_user_id):
    """Test deleting a user"""
    response = client.delete(f"/users/{current_user_id}", headers=auth_headers)
    assert response.status_code == 200
    # After deletion, the token becomes invalid since the user no longer exists
    response = client.get(f"/users/{current_user_id}", headers=auth_headers)
    assert response.status_code == 401
