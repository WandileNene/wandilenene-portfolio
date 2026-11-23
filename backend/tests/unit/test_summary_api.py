"""
Unit tests for Summary API endpoint.
Tests: GET complete portfolio summary with all data aggregated.
"""
import pytest
from httpx import AsyncClient


@pytest.mark.unit
@pytest.mark.asyncio
class TestSummaryAPI:
    """Test suite for /api/v1/summary endpoint."""
    
    async def test_get_summary_empty_portfolio(self, client: AsyncClient):
        """Test getting summary when no data exists."""
        response = await client.get("/api/v1/summary/")
        assert response.status_code == 200
        data = response.json()
        
        # Check structure
        assert "profile" in data
        assert "education" in data
        assert "experience" in data
        assert "skills" in data
        assert "certifications" in data
        assert "projects" in data
        assert "achievements" in data
        assert "stats" in data
        
        # Check empty values
        assert data["profile"] is None
        assert data["education"] == []
        assert data["experience"] == []
        assert data["certifications"] == []
        assert data["projects"] == []
        assert data["achievements"] == []
        assert data["skills"] == {}
        
        # Check stats
        stats = data["stats"]
        assert stats["total_projects"] == 0
        assert stats["featured_projects"] == 0
        assert stats["total_skills"] == 0
        assert stats["total_certifications"] == 0
        assert stats["total_achievements"] == 0
    
    async def test_get_summary_with_complete_portfolio(
        self, 
        client: AsyncClient,
        sample_profile_data,
        sample_education_data,
        sample_experience_data,
        sample_skill_data,
        sample_certification_data,
        sample_project_data,
        sample_achievement_data
    ):
        """Test getting summary with complete portfolio data."""
        # Create all data
        await client.post("/api/v1/profile/", json=sample_profile_data)
        await client.post("/api/v1/education/", json=sample_education_data)
        await client.post("/api/v1/experience/", json=sample_experience_data)
        await client.post("/api/v1/skills/", json=sample_skill_data)
        await client.post("/api/v1/certifications/", json=sample_certification_data)
        await client.post("/api/v1/projects/", json=sample_project_data)
        await client.post("/api/v1/achievements/", json=sample_achievement_data)
        
        # Get summary
        response = await client.get("/api/v1/summary/")
        assert response.status_code == 200
        data = response.json()
        
        # Verify profile
        assert data["profile"] is not None
        assert data["profile"]["full_name"] == sample_profile_data["full_name"]
        assert data["profile"]["email"] == sample_profile_data["email"]
        
        # Verify collections
        assert len(data["education"]) == 1
        assert data["education"][0]["degree"] == sample_education_data["degree"]
        
        assert len(data["experience"]) == 1
        assert data["experience"][0]["title"] == sample_experience_data["title"]
        
        assert len(data["certifications"]) == 1
        assert data["certifications"][0]["name"] == sample_certification_data["name"]
        
        assert len(data["projects"]) == 1
        assert data["projects"][0]["name"] == sample_project_data["name"]
        
        assert len(data["achievements"]) == 1
        assert data["achievements"][0]["title"] == sample_achievement_data["title"]
        
        # Verify skills grouped by category
        assert "skills" in data
        assert sample_skill_data["category"] in data["skills"]
        category_skills = data["skills"][sample_skill_data["category"]]
        assert len(category_skills) == 1
        assert category_skills[0]["name"] == sample_skill_data["name"]
        assert category_skills[0]["proficiency"] == sample_skill_data["proficiency"]
        
        # Verify stats
        stats = data["stats"]
        assert stats["total_projects"] == 1
        assert stats["featured_projects"] == 1  # sample_project_data has is_featured=True
        assert stats["total_skills"] == 1
        assert stats["skill_categories"] == 1
        assert stats["total_certifications"] == 1
        assert stats["total_achievements"] == 1
        assert stats["years_of_experience"] == 1
    
    async def test_get_summary_with_multiple_skills_categories(self, client: AsyncClient):
        """Test summary with multiple skill categories."""
        # Create skills in different categories
        skills = [
            {"name": "Python", "category": "Languages", "proficiency": 90, "order": 0},
            {"name": "JavaScript", "category": "Languages", "proficiency": 85, "order": 1},
            {"name": "React", "category": "Frameworks", "proficiency": 80, "order": 0},
            {"name": "Docker", "category": "Tools", "proficiency": 75, "order": 0},
        ]
        for skill in skills:
            await client.post("/api/v1/skills/", json=skill)
        
        # Get summary
        response = await client.get("/api/v1/summary/")
        data = response.json()
        
        # Verify grouped skills
        assert len(data["skills"]) == 3
        assert "Languages" in data["skills"]
        assert "Frameworks" in data["skills"]
        assert "Tools" in data["skills"]
        assert len(data["skills"]["Languages"]) == 2
        assert len(data["skills"]["Frameworks"]) == 1
        assert len(data["skills"]["Tools"]) == 1
        
        # Verify stats
        assert data["stats"]["total_skills"] == 4
        assert data["stats"]["skill_categories"] == 3
    
    async def test_get_summary_featured_projects_count(self, client: AsyncClient, sample_project_data):
        """Test that featured projects are counted correctly."""
        # Create featured and non-featured projects
        featured = sample_project_data.copy()
        featured["is_featured"] = True
        await client.post("/api/v1/projects/", json=featured)
        
        non_featured = sample_project_data.copy()
        non_featured["slug"] = "non-featured"
        non_featured["is_featured"] = False
        await client.post("/api/v1/projects/", json=non_featured)
        
        # Get summary
        response = await client.get("/api/v1/summary/")
        data = response.json()
        
        assert data["stats"]["total_projects"] == 2
        assert data["stats"]["featured_projects"] == 1
    
    async def test_get_summary_data_ordering(
        self,
        client: AsyncClient,
        sample_education_data,
        sample_experience_data,
        sample_project_data
    ):
        """Test that summary data respects ordering."""
        # Create multiple items with different orders
        for i in range(3):
            edu = sample_education_data.copy()
            edu["order"] = 2 - i  # Reverse order: 2, 1, 0
            edu["degree"] = f"Degree {i}"
            await client.post("/api/v1/education/", json=edu)
        
        # Get summary
        response = await client.get("/api/v1/summary/")
        data = response.json()
        
        # Verify ordering (should be 0, 1, 2)
        assert len(data["education"]) == 3
        assert data["education"][0]["degree"] == "Degree 2"  # order 0
        assert data["education"][1]["degree"] == "Degree 1"  # order 1
        assert data["education"][2]["degree"] == "Degree 0"  # order 2
    
    async def test_summary_response_structure(self, client: AsyncClient):
        """Test that summary response has correct structure."""
        response = await client.get("/api/v1/summary/")
        assert response.status_code == 200
        data = response.json()
        
        # Required top-level keys
        required_keys = [
            "profile", "education", "experience", "skills",
            "certifications", "projects", "achievements", "stats"
        ]
        for key in required_keys:
            assert key in data
        
        # Stats structure
        stats_keys = [
            "total_projects", "featured_projects", "total_skills",
            "skill_categories", "total_certifications",
            "total_achievements", "years_of_experience"
        ]
        for key in stats_keys:
            assert key in data["stats"]
