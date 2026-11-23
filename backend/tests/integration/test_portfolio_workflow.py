"""
Integration tests for complete portfolio management workflows.
Tests real-world scenarios spanning multiple endpoints.
"""
import pytest
from httpx import AsyncClient
from unittest.mock import patch


@pytest.mark.integration
@pytest.mark.asyncio
class TestPortfolioWorkflow:
    """Integration tests for complete portfolio workflows."""
    
    async def test_complete_portfolio_setup_workflow(
        self,
        client: AsyncClient,
        sample_profile_data,
        sample_education_data,
        sample_experience_data,
        sample_skill_data,
        sample_project_data
    ):
        """Test creating a complete portfolio from scratch."""
        # Step 1: Create profile
        profile_response = await client.post("/api/v1/profile/", json=sample_profile_data)
        assert profile_response.status_code == 201
        profile_id = profile_response.json()["id"]
        
        # Step 2: Add education
        education_response = await client.post("/api/v1/education/", json=sample_education_data)
        assert education_response.status_code == 201
        
        # Step 3: Add experience
        experience_response = await client.post("/api/v1/experience/", json=sample_experience_data)
        assert experience_response.status_code == 201
        
        # Step 4: Add skills
        skills_to_add = [
            {"name": "Python", "category": "Languages", "proficiency": 90, "order": 0},
            {"name": "JavaScript", "category": "Languages", "proficiency": 85, "order": 1},
            {"name": "React", "category": "Frameworks", "proficiency": 80, "order": 0},
        ]
        for skill in skills_to_add:
            skill_response = await client.post("/api/v1/skills/", json=skill)
            assert skill_response.status_code == 201
        
        # Step 5: Add project
        project_response = await client.post("/api/v1/projects/", json=sample_project_data)
        assert project_response.status_code == 201
        
        # Step 6: Verify everything via summary endpoint
        summary_response = await client.get("/api/v1/summary/")
        assert summary_response.status_code == 200
        summary = summary_response.json()
        
        assert summary["profile"]["id"] == profile_id
        assert len(summary["education"]) == 1
        assert len(summary["experience"]) == 1
        assert len(summary["projects"]) == 1
        assert summary["stats"]["total_skills"] == 3
        assert summary["stats"]["skill_categories"] == 2
    
    async def test_update_portfolio_workflow(
        self,
        client: AsyncClient,
        sample_profile_data,
        sample_project_data
    ):
        """Test updating multiple portfolio sections."""
        # Create initial data
        await client.post("/api/v1/profile/", json=sample_profile_data)
        project_response = await client.post("/api/v1/projects/", json=sample_project_data)
        project_id = project_response.json()["id"]
        
        # Update profile
        profile_update = {"title": "Lead Software Engineer", "bio": "Updated bio"}
        update_response = await client.patch("/api/v1/profile/", json=profile_update)
        assert update_response.status_code == 200
        
        # Update project
        project_update = {"status": "archived", "is_featured": False}
        project_update_response = await client.patch(
            f"/api/v1/projects/{project_id}",
            json=project_update
        )
        assert project_update_response.status_code == 200
        
        # Verify updates in summary
        summary = await client.get("/api/v1/summary/")
        data = summary.json()
        assert data["profile"]["title"] == "Lead Software Engineer"
        assert data["profile"]["bio"] == "Updated bio"
        assert data["projects"][0]["status"] == "archived"
        assert data["projects"][0]["is_featured"] is False
        assert data["stats"]["featured_projects"] == 0
    
    @patch('app.routers.contact.email_service.send_contact_email')
    async def test_contact_form_workflow(
        self,
        mock_email,
        client: AsyncClient,
        sample_contact_message_data
    ):
        """Test complete contact form submission and management workflow."""
        mock_email.return_value = True
        
        # Visitor submits contact form
        submit_response = await client.post("/api/v1/contact/", json=sample_contact_message_data)
        assert submit_response.status_code == 201
        message_id = submit_response.json()["id"]
        assert submit_response.json()["is_read"] is False
        
        # Portfolio owner views unread messages
        unread_response = await client.get("/api/v1/contact/messages?is_read=false")
        assert unread_response.status_code == 200
        assert len(unread_response.json()) == 1
        
        # Portfolio owner reads the message
        message_response = await client.get(f"/api/v1/contact/messages/{message_id}")
        assert message_response.status_code == 200
        
        # Portfolio owner marks it as read
        mark_read_response = await client.patch(f"/api/v1/contact/messages/{message_id}/read")
        assert mark_read_response.status_code == 200
        assert mark_read_response.json()["is_read"] is True
        
        # Verify it's no longer in unread list
        unread_after = await client.get("/api/v1/contact/messages?is_read=false")
        assert len(unread_after.json()) == 0
        
        # Verify it's in read list
        read_messages = await client.get("/api/v1/contact/messages?is_read=true")
        assert len(read_messages.json()) == 1
    
    async def test_project_showcase_workflow(
        self,
        client: AsyncClient,
        sample_project_data
    ):
        """Test workflow for managing featured projects showcase."""
        # Create multiple projects
        projects_data = []
        for i in range(5):
            project = sample_project_data.copy()
            project["name"] = f"Project {i}"
            project["slug"] = f"project-{i}"
            project["is_featured"] = i < 3  # First 3 are featured
            project["order"] = i
            response = await client.post("/api/v1/projects/", json=project)
            assert response.status_code == 201
            projects_data.append(response.json())
        
        # Get featured projects for homepage
        featured_response = await client.get("/api/v1/projects/featured")
        assert featured_response.status_code == 200
        featured = featured_response.json()
        assert len(featured) == 3
        
        # Unfeature one project
        await client.patch(
            f"/api/v1/projects/{projects_data[0]['id']}",
            json={"is_featured": False}
        )
        
        # Feature a new one
        await client.patch(
            f"/api/v1/projects/{projects_data[3]['id']}",
            json={"is_featured": True}
        )
        
        # Verify featured count unchanged
        featured_after = await client.get("/api/v1/projects/featured")
        assert len(featured_after.json()) == 3
        
        # Verify in summary
        summary = await client.get("/api/v1/summary/")
        assert summary.json()["stats"]["featured_projects"] == 3
    
    async def test_skills_organization_workflow(self, client: AsyncClient):
        """Test organizing skills by categories."""
        # Add skills across multiple categories
        skills = [
            # Languages
            {"name": "Python", "category": "Languages", "proficiency": 90, "order": 0},
            {"name": "JavaScript", "category": "Languages", "proficiency": 85, "order": 1},
            {"name": "TypeScript", "category": "Languages", "proficiency": 80, "order": 2},
            # Frameworks
            {"name": "React", "category": "Frameworks", "proficiency": 85, "order": 0},
            {"name": "FastAPI", "category": "Frameworks", "proficiency": 90, "order": 1},
            # Tools
            {"name": "Docker", "category": "Tools", "proficiency": 75, "order": 0},
            {"name": "Git", "category": "Tools", "proficiency": 90, "order": 1},
        ]
        
        for skill in skills:
            response = await client.post("/api/v1/skills/", json=skill)
            assert response.status_code == 201
        
        # Get grouped skills
        grouped_response = await client.get("/api/v1/skills/grouped")
        assert grouped_response.status_code == 200
        grouped = grouped_response.json()["categories"]
        
        assert len(grouped["Languages"]) == 3
        assert len(grouped["Frameworks"]) == 2
        assert len(grouped["Tools"]) == 2
        
        # Get categories list
        categories_response = await client.get("/api/v1/skills/categories")
        assert categories_response.status_code == 200
        categories = categories_response.json()["categories"]
        assert "Languages" in categories
        assert "Frameworks" in categories
        assert "Tools" in categories
        
        # Filter by category
        languages_response = await client.get("/api/v1/skills/?category=Languages")
        assert len(languages_response.json()) == 3
    
    async def test_education_timeline_workflow(
        self,
        client: AsyncClient,
        sample_education_data
    ):
        """Test building education timeline with ordering."""
        # Add education in reverse chronological order
        education_records = [
            {**sample_education_data, "degree": "PhD", "start_date": "2024-09", "order": 0},
            {**sample_education_data, "degree": "Master's", "start_date": "2022-09", "end_date": "2024-05", "order": 1},
            {**sample_education_data, "degree": "Bachelor's", "start_date": "2018-09", "end_date": "2022-05", "order": 2},
        ]
        
        for edu in education_records:
            response = await client.post("/api/v1/education/", json=edu)
            assert response.status_code == 201
        
        # Get all education (should be ordered)
        all_edu = await client.get("/api/v1/education/")
        data = all_edu.json()
        assert len(data) == 3
        assert data[0]["degree"] == "PhD"
        assert data[1]["degree"] == "Master's"
        assert data[2]["degree"] == "Bachelor's"
        
        # Verify in summary
        summary = await client.get("/api/v1/summary/")
        edu_in_summary = summary.json()["education"]
        assert edu_in_summary[0]["degree"] == "PhD"
    
    async def test_experience_filtering_workflow(
        self,
        client: AsyncClient,
        sample_experience_data
    ):
        """Test filtering experience by type and status."""
        # Create diverse experience records
        experiences = [
            {**sample_experience_data, "title": "Senior Engineer", "employment_type": "Full-time", "is_current": True, "end_date": None},
            {**sample_experience_data, "title": "Junior Engineer", "employment_type": "Full-time", "is_current": False, "end_date": "2020-12"},
            {**sample_experience_data, "title": "Summer Intern", "employment_type": "Internship", "is_current": False, "end_date": "2019-08"},
            {**sample_experience_data, "title": "Part-time Dev", "employment_type": "Part-time", "is_current": False, "end_date": "2018-12"},
        ]
        
        for exp in experiences:
            response = await client.post("/api/v1/experience/", json=exp)
            assert response.status_code == 201
        
        # Get all experience
        all_exp = await client.get("/api/v1/experience/")
        assert len(all_exp.json()) == 4
        
        # Filter by current
        current_exp = await client.get("/api/v1/experience/?is_current=true")
        assert len(current_exp.json()) == 1
        assert current_exp.json()[0]["title"] == "Senior Engineer"
        
        # Filter by employment type
        internships = await client.get("/api/v1/experience/?employment_type=Internship")
        assert len(internships.json()) == 1
        assert internships.json()[0]["title"] == "Summer Intern"
        
        # Verify stats
        summary = await client.get("/api/v1/summary/")
        assert summary.json()["stats"]["years_of_experience"] == 4
    
    async def test_delete_cascade_workflow(
        self,
        client: AsyncClient,
        sample_profile_data,
        sample_education_data,
        sample_project_data
    ):
        """Test deleting multiple portfolio items."""
        # Create portfolio
        await client.post("/api/v1/profile/", json=sample_profile_data)
        edu_response = await client.post("/api/v1/education/", json=sample_education_data)
        proj_response = await client.post("/api/v1/projects/", json=sample_project_data)
        
        edu_id = edu_response.json()["id"]
        proj_id = proj_response.json()["id"]
        
        # Verify initial state
        initial_summary = await client.get("/api/v1/summary/")
        assert initial_summary.json()["profile"] is not None
        assert len(initial_summary.json()["education"]) == 1
        assert len(initial_summary.json()["projects"]) == 1
        
        # Delete education
        delete_edu = await client.delete(f"/api/v1/education/{edu_id}")
        assert delete_edu.status_code == 200
        
        # Delete project
        delete_proj = await client.delete(f"/api/v1/projects/{proj_id}")
        assert delete_proj.status_code == 200
        
        # Verify deletions in summary
        after_summary = await client.get("/api/v1/summary/")
        assert after_summary.json()["profile"] is not None  # Profile still exists
        assert len(after_summary.json()["education"]) == 0
        assert len(after_summary.json()["projects"]) == 0
        
        # Delete profile
        delete_profile = await client.delete("/api/v1/profile/")
        assert delete_profile.status_code == 200
        
        # Verify complete cleanup
        final_summary = await client.get("/api/v1/summary/")
        assert final_summary.json()["profile"] is None
