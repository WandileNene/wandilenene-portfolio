"""
Unit tests for Education API endpoints.
Tests: GET all, GET by ID, POST, PATCH, DELETE education records.
"""
import pytest
from httpx import AsyncClient


@pytest.mark.unit
@pytest.mark.asyncio
class TestEducationAPI:
    """Test suite for /api/v1/education endpoints."""
    
    async def test_get_all_education_empty(self, client: AsyncClient):
        """Test getting all education records when none exist."""
        response = await client.get("/api/v1/education/")
        assert response.status_code == 200
        assert response.json() == []
    
    async def test_create_education_success(self, client: AsyncClient, sample_education_data):
        """Test successful education record creation."""
        response = await client.post("/api/v1/education/", json=sample_education_data)
        assert response.status_code == 201
        data = response.json()
        assert data["degree"] == sample_education_data["degree"]
        assert data["institution"] == sample_education_data["institution"]
        assert data["field_of_study"] == sample_education_data["field_of_study"]
        assert "id" in data
        assert "created_at" in data
    
    async def test_create_education_missing_required_fields(self, client: AsyncClient):
        """Test creating education record with missing required fields."""
        incomplete_data = {"degree": "Bachelor"}
        response = await client.post("/api/v1/education/", json=incomplete_data)
        assert response.status_code == 422
    
    async def test_get_all_education_with_records(self, client: AsyncClient, sample_education_data):
        """Test getting all education records."""
        # Create multiple records
        await client.post("/api/v1/education/", json=sample_education_data)
        
        second_record = sample_education_data.copy()
        second_record["degree"] = "Master of Science"
        second_record["order"] = 1
        await client.post("/api/v1/education/", json=second_record)
        
        # Get all
        response = await client.get("/api/v1/education/")
        assert response.status_code == 200
        data = response.json()
        assert len(data) == 2
        assert data[0]["degree"] == sample_education_data["degree"]
        assert data[1]["degree"] == "Master of Science"
    
    async def test_get_education_by_id_success(self, client: AsyncClient, sample_education_data):
        """Test getting education record by ID."""
        # Create record
        create_response = await client.post("/api/v1/education/", json=sample_education_data)
        created_id = create_response.json()["id"]
        
        # Get by ID
        response = await client.get(f"/api/v1/education/{created_id}")
        assert response.status_code == 200
        data = response.json()
        assert data["id"] == created_id
        assert data["degree"] == sample_education_data["degree"]
    
    async def test_get_education_by_id_not_found(self, client: AsyncClient):
        """Test getting education record with non-existent ID."""
        response = await client.get("/api/v1/education/9999")
        assert response.status_code == 404
        assert "not found" in response.json()["detail"].lower()
    
    async def test_update_education_success(self, client: AsyncClient, sample_education_data):
        """Test successful education record update."""
        # Create record
        create_response = await client.post("/api/v1/education/", json=sample_education_data)
        created_id = create_response.json()["id"]
        
        # Update record
        update_data = {"degree": "Master of Computer Science", "grade": "4.0 GPA"}
        response = await client.patch(f"/api/v1/education/{created_id}", json=update_data)
        assert response.status_code == 200
        data = response.json()
        assert data["degree"] == update_data["degree"]
        assert data["grade"] == update_data["grade"]
        assert data["institution"] == sample_education_data["institution"]  # Unchanged
    
    async def test_update_education_not_found(self, client: AsyncClient):
        """Test updating education record that doesn't exist."""
        update_data = {"degree": "PhD"}
        response = await client.patch("/api/v1/education/9999", json=update_data)
        assert response.status_code == 404
    
    async def test_update_education_partial(self, client: AsyncClient, sample_education_data):
        """Test partial education record update."""
        # Create record
        create_response = await client.post("/api/v1/education/", json=sample_education_data)
        created_id = create_response.json()["id"]
        
        # Update only is_current flag
        update_data = {"is_current": True}
        response = await client.patch(f"/api/v1/education/{created_id}", json=update_data)
        assert response.status_code == 200
        assert response.json()["is_current"] is True
    
    async def test_delete_education_success(self, client: AsyncClient, sample_education_data):
        """Test successful education record deletion."""
        # Create record
        create_response = await client.post("/api/v1/education/", json=sample_education_data)
        created_id = create_response.json()["id"]
        
        # Delete record
        response = await client.delete(f"/api/v1/education/{created_id}")
        assert response.status_code == 200
        assert "deleted successfully" in response.json()["message"].lower()
        
        # Verify deletion
        get_response = await client.get(f"/api/v1/education/{created_id}")
        assert get_response.status_code == 404
    
    async def test_delete_education_not_found(self, client: AsyncClient):
        """Test deleting education record that doesn't exist."""
        response = await client.delete("/api/v1/education/9999")
        assert response.status_code == 404
    
    async def test_education_ordering(self, client: AsyncClient, sample_education_data):
        """Test that education records are returned in order."""
        # Create records with different order values
        data1 = sample_education_data.copy()
        data1["order"] = 2
        data1["degree"] = "Bachelor"
        await client.post("/api/v1/education/", json=data1)
        
        data2 = sample_education_data.copy()
        data2["order"] = 0
        data2["degree"] = "High School"
        await client.post("/api/v1/education/", json=data2)
        
        data3 = sample_education_data.copy()
        data3["order"] = 1
        data3["degree"] = "Associate"
        await client.post("/api/v1/education/", json=data3)
        
        # Get all and verify order
        response = await client.get("/api/v1/education/")
        data = response.json()
        assert len(data) == 3
        assert data[0]["degree"] == "High School"  # order 0
        assert data[1]["degree"] == "Associate"    # order 1
        assert data[2]["degree"] == "Bachelor"     # order 2
