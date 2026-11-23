"""
Integration tests for data validation and constraint enforcement.
Tests validation across different endpoints and edge cases.
"""
import pytest
from httpx import AsyncClient


@pytest.mark.integration
@pytest.mark.asyncio
class TestDataValidation:
    """Integration tests for data validation rules."""
    
    async def test_email_validation_across_endpoints(self, client: AsyncClient):
        """Test email validation in profile and contact endpoints."""
        # Invalid email in profile
        profile_data = {
            "full_name": "John Doe",
            "title": "Engineer",
            "email": "not-an-email",
        }
        profile_response = await client.post("/api/v1/profile/", json=profile_data)
        assert profile_response.status_code == 422
        
        # Invalid email in contact
        contact_data = {
            "name": "Jane Doe",
            "email": "invalid",
            "message": "Test message",
        }
        contact_response = await client.post("/api/v1/contact/", json=contact_data)
        assert contact_response.status_code == 422
    
    async def test_unique_slug_constraint(self, client: AsyncClient, sample_project_data):
        """Test that project slugs must be unique."""
        # Create first project
        response1 = await client.post("/api/v1/projects/", json=sample_project_data)
        assert response1.status_code == 201
        
        # Try to create another with same slug
        duplicate_data = sample_project_data.copy()
        duplicate_data["name"] = "Different Name"
        response2 = await client.post("/api/v1/projects/", json=duplicate_data)
        assert response2.status_code == 409
        assert "already exists" in response2.json()["detail"].lower()
    
    async def test_proficiency_range_validation(self, client: AsyncClient):
        """Test that skill proficiency is bounded 0-100."""
        # Test over 100
        skill_over = {
            "name": "Python",
            "category": "Languages",
            "proficiency": 150,
            "order": 0
        }
        response_over = await client.post("/api/v1/skills/", json=skill_over)
        assert response_over.status_code == 422
        
        # Test negative
        skill_negative = {
            "name": "Python",
            "category": "Languages",
            "proficiency": -10,
            "order": 0
        }
        response_negative = await client.post("/api/v1/skills/", json=skill_negative)
        assert response_negative.status_code == 422
        
        # Test valid boundaries
        skill_zero = {
            "name": "Beginner Skill",
            "category": "Languages",
            "proficiency": 0,
            "order": 0
        }
        response_zero = await client.post("/api/v1/skills/", json=skill_zero)
        assert response_zero.status_code == 201
        
        skill_hundred = {
            "name": "Expert Skill",
            "category": "Languages",
            "proficiency": 100,
            "order": 0
        }
        response_hundred = await client.post("/api/v1/skills/", json=skill_hundred)
        assert response_hundred.status_code == 201
    
    async def test_required_fields_validation(self, client: AsyncClient):
        """Test that required fields are enforced."""
        # Profile missing title
        profile_incomplete = {
            "full_name": "John Doe",
            "email": "john@example.com",
        }
        response = await client.post("/api/v1/profile/", json=profile_incomplete)
        assert response.status_code == 422
        
        # Experience missing company
        experience_incomplete = {
            "title": "Engineer",
            "start_date": "2020-01",
        }
        response = await client.post("/api/v1/experience/", json=experience_incomplete)
        assert response.status_code == 422
        
        # Project missing slug
        project_incomplete = {
            "name": "My Project",
            "short_description": "A project",
        }
        response = await client.post("/api/v1/projects/", json=project_incomplete)
        assert response.status_code == 422
    
    async def test_field_length_validation(self, client: AsyncClient, sample_profile_data):
        """Test field length constraints."""
        # Test max length on short_description (500 chars)
        project_data = {
            "name": "Test Project",
            "slug": "test-project",
            "short_description": "x" * 501,  # Over limit
        }
        response = await client.post("/api/v1/projects/", json=project_data)
        assert response.status_code == 422
        
        # Test valid length
        project_data["short_description"] = "x" * 500  # Exactly at limit
        response = await client.post("/api/v1/projects/", json=project_data)
        assert response.status_code == 201
    
    async def test_optional_fields_handling(
        self,
        client: AsyncClient,
        sample_profile_data,
        sample_project_data
    ):
        """Test that optional fields can be omitted."""
        # Profile with minimal required fields
        minimal_profile = {
            "full_name": "John Doe",
            "title": "Engineer",
            "email": "john@example.com",
        }
        response = await client.post("/api/v1/profile/", json=minimal_profile)
        assert response.status_code == 201
        data = response.json()
        assert data["phone"] is None
        assert data["bio"] is None
        assert data["tagline"] is None
        
        # Project without optional URLs
        minimal_project = {
            "name": "Minimal Project",
            "slug": "minimal-project",
            "short_description": "A minimal project",
        }
        response = await client.post("/api/v1/projects/", json=minimal_project)
        assert response.status_code == 201
        data = response.json()
        assert data["github_url"] is None
        assert data["demo_url"] is None
    
    async def test_array_field_validation(self, client: AsyncClient, sample_experience_data):
        """Test validation of array fields."""
        # Valid arrays
        experience_with_arrays = sample_experience_data.copy()
        experience_with_arrays["responsibilities"] = ["Task 1", "Task 2"]
        experience_with_arrays["technologies"] = ["Python", "React"]
        response = await client.post("/api/v1/experience/", json=experience_with_arrays)
        assert response.status_code == 201
        data = response.json()
        assert data["responsibilities"] == ["Task 1", "Task 2"]
        assert data["technologies"] == ["Python", "React"]
        
        # Empty arrays should be allowed
        experience_with_arrays["responsibilities"] = []
        experience_with_arrays["technologies"] = []
        response = await client.post("/api/v1/experience/", json=experience_with_arrays)
        assert response.status_code == 201
    
    async def test_boolean_field_validation(self, client: AsyncClient, sample_project_data):
        """Test boolean field handling."""
        # Test explicit true
        project_featured = sample_project_data.copy()
        project_featured["is_featured"] = True
        response = await client.post("/api/v1/projects/", json=project_featured)
        assert response.status_code == 201
        assert response.json()["is_featured"] is True
        
        # Test explicit false
        project_not_featured = sample_project_data.copy()
        project_not_featured["slug"] = "not-featured"
        project_not_featured["is_featured"] = False
        response = await client.post("/api/v1/projects/", json=project_not_featured)
        assert response.status_code == 201
        assert response.json()["is_featured"] is False
    
    async def test_update_validation_partial_data(
        self,
        client: AsyncClient,
        sample_profile_data
    ):
        """Test that partial updates don't require all fields."""
        # Create profile
        await client.post("/api/v1/profile/", json=sample_profile_data)
        
        # Update with only one field
        update_data = {"title": "Senior Engineer"}
        response = await client.patch("/api/v1/profile/", json=update_data)
        assert response.status_code == 200
        data = response.json()
        assert data["title"] == "Senior Engineer"
        assert data["full_name"] == sample_profile_data["full_name"]  # Unchanged
        
        # Update with invalid email should fail
        invalid_update = {"email": "not-an-email"}
        response = await client.patch("/api/v1/profile/", json=invalid_update)
        assert response.status_code == 422
    
    async def test_single_profile_constraint(self, client: AsyncClient, sample_profile_data):
        """Test that only one profile can exist."""
        # Create first profile
        response1 = await client.post("/api/v1/profile/", json=sample_profile_data)
        assert response1.status_code == 201
        
        # Try to create second profile
        second_profile = sample_profile_data.copy()
        second_profile["full_name"] = "Different Person"
        second_profile["email"] = "different@example.com"
        response2 = await client.post("/api/v1/profile/", json=second_profile)
        assert response2.status_code == 409
        assert "already exists" in response2.json()["detail"].lower()
    
    async def test_date_string_format_handling(
        self,
        client: AsyncClient,
        sample_education_data
    ):
        """Test that date strings are accepted in various formats."""
        # Different date formats should all be accepted as strings
        date_formats = ["2024-01", "2024-01-15", "Jan 2024", "2024"]
        
        for i, date_format in enumerate(date_formats):
            edu_data = sample_education_data.copy()
            edu_data["start_date"] = date_format
            edu_data["degree"] = f"Degree {i}"
            response = await client.post("/api/v1/education/", json=edu_data)
            assert response.status_code == 201
            assert response.json()["start_date"] == date_format
    
    async def test_json_field_persistence(self, client: AsyncClient, sample_project_data):
        """Test that JSON fields (arrays, objects) persist correctly."""
        # Create project with arrays
        project_data = sample_project_data.copy()
        project_data["technologies"] = ["Python", "FastAPI", "React", "PostgreSQL"]
        project_data["features"] = ["Authentication", "API", "Admin Panel"]
        
        create_response = await client.post("/api/v1/projects/", json=project_data)
        assert create_response.status_code == 201
        created_id = create_response.json()["id"]
        
        # Retrieve and verify
        get_response = await client.get(f"/api/v1/projects/{created_id}")
        assert get_response.status_code == 200
        data = get_response.json()
        assert data["technologies"] == project_data["technologies"]
        assert data["features"] == project_data["features"]
        
        # Update arrays
        update_data = {"technologies": ["TypeScript", "Node.js"]}
        update_response = await client.patch(f"/api/v1/projects/{created_id}", json=update_data)
        assert update_response.status_code == 200
        assert update_response.json()["technologies"] == ["TypeScript", "Node.js"]
