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
def test_exploration_data():
    return {
        "current_level": 1,
        "experience_points": 100,
        "discovered_planets": ["Earth", "Mars"],
        "completed_missions": ["mission1", "mission2"],
        "current_planet": "Earth"
    }

def test_create_exploration(client, auth_headers, test_exploration_data):
    """Test creating an exploration state"""
    response = client.post("/exploration/", json=test_exploration_data, headers=auth_headers)
    assert response.status_code == 200
    data = response.json()
    assert data["current_level"] == test_exploration_data["current_level"]
    assert data["experience_points"] == test_exploration_data["experience_points"]
    assert data["discovered_planets"] == test_exploration_data["discovered_planets"]

def test_get_exploration(client, auth_headers, test_exploration_data):
    """Test getting an exploration state"""
    # Create exploration first
    create_response = client.post("/exploration/", json=test_exploration_data, headers=auth_headers)
    exploration_id = create_response.json()["id"]

    # Get the exploration
    response = client.get(f"/exploration/{exploration_id}", headers=auth_headers)
    assert response.status_code == 200
    data = response.json()
    assert data["id"] == exploration_id
    assert data["current_level"] == test_exploration_data["current_level"]

def test_update_exploration(client, auth_headers, test_exploration_data):
    """Test updating an exploration state"""
    # Create exploration first
    create_response = client.post("/exploration/", json=test_exploration_data, headers=auth_headers)
    exploration_id = create_response.json()["id"]

    # Update the exploration
    update_data = {"current_level": 2, "experience_points": 200}
    response = client.put(f"/exploration/{exploration_id}", json=update_data, headers=auth_headers)
    assert response.status_code == 200
    data = response.json()
    assert data["current_level"] == 2
    assert data["experience_points"] == 200

def test_delete_exploration(client, auth_headers, test_exploration_data):
    """Test deleting an exploration state"""
    # Create exploration first
    create_response = client.post("/exploration/", json=test_exploration_data, headers=auth_headers)
    exploration_id = create_response.json()["id"]

    # Delete the exploration
    response = client.delete(f"/exploration/{exploration_id}", headers=auth_headers)
    assert response.status_code == 200

    # Verify it's deleted
    get_response = client.get(f"/exploration/{exploration_id}", headers=auth_headers)
    assert get_response.status_code == 404
