import pytest
from app.database import Base, get_db
from app.main import app
from fastapi.testclient import TestClient
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker

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

def test_create_achievement(client):
    response = client.post("/achievements/", json={
        "code": "first_launch",
        "name": "First Launch",
        "description": "Complete your first daily goal.",
        "icon": "🚀",
        "xp_reward": 25
    })
    assert response.status_code == 200
    data = response.json()
    assert data["code"] == "first_launch"
    assert data["name"] == "First Launch"
    assert "id" in data

def test_get_achievement(client):
    response = client.get("/achievements/")
    assert response.status_code == 200
    data = response.json()
    assert isinstance(data, list)
    assert len(data) > 0
    achievement_id = data[0]["id"]
    response = client.get(f"/achievements/{achievement_id}")
    assert response.status_code == 200
    achievement = response.json()
    assert achievement["id"] == achievement_id

def test_update_achievement(client):
    response = client.get("/achievements/")
    achievement_id = response.json()[0]["id"]
    response = client.put(f"/achievements/{achievement_id}", json={"name": "Updated Achievement"})
    assert response.status_code == 200
    data = response.json()
    assert data["name"] == "Updated Achievement"

def test_delete_achievement(client):
    response = client.get("/achievements/")
    achievement_id = response.json()[0]["id"]
    response = client.delete(f"/achievements/{achievement_id}")
    assert response.status_code == 200
    response = client.get(f"/achievements/{achievement_id}")
    assert response.status_code == 404
