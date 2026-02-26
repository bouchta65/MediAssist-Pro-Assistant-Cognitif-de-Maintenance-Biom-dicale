import pytest
from fastapi.testclient import TestClient
from app.main import app

client = TestClient(app)


class TestUserEndpoints:
    """Test suite for user-related endpoints"""

    def test_get_current_user_unauthorized(self):
        """Test getting current user without authentication"""
        response = client.get("/api/users/me")
        assert response.status_code == 401

    def test_user_registration_flow(self):
        """Test user registration"""
        user_data = {
            "email": "test@example.com",
            "username": "testuser",
            "full_name": "Test User"
        }
        response = client.post("/api/users/register", json=user_data)
        assert response.status_code in [200, 201, 409]

    def test_invalid_email_format(self):
        """Test user registration with invalid email"""
        user_data = {
            "email": "invalid-email",
            "username": "testuser",
            "full_name": "Test User"
        }
        response = client.post("/api/users/register", json=user_data)
        assert response.status_code == 422  
