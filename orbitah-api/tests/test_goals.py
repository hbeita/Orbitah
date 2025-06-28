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
def test_goal_data():
    return {
        "title": "Test Goal",
        "description": "A test goal",
        "target_date": "2024-12-31",
        "status": "active"
    }

def test_create_goal(client, auth_headers, test_goal_data):
    """Test creating a goal"""
    response = client.post("/goals/", json=test_goal_data, headers=auth_headers)
    assert response.status_code == 200
    data = response.json()
    assert data["title"] == test_goal_data["title"]
    assert data["description"] == test_goal_data["description"]

def test_get_goal(client, auth_headers, test_goal_data):
    """Test getting a goal"""
    # Create goal first
    create_response = client.post("/goals/", json=test_goal_data, headers=auth_headers)
    goal_id = create_response.json()["id"]

    # Get the goal
    response = client.get(f"/goals/{goal_id}", headers=auth_headers)
    assert response.status_code == 200
    data = response.json()
    assert data["id"] == goal_id
    assert data["title"] == test_goal_data["title"]

def test_update_goal(client, auth_headers, test_goal_data):
    """Test updating a goal"""
    # Create goal first
    create_response = client.post("/goals/", json=test_goal_data, headers=auth_headers)
    goal_id = create_response.json()["id"]

    # Update the goal
    update_data = {"title": "Updated Goal"}
    response = client.put(f"/goals/{goal_id}", json=update_data, headers=auth_headers)
    assert response.status_code == 200
    data = response.json()
    assert data["title"] == "Updated Goal"

def test_delete_goal(client, auth_headers, test_goal_data):
    """Test deleting a goal"""
    # Create goal first
    create_response = client.post("/goals/", json=test_goal_data, headers=auth_headers)
    goal_id = create_response.json()["id"]

    # Delete the goal
    response = client.delete(f"/goals/{goal_id}", headers=auth_headers)
    assert response.status_code == 200

    # Verify it's deleted
    get_response = client.get(f"/goals/{goal_id}", headers=auth_headers)
    assert get_response.status_code == 404
