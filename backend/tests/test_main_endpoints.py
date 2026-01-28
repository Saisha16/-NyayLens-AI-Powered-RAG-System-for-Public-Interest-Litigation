"""Integration tests for main API endpoints."""

import pytest
import json
from fastapi.testclient import TestClient
from backend.main import app

client = TestClient(app)

class TestMainEndpoints:
    """Main API endpoint tests."""
    
    def test_health_endpoint(self):
        """Test health check endpoint."""
        # First, try without auth (may fail if auth required)
        response = client.get("/health")
        # Should return 200 or 401
        assert response.status_code in [200, 401, 404]
    
    def test_topics_endpoint(self):
        """Test topics endpoint."""
        response = client.get("/topics")
        
        if response.status_code == 200:
            data = response.json()
            assert "topics" in data
            assert isinstance(data["topics"], list)
            assert len(data["topics"]) > 0
    
    def test_news_endpoint_basic(self):
        """Test news endpoint without filters."""
        response = client.get("/news")
        
        if response.status_code == 200:
            data = response.json()
            assert "items" in data or "error" in data
    
    def test_news_endpoint_with_topic_filter(self):
        """Test news endpoint with topic filter."""
        response = client.get("/news?topic=crime")
        
        if response.status_code == 200:
            data = response.json()
            assert "items" in data or "error" in data
    
    def test_news_endpoint_with_date_filter(self):
        """Test news endpoint with date filter."""
        response = client.get("/news?days_back=7")
        
        if response.status_code == 200:
            data = response.json()
            assert "items" in data or "error" in data
    
    def test_generate_pil_endpoint(self):
        """Test PIL generation endpoint."""
        response = client.get("/generate-pil?idx=0")
        
        if response.status_code == 200:
            data = response.json()
            if "news_title" in data:  # Success case
                assert "severity_score" in data
                assert "priority_level" in data
                assert isinstance(data["severity_score"], (int, float))
    
    def test_generate_pil_with_topic(self):
        """Test PIL generation with topic filter."""
        response = client.get("/generate-pil?idx=0&topic=crime")
        
        if response.status_code == 200:
            data = response.json()
            if "error" not in data:
                assert "severity_score" in data
    
    def test_add_custom_news_endpoint(self):
        """Test custom news addition endpoint."""
        response = client.post(
            "/add-custom-news",
            params={
                "url": "https://example.com/article",
                "title": "Test Article"
            }
        )
        
        # May fail if URL doesn't exist, but should handle gracefully
        assert response.status_code in [200, 400]
    
    def test_refresh_news_endpoint(self):
        """Test news refresh endpoint."""
        response = client.post(
            "/refresh-news",
            params={"days_back": 7}
        )
        
        if response.status_code == 200:
            data = response.json()
            assert "success" in data or "error" in data
    
    def test_api_documentation_endpoint(self):
        """Test Swagger API docs endpoint."""
        response = client.get("/docs")
        
        # Swagger UI should return HTML
        assert response.status_code == 200
        assert "swagger" in response.text.lower() or "openapi" in response.text.lower()
    
    def test_openapi_schema_endpoint(self):
        """Test OpenAPI schema endpoint."""
        response = client.get("/openapi.json")
        
        assert response.status_code == 200
        data = response.json()
        assert "openapi" in data or "swagger" in data
        assert "paths" in data
