"""
Unit tests for Skills API endpoints.
Tests: GET all, GET grouped, GET categories, GET by ID, POST, PATCH, DELETE skills.
"""
import pytest
from httpx import AsyncClient


@pytest.mark.unit
@pytest.mark.asyncio
class TestSkillsAPI:
    """Test suite for /api/v1/skills endpoints."""
    
    async def test_get_all_skills_empty(self, client: AsyncClient):
        """Test getting all skills when none exist."""
        response = await client.get("/api/v1/skills/")
        assert response.status_code == 200
        assert response.json() == []
    
    async def test_create_skill_success(self, client: AsyncClient, sample_skill_data):
        """Test successful skill creation."""
        response = await client.post("/api/v1/skills/", json=sample_skill_data)
        assert response.status_code == 201
        data = response.json()
        assert data["name"] == sample_skill_data["name"]
        assert data["category"] == sample_skill_data["category"]
        assert data["proficiency"] == sample_skill_data["proficiency"]
        assert "id" in data
    
    async def test_create_skill_invalid_proficiency(self, client: AsyncClient, sample_skill_data):
        """Test creating skill with invalid proficiency value."""
        sample_skill_data["proficiency"] = 150  # Over 100
        response = await client.post("/api/v1/skills/", json=sample_skill_data)
        assert response.status_code == 422
    
    async def test_create_skill_negative_proficiency(self, client: AsyncClient, sample_skill_data):
        """Test creating skill with negative proficiency."""
        sample_skill_data["proficiency"] = -10
        response = await client.post("/api/v1/skills/", json=sample_skill_data)
        assert response.status_code == 422
    
    async def test_get_all_skills_with_records(self, client: AsyncClient):
        """Test getting all skills."""
        # Create multiple skills
        skills = [
            {"name": "Python", "category": "Languages", "proficiency": 90, "order": 0},
            {"name": "JavaScript", "category": "Languages", "proficiency": 85, "order": 1},
            {"name": "Docker", "category": "Tools", "proficiency": 75, "order": 0},
        ]
        for skill in skills:
            await client.post("/api/v1/skills/", json=skill)
        
        # Get all
        response = await client.get("/api/v1/skills/")
        assert response.status_code == 200
        data = response.json()
        assert len(data) == 3
    
    async def test_filter_skills_by_category(self, client: AsyncClient):
        """Test filtering skills by category."""
        # Create skills in different categories
        await client.post("/api/v1/skills/", json={
            "name": "Python", "category": "Languages", "proficiency": 90, "order": 0
        })
        await client.post("/api/v1/skills/", json={
            "name": "Docker", "category": "Tools", "proficiency": 75, "order": 0
        })
        
        # Filter by category
        response = await client.get("/api/v1/skills/?category=Languages")
        assert response.status_code == 200
        data = response.json()
        assert len(data) == 1
        assert data[0]["category"] == "Languages"
        assert data[0]["name"] == "Python"
    
    async def test_get_skills_grouped(self, client: AsyncClient):
        """Test getting skills grouped by category."""
        # Create skills in multiple categories
        skills = [
            {"name": "Python", "category": "Languages", "proficiency": 90, "order": 0},
            {"name": "JavaScript", "category": "Languages", "proficiency": 85, "order": 1},
            {"name": "React", "category": "Frameworks", "proficiency": 80, "order": 0},
            {"name": "Docker", "category": "Tools", "proficiency": 75, "order": 0},
        ]
        for skill in skills:
            await client.post("/api/v1/skills/", json=skill)
        
        # Get grouped
        response = await client.get("/api/v1/skills/grouped")
        assert response.status_code == 200
        data = response.json()
        assert "categories" in data
        categories = data["categories"]
        assert "Languages" in categories
        assert "Frameworks" in categories
        assert "Tools" in categories
        assert len(categories["Languages"]) == 2
        assert len(categories["Frameworks"]) == 1
        assert len(categories["Tools"]) == 1
    
    async def test_get_skill_categories(self, client: AsyncClient):
        """Test getting list of unique skill categories."""
        # Create skills in different categories
        await client.post("/api/v1/skills/", json={
            "name": "Python", "category": "Languages", "proficiency": 90, "order": 0
        })
        await client.post("/api/v1/skills/", json={
            "name": "React", "category": "Frameworks", "proficiency": 80, "order": 0
        })
        await client.post("/api/v1/skills/", json={
            "name": "Docker", "category": "Tools", "proficiency": 75, "order": 0
        })
        
        # Get categories
        response = await client.get("/api/v1/skills/categories")
        assert response.status_code == 200
        data = response.json()
        assert "categories" in data
        categories = data["categories"]
        assert len(categories) == 3
        assert "Languages" in categories
        assert "Frameworks" in categories
        assert "Tools" in categories
    
    async def test_get_skill_by_id_success(self, client: AsyncClient, sample_skill_data):
        """Test getting skill by ID."""
        # Create skill
        create_response = await client.post("/api/v1/skills/", json=sample_skill_data)
        created_id = create_response.json()["id"]
        
        # Get by ID
        response = await client.get(f"/api/v1/skills/{created_id}")
        assert response.status_code == 200
        data = response.json()
        assert data["id"] == created_id
        assert data["name"] == sample_skill_data["name"]
    
    async def test_get_skill_by_id_not_found(self, client: AsyncClient):
        """Test getting skill with non-existent ID."""
        response = await client.get("/api/v1/skills/9999")
        assert response.status_code == 404
    
    async def test_update_skill_success(self, client: AsyncClient, sample_skill_data):
        """Test successful skill update."""
        # Create skill
        create_response = await client.post("/api/v1/skills/", json=sample_skill_data)
        created_id = create_response.json()["id"]
        
        # Update skill
        update_data = {"proficiency": 95, "icon": "python-new-icon"}
        response = await client.patch(f"/api/v1/skills/{created_id}", json=update_data)
        assert response.status_code == 200
        data = response.json()
        assert data["proficiency"] == 95
        assert data["icon"] == "python-new-icon"
        assert data["name"] == sample_skill_data["name"]  # Unchanged
    
    async def test_update_skill_not_found(self, client: AsyncClient):
        """Test updating skill that doesn't exist."""
        update_data = {"proficiency": 95}
        response = await client.patch("/api/v1/skills/9999", json=update_data)
        assert response.status_code == 404
    
    async def test_update_skill_change_category(self, client: AsyncClient, sample_skill_data):
        """Test updating skill category."""
        # Create skill
        create_response = await client.post("/api/v1/skills/", json=sample_skill_data)
        created_id = create_response.json()["id"]
        
        # Update category
        update_data = {"category": "Backend Languages"}
        response = await client.patch(f"/api/v1/skills/{created_id}", json=update_data)
        assert response.status_code == 200
        assert response.json()["category"] == "Backend Languages"
    
    async def test_delete_skill_success(self, client: AsyncClient, sample_skill_data):
        """Test successful skill deletion."""
        # Create skill
        create_response = await client.post("/api/v1/skills/", json=sample_skill_data)
        created_id = create_response.json()["id"]
        
        # Delete skill
        response = await client.delete(f"/api/v1/skills/{created_id}")
        assert response.status_code == 200
        assert "deleted successfully" in response.json()["message"].lower()
        
        # Verify deletion
        get_response = await client.get(f"/api/v1/skills/{created_id}")
        assert get_response.status_code == 404
    
    async def test_delete_skill_not_found(self, client: AsyncClient):
        """Test deleting skill that doesn't exist."""
        response = await client.delete("/api/v1/skills/9999")
        assert response.status_code == 404
    
    async def test_skills_ordering_by_category(self, client: AsyncClient):
        """Test that skills are ordered by category and order field."""
        # Create skills
        skills = [
            {"name": "Python", "category": "Languages", "proficiency": 90, "order": 1},
            {"name": "Java", "category": "Languages", "proficiency": 80, "order": 0},
            {"name": "Docker", "category": "Tools", "proficiency": 75, "order": 0},
        ]
        for skill in skills:
            await client.post("/api/v1/skills/", json=skill)
        
        # Get all (should be ordered by category, then order)
        response = await client.get("/api/v1/skills/")
        data = response.json()
        assert len(data) == 3
        # Languages category comes first (alphabetically), then Tools
        assert data[0]["category"] == "Languages"
        assert data[0]["name"] == "Java"  # order 0 in Languages
        assert data[1]["category"] == "Languages"
        assert data[1]["name"] == "Python"  # order 1 in Languages
        assert data[2]["category"] == "Tools"
