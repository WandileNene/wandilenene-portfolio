"""
Unit tests for Projects API endpoints.
Tests: GET all with filters, GET featured, GET by slug/ID, POST, PATCH, DELETE projects.
"""
import pytest
from httpx import AsyncClient


@pytest.mark.unit
@pytest.mark.asyncio
class TestProjectsAPI:
    """Test suite for /api/v1/projects endpoints."""
    
    async def test_get_all_projects_empty(self, client: AsyncClient):
        """Test getting all projects when none exist."""
        response = await client.get("/api/v1/projects/")
        assert response.status_code == 200
        assert response.json() == []
    
    async def test_create_project_success(self, client: AsyncClient, sample_project_data):
        """Test successful project creation."""
        response = await client.post("/api/v1/projects/", json=sample_project_data)
        assert response.status_code == 201
        data = response.json()
        assert data["name"] == sample_project_data["name"]
        assert data["slug"] == sample_project_data["slug"]
        assert data["short_description"] == sample_project_data["short_description"]
        assert data["technologies"] == sample_project_data["technologies"]
        assert data["is_featured"] == sample_project_data["is_featured"]
        assert "id" in data
    
    async def test_create_project_duplicate_slug(self, client: AsyncClient, sample_project_data):
        """Test creating project with duplicate slug."""
        # Create first project
        await client.post("/api/v1/projects/", json=sample_project_data)
        
        # Try to create another with same slug
        response = await client.post("/api/v1/projects/", json=sample_project_data)
        assert response.status_code == 409
        assert "already exists" in response.json()["detail"].lower()
    
    async def test_create_project_missing_required_fields(self, client: AsyncClient):
        """Test creating project with missing required fields."""
        incomplete_data = {"name": "Test Project"}
        response = await client.post("/api/v1/projects/", json=incomplete_data)
        assert response.status_code == 422
    
    async def test_get_all_projects_with_records(self, client: AsyncClient, sample_project_data):
        """Test getting all projects."""
        # Create multiple projects
        await client.post("/api/v1/projects/", json=sample_project_data)
        
        second_project = sample_project_data.copy()
        second_project["name"] = "Second Project"
        second_project["slug"] = "second-project"
        second_project["order"] = 1
        await client.post("/api/v1/projects/", json=second_project)
        
        # Get all
        response = await client.get("/api/v1/projects/")
        assert response.status_code == 200
        data = response.json()
        assert len(data) == 2
    
    async def test_filter_projects_by_featured(self, client: AsyncClient, sample_project_data):
        """Test filtering projects by featured status."""
        # Create featured project
        featured_data = sample_project_data.copy()
        featured_data["is_featured"] = True
        await client.post("/api/v1/projects/", json=featured_data)
        
        # Create non-featured project
        non_featured_data = sample_project_data.copy()
        non_featured_data["slug"] = "non-featured-project"
        non_featured_data["is_featured"] = False
        await client.post("/api/v1/projects/", json=non_featured_data)
        
        # Filter by featured
        response = await client.get("/api/v1/projects/?featured=true")
        assert response.status_code == 200
        data = response.json()
        assert len(data) == 1
        assert data[0]["is_featured"] is True
    
    async def test_filter_projects_by_status(self, client: AsyncClient, sample_project_data):
        """Test filtering projects by status."""
        # Create completed project
        completed_data = sample_project_data.copy()
        completed_data["status"] = "completed"
        await client.post("/api/v1/projects/", json=completed_data)
        
        # Create in-progress project
        inprogress_data = sample_project_data.copy()
        inprogress_data["slug"] = "inprogress-project"
        inprogress_data["status"] = "in-progress"
        await client.post("/api/v1/projects/", json=inprogress_data)
        
        # Filter by status
        response = await client.get("/api/v1/projects/?status=in-progress")
        assert response.status_code == 200
        data = response.json()
        assert len(data) == 1
        assert data[0]["status"] == "in-progress"
    
    async def test_get_featured_projects(self, client: AsyncClient, sample_project_data):
        """Test getting only featured projects."""
        # Create mixed projects
        featured_data = sample_project_data.copy()
        featured_data["is_featured"] = True
        await client.post("/api/v1/projects/", json=featured_data)
        
        non_featured_data = sample_project_data.copy()
        non_featured_data["slug"] = "non-featured"
        non_featured_data["is_featured"] = False
        await client.post("/api/v1/projects/", json=non_featured_data)
        
        # Get featured
        response = await client.get("/api/v1/projects/featured")
        assert response.status_code == 200
        data = response.json()
        assert len(data) == 1
        assert data[0]["is_featured"] is True
    
    async def test_get_project_by_slug_success(self, client: AsyncClient, sample_project_data):
        """Test getting project by slug."""
        # Create project
        await client.post("/api/v1/projects/", json=sample_project_data)
        
        # Get by slug
        response = await client.get(f"/api/v1/projects/slug/{sample_project_data['slug']}")
        assert response.status_code == 200
        data = response.json()
        assert data["slug"] == sample_project_data["slug"]
        assert data["name"] == sample_project_data["name"]
    
    async def test_get_project_by_slug_not_found(self, client: AsyncClient):
        """Test getting project with non-existent slug."""
        response = await client.get("/api/v1/projects/slug/non-existent-slug")
        assert response.status_code == 404
    
    async def test_get_project_by_id_success(self, client: AsyncClient, sample_project_data):
        """Test getting project by ID."""
        # Create project
        create_response = await client.post("/api/v1/projects/", json=sample_project_data)
        created_id = create_response.json()["id"]
        
        # Get by ID
        response = await client.get(f"/api/v1/projects/{created_id}")
        assert response.status_code == 200
        data = response.json()
        assert data["id"] == created_id
    
    async def test_get_project_by_id_not_found(self, client: AsyncClient):
        """Test getting project with non-existent ID."""
        response = await client.get("/api/v1/projects/9999")
        assert response.status_code == 404
    
    async def test_update_project_success(self, client: AsyncClient, sample_project_data):
        """Test successful project update."""
        # Create project
        create_response = await client.post("/api/v1/projects/", json=sample_project_data)
        created_id = create_response.json()["id"]
        
        # Update project
        update_data = {
            "name": "Updated Project Name",
            "status": "archived",
            "is_featured": False
        }
        response = await client.patch(f"/api/v1/projects/{created_id}", json=update_data)
        assert response.status_code == 200
        data = response.json()
        assert data["name"] == update_data["name"]
        assert data["status"] == update_data["status"]
        assert data["is_featured"] is False
    
    async def test_update_project_slug_conflict(self, client: AsyncClient, sample_project_data):
        """Test updating project slug to existing slug."""
        # Create two projects
        await client.post("/api/v1/projects/", json=sample_project_data)
        
        second_data = sample_project_data.copy()
        second_data["slug"] = "second-project"
        second_data["name"] = "Second Project"
        create_response = await client.post("/api/v1/projects/", json=second_data)
        second_id = create_response.json()["id"]
        
        # Try to update second project with first project's slug
        update_data = {"slug": sample_project_data["slug"]}
        response = await client.patch(f"/api/v1/projects/{second_id}", json=update_data)
        assert response.status_code == 409
    
    async def test_update_project_not_found(self, client: AsyncClient):
        """Test updating project that doesn't exist."""
        update_data = {"name": "New Name"}
        response = await client.patch("/api/v1/projects/9999", json=update_data)
        assert response.status_code == 404
    
    async def test_delete_project_success(self, client: AsyncClient, sample_project_data):
        """Test successful project deletion."""
        # Create project
        create_response = await client.post("/api/v1/projects/", json=sample_project_data)
        created_id = create_response.json()["id"]
        
        # Delete project
        response = await client.delete(f"/api/v1/projects/{created_id}")
        assert response.status_code == 200
        assert "deleted successfully" in response.json()["message"].lower()
        
        # Verify deletion
        get_response = await client.get(f"/api/v1/projects/{created_id}")
        assert get_response.status_code == 404
    
    async def test_delete_project_not_found(self, client: AsyncClient):
        """Test deleting project that doesn't exist."""
        response = await client.delete("/api/v1/projects/9999")
        assert response.status_code == 404
    
    async def test_projects_ordering(self, client: AsyncClient, sample_project_data):
        """Test that projects are returned in order."""
        # Create projects with different order values
        for i, name in enumerate(["Project C", "Project A", "Project B"]):
            data = sample_project_data.copy()
            data["order"] = i
            data["name"] = name
            data["slug"] = name.lower().replace(" ", "-")
            await client.post("/api/v1/projects/", json=data)
        
        # Get all and verify order
        response = await client.get("/api/v1/projects/")
        data = response.json()
        assert len(data) == 3
        assert data[0]["name"] == "Project C"  # order 0
        assert data[1]["name"] == "Project A"  # order 1
        assert data[2]["name"] == "Project B"  # order 2
