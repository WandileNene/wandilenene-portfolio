"""
Unit tests for Profile API endpoints.
Tests: GET, POST, PATCH, DELETE profile operations.
"""
import pytest
from httpx import AsyncClient


@pytest.mark.unit
@pytest.mark.asyncio
class TestProfileAPI:
    """Test suite for /api/v1/profile endpoints."""
    
    async def test_get_profile_not_found(self, client: AsyncClient):
        """Test getting profile when none exists."""
        response = await client.get("/api/v1/profile/")
        assert response.status_code == 404
        assert "not found" in response.json()["detail"].lower()
    
    async def test_create_profile_success(self, client: AsyncClient, sample_profile_data):
        """Test successful profile creation."""
        response = await client.post("/api/v1/profile/", json=sample_profile_data)
        assert response.status_code == 201
        data = response.json()
        assert data["full_name"] == sample_profile_data["full_name"]
        assert data["email"] == sample_profile_data["email"]
        assert data["title"] == sample_profile_data["title"]
        assert "id" in data
        assert "created_at" in data
        assert "updated_at" in data
    
    async def test_create_profile_duplicate_conflict(self, client: AsyncClient, sample_profile_data):
        """Test creating profile when one already exists."""
        # Create first profile
        await client.post("/api/v1/profile/", json=sample_profile_data)
        
        # Try to create another
        response = await client.post("/api/v1/profile/", json=sample_profile_data)
        assert response.status_code == 409
        assert "already exists" in response.json()["detail"].lower()
    
    async def test_create_profile_invalid_email(self, client: AsyncClient, sample_profile_data):
        """Test creating profile with invalid email."""
        sample_profile_data["email"] = "not-an-email"
        response = await client.post("/api/v1/profile/", json=sample_profile_data)
        assert response.status_code == 422
    
    async def test_create_profile_missing_required_fields(self, client: AsyncClient):
        """Test creating profile with missing required fields."""
        incomplete_data = {"full_name": "John Doe"}
        response = await client.post("/api/v1/profile/", json=incomplete_data)
        assert response.status_code == 422
    
    async def test_get_profile_success(self, client: AsyncClient, sample_profile_data):
        """Test getting profile after creation."""
        # Create profile
        create_response = await client.post("/api/v1/profile/", json=sample_profile_data)
        created_id = create_response.json()["id"]
        
        # Get profile
        response = await client.get("/api/v1/profile/")
        assert response.status_code == 200
        data = response.json()
        assert data["id"] == created_id
        assert data["full_name"] == sample_profile_data["full_name"]
    
    async def test_update_profile_success(self, client: AsyncClient, sample_profile_data):
        """Test successful profile update."""
        # Create profile
        await client.post("/api/v1/profile/", json=sample_profile_data)
        
        # Update profile
        update_data = {"title": "Senior Software Engineer", "tagline": "New tagline"}
        response = await client.patch("/api/v1/profile/", json=update_data)
        assert response.status_code == 200
        data = response.json()
        assert data["title"] == update_data["title"]
        assert data["tagline"] == update_data["tagline"]
        assert data["full_name"] == sample_profile_data["full_name"]  # Unchanged
    
    async def test_update_profile_not_found(self, client: AsyncClient):
        """Test updating profile when none exists."""
        update_data = {"title": "Senior Software Engineer"}
        response = await client.patch("/api/v1/profile/", json=update_data)
        assert response.status_code == 404
    
    async def test_update_profile_partial(self, client: AsyncClient, sample_profile_data):
        """Test partial profile update."""
        # Create profile
        await client.post("/api/v1/profile/", json=sample_profile_data)
        
        # Update only one field
        update_data = {"bio": "Updated bio text"}
        response = await client.patch("/api/v1/profile/", json=update_data)
        assert response.status_code == 200
        data = response.json()
        assert data["bio"] == update_data["bio"]
    
    async def test_delete_profile_success(self, client: AsyncClient, sample_profile_data):
        """Test successful profile deletion."""
        # Create profile
        await client.post("/api/v1/profile/", json=sample_profile_data)
        
        # Delete profile
        response = await client.delete("/api/v1/profile/")
        assert response.status_code == 200
        assert "deleted successfully" in response.json()["message"].lower()
        
        # Verify deletion
        get_response = await client.get("/api/v1/profile/")
        assert get_response.status_code == 404
    
    async def test_delete_profile_not_found(self, client: AsyncClient):
        """Test deleting profile when none exists."""
        response = await client.delete("/api/v1/profile/")
        assert response.status_code == 404
