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
def test_group_data():
    return {
        "name": "Test Group",
        "description": "A test group",
        "is_public": True
    }

def test_create_group(client, auth_headers, test_group_data):
    """Test creating a group"""
    response = client.post("/groups/", json=test_group_data, headers=auth_headers)
    assert response.status_code == 200
    data = response.json()
    assert data["name"] == test_group_data["name"]
    assert data["description"] == test_group_data["description"]

def test_get_group(client, auth_headers, test_group_data):
    """Test getting a group"""
    # Create group first
    create_response = client.post("/groups/", json=test_group_data, headers=auth_headers)
    group_id = create_response.json()["id"]

    # Get the group
    response = client.get(f"/groups/{group_id}", headers=auth_headers)
    assert response.status_code == 200
    data = response.json()
    assert data["id"] == group_id
    assert data["name"] == test_group_data["name"]

def test_update_group(client, auth_headers, test_group_data):
    """Test updating a group"""
    # Create group first
    create_response = client.post("/groups/", json=test_group_data, headers=auth_headers)
    group_id = create_response.json()["id"]

    # Update the group
    update_data = {"name": "Updated Group"}
    response = client.put(f"/groups/{group_id}", json=update_data, headers=auth_headers)
    assert response.status_code == 200
    data = response.json()
    assert data["name"] == "Updated Group"

def test_delete_group(client, auth_headers, test_group_data):
    """Test deleting a group"""
    # Create group first
    create_response = client.post("/groups/", json=test_group_data, headers=auth_headers)
    group_id = create_response.json()["id"]

    # Delete the group
    response = client.delete(f"/groups/{group_id}", headers=auth_headers)
    assert response.status_code == 200

    # Verify it's deleted
    get_response = client.get(f"/groups/{group_id}", headers=auth_headers)
    assert get_response.status_code == 404
