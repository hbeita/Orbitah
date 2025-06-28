import time

import pytest


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
def test_achievement_data():
    return {
        "name": "First Launch",
        "description": "Complete your first space mission",
        "category": "exploration",
        "points": 100,
        "icon": "rocket.png"
    }

def test_create_achievement(client, auth_headers, test_achievement_data):
    """Test creating an achievement"""
    response = client.post("/achievements/", json=test_achievement_data, headers=auth_headers)
    assert response.status_code == 200
    data = response.json()
    assert data["name"] == test_achievement_data["name"]
    assert data["description"] == test_achievement_data["description"]
    assert data["points"] == test_achievement_data["points"]

def test_get_achievement(client, auth_headers, test_achievement_data):
    """Test getting an achievement"""
    # Create achievement first
    create_response = client.post("/achievements/", json=test_achievement_data, headers=auth_headers)
    achievement_id = create_response.json()["id"]

    # Get the achievement
    response = client.get(f"/achievements/{achievement_id}", headers=auth_headers)
    assert response.status_code == 200
    data = response.json()
    assert data["id"] == achievement_id
    assert data["name"] == test_achievement_data["name"]

def test_update_achievement(client, auth_headers, test_achievement_data):
    """Test updating an achievement"""
    # Create achievement first
    create_response = client.post("/achievements/", json=test_achievement_data, headers=auth_headers)
    achievement_id = create_response.json()["id"]

    # Update the achievement
    update_data = {"name": "Updated Achievement", "points": 200}
    response = client.put(f"/achievements/{achievement_id}", json=update_data, headers=auth_headers)
    assert response.status_code == 200
    data = response.json()
    assert data["name"] == "Updated Achievement"
    assert data["points"] == 200

def test_delete_achievement(client, auth_headers, test_achievement_data):
    """Test deleting an achievement"""
    # Create achievement first
    create_response = client.post("/achievements/", json=test_achievement_data, headers=auth_headers)
    achievement_id = create_response.json()["id"]

    # Delete the achievement
    response = client.delete(f"/achievements/{achievement_id}", headers=auth_headers)
    assert response.status_code == 200

    # Verify it's deleted
    get_response = client.get(f"/achievements/{achievement_id}", headers=auth_headers)
    assert get_response.status_code == 404
