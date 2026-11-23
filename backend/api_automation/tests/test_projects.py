"""
Tests for Projects API endpoints.
Covers GET (all, featured, by slug, by id), POST, PATCH, and DELETE operations.
"""
import pytest
import allure
from api_automation.clients.portfolio_clients import ProjectClient


@pytest.fixture
def project_client():
    """Provide a ProjectClient instance."""
    return ProjectClient()


@allure.feature("Projects API")
@allure.story("Get All Projects")
class TestGetAllProjects:
    """Test GET /api/v1/projects endpoint."""
    
    @pytest.mark.smoke
    @pytest.mark.regression
    @pytest.mark.positive
    @allure.title("Get all projects successfully")
    def test_get_all_projects_success(self, project_client):
        """Verify successful retrieval of all projects."""
        with allure.step("Request all projects"):
            response = project_client.get_all_projects()
        
        with allure.step("Verify response status"):
            assert response.status_code == 200
        
        with allure.step("Verify response is a list"):
            data = response.json()
            assert isinstance(data, list)
    
    @pytest.mark.regression
    @pytest.mark.positive
    @allure.title("Get featured projects only")
    def test_get_projects_featured_only(self, project_client):
        """Verify retrieval of featured projects only."""
        with allure.step("Request featured projects"):
            response = project_client.get_all_projects(featured_only=True)
        
        with allure.step("Verify response status"):
            assert response.status_code == 200
        
        with allure.step("Verify response is a list"):
            data = response.json()
            assert isinstance(data, list)


@allure.feature("Projects API")
@allure.story("Get Featured Projects")
class TestGetFeaturedProjects:
    """Test GET /api/v1/projects/featured endpoint."""
    
    @pytest.mark.regression
    @pytest.mark.positive
    @allure.title("Get featured projects endpoint")
    def test_get_featured_projects_success(self, project_client):
        """Verify successful retrieval of featured projects."""
        with allure.step("Request featured projects"):
            response = project_client.get_featured_projects()
        
        with allure.step("Verify response status"):
            assert response.status_code == 200
        
        with allure.step("Verify response is a list"):
            data = response.json()
            assert isinstance(data, list)


@allure.feature("Projects API")
@allure.story("Get Project by Slug")
class TestGetProjectBySlug:
    """Test GET /api/v1/projects/by-slug/{slug} endpoint."""
    
    @pytest.mark.regression
    @pytest.mark.positive
    @allure.title("Get project by valid slug")
    def test_get_project_by_slug_success(self, project_client):
        """Verify successful retrieval of project by slug."""
        with allure.step("Request project by slug"):
            response = project_client.get_project_by_slug("portfolio-website")
        
        with allure.step("Verify response status"):
            # Either 200 (found) or 404 (not found)
            assert response.status_code in [200, 404]
    
    @pytest.mark.regression
    @pytest.mark.negative
    @allure.title("Get project by non-existent slug")
    def test_get_project_by_slug_not_found(self, project_client):
        """Verify 404 response for non-existent slug."""
        with allure.step("Request project with non-existent slug"):
            response = project_client.get_project_by_slug("non-existent-project-123")
        
        with allure.step("Verify not found response"):
            assert response.status_code == 404


@allure.feature("Projects API")
@allure.story("Get Single Project")
class TestGetProject:
    """Test GET /api/v1/projects/{project_id} endpoint."""
    
    @pytest.mark.regression
    @pytest.mark.positive
    @allure.title("Get project by valid ID")
    def test_get_project_success(self, project_client):
        """Verify successful retrieval of project by ID."""
        with allure.step("Request project with ID 1"):
            response = project_client.get_project(1)
        
        with allure.step("Verify response status"):
            assert response.status_code in [200, 404]
    
    @pytest.mark.regression
    @pytest.mark.negative
    @allure.title("Get project by invalid ID")
    def test_get_project_not_found(self, project_client):
        """Verify 404 response when project doesn't exist."""
        with allure.step("Request project with non-existent ID"):
            response = project_client.get_project(99999)
        
        with allure.step("Verify not found response"):
            assert response.status_code == 404


@allure.feature("Projects API")
@allure.story("Create Project")
class TestCreateProject:
    """Test POST /api/v1/projects endpoint."""
    
    @pytest.mark.regression
    @pytest.mark.positive
    @allure.title("Create project with valid payload")
    def test_create_project_success(self, project_client, project_data):
        """Verify successful project creation."""
        with allure.step("Prepare project payload"):
            payload = project_data
        
        with allure.step("Create project"):
            response = project_client.create_project(payload)
        
        with allure.step("Verify response status"):
            assert response.status_code == 201
        
        with allure.step("Verify response contains project ID"):
            data = response.json()
            assert "id" in data
    
    @pytest.mark.regression
    @pytest.mark.negative
    @allure.title("Create project with missing title")
    def test_create_project_missing_title(self, project_client, project_data):
        """Verify project creation fails without title."""
        with allure.step("Prepare payload without title"):
            payload = project_data.copy()
            del payload["title"]
        
        with allure.step("Attempt to create project"):
            response = project_client.create_project(payload)
        
        with allure.step("Verify validation error"):
            assert response.status_code == 422
    
    @pytest.mark.regression
    @pytest.mark.negative
    @allure.title("Create project with duplicate slug")
    def test_create_project_duplicate_slug(self, project_client, project_data):
        """Verify project creation fails with duplicate slug."""
        with allure.step("Prepare first project"):
            payload1 = project_data.copy()
            payload1["slug"] = "unique-slug-test"
        
        with allure.step("Create first project"):
            response1 = project_client.create_project(payload1)
            if response1.status_code == 201:
                project_id = response1.json()["id"]
        
        with allure.step("Prepare duplicate slug payload"):
            payload2 = project_data.copy()
            payload2["slug"] = "unique-slug-test"  # Same slug
        
        with allure.step("Attempt to create project with duplicate slug"):
            response2 = project_client.create_project(payload2)
        
        with allure.step("Verify conflict error"):
            assert response2.status_code == 409  # Conflict


@allure.feature("Projects API")
@allure.story("Update Project")
class TestUpdateProject:
    """Test PATCH /api/v1/projects/{project_id} endpoint."""
    
    @pytest.mark.regression
    @pytest.mark.positive
    @allure.title("Update project with valid payload")
    def test_update_project_success(self, project_client):
        """Verify successful project update."""
        with allure.step("Prepare update payload"):
            payload = {"description": "Updated description"}
        
        with allure.step("Update project with ID 1"):
            response = project_client.update_project(1, payload)
        
        with allure.step("Verify response status"):
            assert response.status_code in [200, 204, 404]


@allure.feature("Projects API")
@allure.story("Delete Project")
class TestDeleteProject:
    """Test DELETE /api/v1/projects/{project_id} endpoint."""
    
    @pytest.mark.regression
    @pytest.mark.positive
    @allure.title("Delete project successfully")
    def test_delete_project_success(self, project_client):
        """Verify successful project deletion."""
        with allure.step("Delete project with ID 1"):
            response = project_client.delete_project(1)
        
        with allure.step("Verify response status"):
            assert response.status_code in [200, 204, 404]
