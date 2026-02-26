import pytest
from fastapi.testclient import TestClient
from app.main import app

client = TestClient(app)


class TestQueryEndpoints:
    """Test suite for query-related endpoints"""

    def test_create_query_success(self):
        """Test successful query creation"""
        query_data = {
            "query_text": "Comment réparer le dispositif médical X?",
            "user_id": 1
        }
        response = client.post("/api/queries/", json=query_data)
        assert response.status_code == 200
        data = response.json()
        assert "id" in data
        assert data["query_text"] == query_data["query_text"]

    def test_create_query_empty_text(self):
        """Test query creation with empty text"""
        query_data = {
            "query_text": "",
            "user_id": 1
        }
        response = client.post("/api/queries/", json=query_data)
        assert response.status_code == 422  

    def test_get_query_history(self):
        """Test retrieving query history"""
        response = client.get("/api/queries/history/1")
        assert response.status_code == 200
        data = response.json()
        assert isinstance(data, list)

    def test_health_check(self):
        """Test API health check endpoint"""
        response = client.get("/health")
        assert response.status_code == 200
        assert response.json()["status"] == "healthy"
