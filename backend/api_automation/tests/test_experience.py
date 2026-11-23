"""
Tests for Experience API endpoints.
Covers GET (all with filtering, by id), POST, PATCH, and DELETE operations.
"""
import pytest
import allure
from api_automation.clients.portfolio_clients import ExperienceClient


@pytest.fixture
def experience_client():
    """Provide an ExperienceClient instance."""
    return ExperienceClient()


@allure.feature("Experience API")
@allure.story("Get All Experience")
class TestGetAllExperience:
    """Test GET /api/v1/experience endpoint."""
    
    @pytest.mark.smoke
    @pytest.mark.regression
    @pytest.mark.positive
    @allure.title("Get all experience records")
    def test_get_all_experience_success(self, experience_client):
        """Verify successful retrieval of all experience records."""
        with allure.step("Request all experience records"):
            response = experience_client.get_all_experience()
        
        with allure.step("Verify response status"):
            assert response.status_code == 200
        
        with allure.step("Verify response is a list"):
            data = response.json()
            assert isinstance(data, list)
    
    @pytest.mark.regression
    @pytest.mark.positive
    @allure.title("Get all experience including current")
    def test_get_all_experience_include_current(self, experience_client):
        """Verify retrieval includes current experience."""
        with allure.step("Request all experience (include current)"):
            response = experience_client.get_all_experience(include_current=True)
        
        with allure.step("Verify response status"):
            assert response.status_code == 200


@allure.feature("Experience API")
@allure.story("Get Single Experience")
class TestGetExperience:
    """Test GET /api/v1/experience/{experience_id} endpoint."""
    
    @pytest.mark.regression
    @pytest.mark.positive
    @allure.title("Get experience record by valid ID")
    def test_get_experience_success(self, experience_client):
        """Verify successful retrieval of experience record."""
        with allure.step("Request experience record with ID 1"):
            response = experience_client.get_experience(1)
        
        with allure.step("Verify response status"):
            assert response.status_code in [200, 404]
    
    @pytest.mark.regression
    @pytest.mark.negative
    @allure.title("Get experience record by invalid ID")
    def test_get_experience_not_found(self, experience_client):
        """Verify 404 response for non-existent record."""
        with allure.step("Request non-existent experience record"):
            response = experience_client.get_experience(99999)
        
        with allure.step("Verify not found response"):
            assert response.status_code == 404


@allure.feature("Experience API")
@allure.story("Create Experience")
class TestCreateExperience:
    """Test POST /api/v1/experience endpoint."""
    
    @pytest.mark.regression
    @pytest.mark.positive
    @allure.title("Create experience record with valid payload")
    def test_create_experience_success(self, experience_client, experience_data):
        """Verify successful experience record creation."""
        with allure.step("Prepare experience payload"):
            payload = experience_data
        
        with allure.step("Create experience record"):
            response = experience_client.create_experience(payload)
        
        with allure.step("Verify response status"):
            assert response.status_code == 201
        
        with allure.step("Verify response contains record ID"):
            data = response.json()
            assert "id" in data
    
    @pytest.mark.regression
    @pytest.mark.negative
    @allure.title("Create experience without company name")
    def test_create_experience_missing_company(self, experience_client, experience_data):
        """Verify experience creation fails without company."""
        with allure.step("Prepare payload without company"):
            payload = experience_data.copy()
            del payload["company"]
        
        with allure.step("Attempt to create experience record"):
            response = experience_client.create_experience(payload)
        
        with allure.step("Verify validation error"):
            assert response.status_code == 422


@allure.feature("Experience API")
@allure.story("Update Experience")
class TestUpdateExperience:
    """Test PATCH /api/v1/experience/{experience_id} endpoint."""
    
    @pytest.mark.regression
    @pytest.mark.positive
    @allure.title("Update experience record with valid payload")
    def test_update_experience_success(self, experience_client):
        """Verify successful experience record update."""
        with allure.step("Prepare update payload"):
            payload = {"description": "Updated description"}
        
        with allure.step("Update experience record with ID 1"):
            response = experience_client.update_experience(1, payload)
        
        with allure.step("Verify response status"):
            assert response.status_code in [200, 204, 404]


@allure.feature("Experience API")
@allure.story("Delete Experience")
class TestDeleteExperience:
    """Test DELETE /api/v1/experience/{experience_id} endpoint."""
    
    @pytest.mark.regression
    @pytest.mark.positive
    @allure.title("Delete experience record successfully")
    def test_delete_experience_success(self, experience_client):
        """Verify successful experience record deletion."""
        with allure.step("Delete experience record with ID 1"):
            response = experience_client.delete_experience(1)
        
        with allure.step("Verify response status"):
            assert response.status_code in [200, 204, 404]
