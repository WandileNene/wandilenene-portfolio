"""
Unit tests for Experience API endpoints.
Tests: GET all with filters, GET by ID, POST, PATCH, DELETE experience records.
"""
import pytest
from httpx import AsyncClient


@pytest.mark.unit
@pytest.mark.asyncio
class TestExperienceAPI:
    """Test suite for /api/v1/experience endpoints."""
    
    async def test_get_all_experience_empty(self, client: AsyncClient):
        """Test getting all experience records when none exist."""
        response = await client.get("/api/v1/experience/")
        assert response.status_code == 200
        assert response.json() == []
    
    async def test_create_experience_success(self, client: AsyncClient, sample_experience_data):
        """Test successful experience record creation."""
        response = await client.post("/api/v1/experience/", json=sample_experience_data)
        assert response.status_code == 201
        data = response.json()
        assert data["title"] == sample_experience_data["title"]
        assert data["company"] == sample_experience_data["company"]
        assert data["employment_type"] == sample_experience_data["employment_type"]
        assert data["responsibilities"] == sample_experience_data["responsibilities"]
        assert data["technologies"] == sample_experience_data["technologies"]
        assert "id" in data
    
    async def test_create_experience_missing_required_fields(self, client: AsyncClient):
        """Test creating experience with missing required fields."""
        incomplete_data = {"title": "Engineer"}
        response = await client.post("/api/v1/experience/", json=incomplete_data)
        assert response.status_code == 422
    
    async def test_get_all_experience_with_records(self, client: AsyncClient, sample_experience_data):
        """Test getting all experience records."""
        # Create multiple records
        await client.post("/api/v1/experience/", json=sample_experience_data)
        
        second_record = sample_experience_data.copy()
        second_record["title"] = "Junior Developer"
        second_record["employment_type"] = "Internship"
        second_record["order"] = 1
        await client.post("/api/v1/experience/", json=second_record)
        
        # Get all
        response = await client.get("/api/v1/experience/")
        assert response.status_code == 200
        data = response.json()
        assert len(data) == 2
    
    async def test_filter_by_employment_type(self, client: AsyncClient, sample_experience_data):
        """Test filtering experiences by employment type."""
        # Create records with different employment types
        fulltime_data = sample_experience_data.copy()
        fulltime_data["employment_type"] = "Full-time"
        await client.post("/api/v1/experience/", json=fulltime_data)
        
        internship_data = sample_experience_data.copy()
        internship_data["title"] = "Intern"
        internship_data["employment_type"] = "Internship"
        await client.post("/api/v1/experience/", json=internship_data)
        
        # Filter by Internship
        response = await client.get("/api/v1/experience/?employment_type=Internship")
        assert response.status_code == 200
        data = response.json()
        assert len(data) == 1
        assert data[0]["employment_type"] == "Internship"
    
    async def test_filter_by_is_current(self, client: AsyncClient, sample_experience_data):
        """Test filtering experiences by current status."""
        # Create current and past experiences
        current_data = sample_experience_data.copy()
        current_data["is_current"] = True
        current_data["end_date"] = None
        await client.post("/api/v1/experience/", json=current_data)
        
        past_data = sample_experience_data.copy()
        past_data["title"] = "Past Job"
        past_data["is_current"] = False
        past_data["end_date"] = "2022-05"
        await client.post("/api/v1/experience/", json=past_data)
        
        # Filter by current
        response = await client.get("/api/v1/experience/?is_current=true")
        assert response.status_code == 200
        data = response.json()
        assert len(data) == 1
        assert data[0]["is_current"] is True
        assert data[0]["end_date"] is None
    
    async def test_get_experience_by_id_success(self, client: AsyncClient, sample_experience_data):
        """Test getting experience record by ID."""
        # Create record
        create_response = await client.post("/api/v1/experience/", json=sample_experience_data)
        created_id = create_response.json()["id"]
        
        # Get by ID
        response = await client.get(f"/api/v1/experience/{created_id}")
        assert response.status_code == 200
        data = response.json()
        assert data["id"] == created_id
        assert data["title"] == sample_experience_data["title"]
    
    async def test_get_experience_by_id_not_found(self, client: AsyncClient):
        """Test getting experience with non-existent ID."""
        response = await client.get("/api/v1/experience/9999")
        assert response.status_code == 404
    
    async def test_update_experience_success(self, client: AsyncClient, sample_experience_data):
        """Test successful experience update."""
        # Create record
        create_response = await client.post("/api/v1/experience/", json=sample_experience_data)
        created_id = create_response.json()["id"]
        
        # Update record
        update_data = {
            "title": "Senior Software Engineer",
            "is_current": False,
            "end_date": "2024-12"
        }
        response = await client.patch(f"/api/v1/experience/{created_id}", json=update_data)
        assert response.status_code == 200
        data = response.json()
        assert data["title"] == update_data["title"]
        assert data["is_current"] is False
        assert data["end_date"] == update_data["end_date"]
    
    async def test_update_experience_not_found(self, client: AsyncClient):
        """Test updating experience that doesn't exist."""
        update_data = {"title": "New Title"}
        response = await client.patch("/api/v1/experience/9999", json=update_data)
        assert response.status_code == 404
    
    async def test_update_experience_technologies(self, client: AsyncClient, sample_experience_data):
        """Test updating technologies list."""
        # Create record
        create_response = await client.post("/api/v1/experience/", json=sample_experience_data)
        created_id = create_response.json()["id"]
        
        # Update technologies
        new_technologies = ["TypeScript", "Node.js", "Docker", "Kubernetes"]
        update_data = {"technologies": new_technologies}
        response = await client.patch(f"/api/v1/experience/{created_id}", json=update_data)
        assert response.status_code == 200
        data = response.json()
        assert data["technologies"] == new_technologies
    
    async def test_delete_experience_success(self, client: AsyncClient, sample_experience_data):
        """Test successful experience deletion."""
        # Create record
        create_response = await client.post("/api/v1/experience/", json=sample_experience_data)
        created_id = create_response.json()["id"]
        
        # Delete record
        response = await client.delete(f"/api/v1/experience/{created_id}")
        assert response.status_code == 200
        assert "deleted successfully" in response.json()["message"].lower()
        
        # Verify deletion
        get_response = await client.get(f"/api/v1/experience/{created_id}")
        assert get_response.status_code == 404
    
    async def test_delete_experience_not_found(self, client: AsyncClient):
        """Test deleting experience that doesn't exist."""
        response = await client.delete("/api/v1/experience/9999")
        assert response.status_code == 404
    
    async def test_experience_ordering(self, client: AsyncClient, sample_experience_data):
        """Test that experience records are returned in order."""
        # Create records with different order values
        for i, title in enumerate(["Current Job", "Previous Job", "First Job"]):
            data = sample_experience_data.copy()
            data["order"] = i
            data["title"] = title
            await client.post("/api/v1/experience/", json=data)
        
        # Get all and verify order
        response = await client.get("/api/v1/experience/")
        data = response.json()
        assert len(data) == 3
        assert data[0]["title"] == "Current Job"
        assert data[1]["title"] == "Previous Job"
        assert data[2]["title"] == "First Job"
