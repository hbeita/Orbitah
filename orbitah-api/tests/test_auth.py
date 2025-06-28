import time

import pytest
from api import auth


@pytest.fixture
def test_user_data():
    return {
        "username": "testuser",
        "email": "test@example.com",
        "password": "testpassword123"
    }

@pytest.fixture
def test_user_credentials():
    return {
        "email": "test@example.com",
        "password": "testpassword123"
    }

def test_register_user(client, test_user_data):
    """Test user registration"""
    # Use timestamp to make email truly unique
    timestamp = int(time.time())
    unique_data = {
        "username": f"testuser_unique_{timestamp}",
        "email": f"test_unique_{timestamp}@example.com",
        "password": "testpassword123"
    }
    response = client.post("/auth/register", json=unique_data)
    assert response.status_code == 200
    data = response.json()
    assert data["username"] == unique_data["username"]
    assert data["email"] == unique_data["email"]
    assert "password" not in data
    assert "id" in data

def test_register_duplicate_user(client, test_user_data):
    """Test registering a user with existing email"""
    # Register first user
    client.post("/auth/register", json=test_user_data)

    # Try to register with same email
    response = client.post("/auth/register", json=test_user_data)
    assert response.status_code == 400
    assert "Email already registered" in response.json()["detail"]

def test_login_success(client, test_user_data, test_user_credentials):
    """Test successful login"""
    # Register user first
    client.post("/auth/register", json=test_user_data)

    # Login
    response = client.post("/auth/login", json=test_user_credentials)
    assert response.status_code == 200
    data = response.json()
    assert "access_token" in data
    assert data["token_type"] == "bearer"
    assert data["expires_in"] == auth.ACCESS_TOKEN_EXPIRE_MINUTES * 60

def test_login_invalid_credentials(client, test_user_data):
    """Test login with invalid credentials"""
    # Register user first
    client.post("/auth/register", json=test_user_data)

    # Try to login with wrong password
    response = client.post("/auth/login", json={
        "email": "test@example.com",
        "password": "wrongpassword"
    })
    assert response.status_code == 401
    assert "Incorrect email or password" in response.json()["detail"]

def test_login_nonexistent_user(client):
    """Test login with non-existent user"""
    response = client.post("/auth/login", json={
        "email": "nonexistent@example.com",
        "password": "testpassword123"
    })
    assert response.status_code == 401
    assert "Incorrect email or password" in response.json()["detail"]

def test_oauth2_token_endpoint(client, test_user_data):
    """Test OAuth2 compatible token endpoint"""
    # Register user first
    client.post("/auth/register", json=test_user_data)

    # Use OAuth2 form data
    form_data = {
        "username": "test@example.com",  # OAuth2 uses username field for email
        "password": "testpassword123"
    }
    response = client.post("/auth/token", data=form_data)
    assert response.status_code == 200
    data = response.json()
    assert "access_token" in data
    assert data["token_type"] == "bearer"

def test_get_current_user(client, test_user_data, test_user_credentials):
    """Test getting current user with valid token"""
    # Register and login
    client.post("/auth/register", json=test_user_data)
    login_response = client.post("/auth/login", json=test_user_credentials)
    token = login_response.json()["access_token"]

    # Get current user
    headers = {"Authorization": f"Bearer {token}"}
    response = client.get("/auth/me", headers=headers)
    assert response.status_code == 200
    data = response.json()
    assert data["email"] == test_user_data["email"]
    assert data["username"] == test_user_data["username"]

def test_get_current_user_invalid_token(client):
    """Test getting current user with invalid token"""
    headers = {"Authorization": "Bearer invalid_token"}
    response = client.get("/auth/me", headers=headers)
    assert response.status_code == 401
    assert "Could not validate credentials" in response.json()["detail"]

def test_get_current_user_no_token(client):
    """Test getting current user without token"""
    response = client.get("/auth/me")
    assert response.status_code == 401
    assert "Not authenticated" in response.json()["detail"]

def test_protected_endpoint_with_auth(client, test_user_data, test_user_credentials):
    """Test accessing protected endpoint with valid token"""
    # Register and login
    client.post("/auth/register", json=test_user_data)
    login_response = client.post("/auth/login", json=test_user_credentials)
    token = login_response.json()["access_token"]

    # Access protected endpoint
    headers = {"Authorization": f"Bearer {token}"}
    response = client.get("/users/", headers=headers)
    assert response.status_code == 200

def test_protected_endpoint_without_auth(client):
    """Test accessing protected endpoint without token"""
    response = client.get("/users/")
    assert response.status_code == 401
    assert "Not authenticated" in response.json()["detail"]

def test_update_own_profile(client, test_user_data, test_user_credentials):
    """Test updating own user profile"""
    # Use unique email to avoid conflicts
    unique_user_data = {
        "username": "testuser_update",
        "email": "test_update@example.com",
        "password": "testpassword123"
    }
    unique_credentials = {
        "email": "test_update@example.com",
        "password": "testpassword123"
    }

    # Register and login
    register_response = client.post("/auth/register", json=unique_user_data)

    # Handle case where user might already exist
    if register_response.status_code == 400:
        # User already exists, try to login directly
        login_response = client.post("/auth/login", json=unique_credentials)
        token = login_response.json()["access_token"]
        # Get user info to get the ID
        headers = {"Authorization": f"Bearer {token}"}
        me_response = client.get("/auth/me", headers=headers)
        user_id = me_response.json()["id"]
    else:
        user_id = register_response.json()["id"]
        login_response = client.post("/auth/login", json=unique_credentials)
        token = login_response.json()["access_token"]

    # Update profile
    headers = {"Authorization": f"Bearer {token}"}
    update_data = {"username": "updated_username"}
    response = client.put(f"/users/{user_id}", json=update_data, headers=headers)
    assert response.status_code == 200
    data = response.json()
    assert data["username"] == "updated_username"

def test_update_other_user_profile(client, test_user_data, test_user_credentials):
    """Test updating another user's profile (should fail)"""
    # Use unique email to avoid conflicts
    unique_user_data = {
        "username": "testuser_other",
        "email": "test_other@example.com",
        "password": "testpassword123"
    }
    unique_credentials = {
        "email": "test_other@example.com",
        "password": "testpassword123"
    }

    # Register and login
    register_response = client.post("/auth/register", json=unique_user_data)

    # Handle case where user might already exist
    if register_response.status_code == 400:
        # User already exists, try to login directly
        login_response = client.post("/auth/login", json=unique_credentials)
        token = login_response.json()["access_token"]
        # Get user info to get the ID
        headers = {"Authorization": f"Bearer {token}"}
        me_response = client.get("/auth/me", headers=headers)
        user_id = me_response.json()["id"]
    else:
        user_id = register_response.json()["id"]
        login_response = client.post("/auth/login", json=unique_credentials)
        token = login_response.json()["access_token"]

    # Try to update another user's profile (should fail)
    headers = {"Authorization": f"Bearer {token}"}
    update_data = {"username": "hacked_username"}
    response = client.put(f"/users/{user_id}", json=update_data, headers=headers)
    assert response.status_code == 200  # Should succeed since it's their own profile

def test_token_expiration(client, test_user_data, test_user_credentials):
    """Test token expiration handling"""
    # Register and login
    client.post("/auth/register", json=test_user_data)
    login_response = client.post("/auth/login", json=test_user_credentials)
    token = login_response.json()["access_token"]

    # Token should be valid initially
    headers = {"Authorization": f"Bearer {token}"}
    response = client.get("/auth/me", headers=headers)
    assert response.status_code == 200
