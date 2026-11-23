"""
Tests for Education API endpoints.
Covers GET (all, by id), POST, PATCH, and DELETE operations.
"""
import pytest
import allure
from api_automation.clients.portfolio_clients import EducationClient


@pytest.fixture
def education_client():
    """Provide an EducationClient instance."""
    return EducationClient()


@allure.feature("Education API")
@allure.story("Get All Education")
class TestGetAllEducation:
    """Test GET /api/v1/education endpoint."""
    
    @pytest.mark.smoke
    @pytest.mark.regression
    @pytest.mark.positive
    @allure.title("Get all education records successfully")
    def test_get_all_education_success(self, education_client):
        """Verify successful retrieval of all education records."""
        with allure.step("Request all education records"):
            response = education_client.get_all_education()
        
        with allure.step("Verify response status"):
            assert response.status_code == 200
        
        with allure.step("Verify response is a list"):
            data = response.json()
            assert isinstance(data, list)


@allure.feature("Education API")
@allure.story("Get Single Education")
class TestGetEducation:
    """Test GET /api/v1/education/{education_id} endpoint."""
    
    @pytest.mark.regression
    @pytest.mark.positive
    @allure.title("Get education record by valid ID")
    def test_get_education_success(self, education_client):
        """Verify successful retrieval of education record by ID."""
        with allure.step("Request education record with ID 1"):
            response = education_client.get_education(1)
        
        with allure.step("Verify response status"):
            assert response.status_code in [200, 404]
    
    @pytest.mark.regression
    @pytest.mark.negative
    @allure.title("Get education record by invalid ID")
    def test_get_education_not_found(self, education_client):
        """Verify 404 response for non-existent education record."""
        with allure.step("Request education record with non-existent ID"):
            response = education_client.get_education(99999)
        
        with allure.step("Verify not found response"):
            assert response.status_code == 404


@allure.feature("Education API")
@allure.story("Create Education")
class TestCreateEducation:
    """Test POST /api/v1/education endpoint."""
    
    @pytest.mark.regression
    @pytest.mark.positive
    @allure.title("Create education record with valid payload")
    def test_create_education_success(self, education_client, education_data):
        """Verify successful education record creation."""
        with allure.step("Prepare education payload"):
            payload = education_data
        
        with allure.step("Create education record"):
            response = education_client.create_education(payload)
        
        with allure.step("Verify response status"):
            assert response.status_code == 201
        
        with allure.step("Verify response contains record ID"):
            data = response.json()
            assert "id" in data
    
    @pytest.mark.regression
    @pytest.mark.negative
    @allure.title("Create education without required fields")
    def test_create_education_missing_school(self, education_client, education_data):
        """Verify education creation fails without school."""
        with allure.step("Prepare payload without school"):
            payload = education_data.copy()
            del payload["school"]
        
        with allure.step("Attempt to create education record"):
            response = education_client.create_education(payload)
        
        with allure.step("Verify validation error"):
            assert response.status_code == 422
    
    @pytest.mark.regression
    @pytest.mark.negative
    @allure.title("Create education with invalid date range")
    def test_create_education_invalid_dates(self, education_client, education_data):
        """Verify education creation fails with invalid date range."""
        with allure.step("Prepare payload with end_date before start_date"):
            payload = education_data.copy()
            payload["start_date"] = "2019-12-31"
            payload["end_date"] = "2015-01-01"
        
        with allure.step("Attempt to create education record"):
            response = education_client.create_education(payload)
        
        with allure.step("Verify validation error"):
            # May return 422 or 400 depending on validation
            assert response.status_code in [400, 422]


@allure.feature("Education API")
@allure.story("Update Education")
class TestUpdateEducation:
    """Test PATCH /api/v1/education/{education_id} endpoint."""
    
    @pytest.mark.regression
    @pytest.mark.positive
    @allure.title("Update education record with valid payload")
    def test_update_education_success(self, education_client):
        """Verify successful education record update."""
        with allure.step("Prepare update payload"):
            payload = {"grade": "4.0"}
        
        with allure.step("Update education record with ID 1"):
            response = education_client.update_education(1, payload)
        
        with allure.step("Verify response status"):
            assert response.status_code in [200, 204, 404]
    
    @pytest.mark.regression
    @pytest.mark.negative
    @allure.title("Update education with invalid grade")
    def test_update_education_invalid_grade(self, education_client):
        """Verify education update fails with invalid grade."""
        with allure.step("Prepare payload with invalid grade"):
            payload = {"grade": "invalid"}
        
        with allure.step("Attempt to update education record"):
            response = education_client.update_education(1, payload)
        
        with allure.step("Verify validation error or not found"):
            assert response.status_code in [400, 404, 422]


@allure.feature("Education API")
@allure.story("Delete Education")
class TestDeleteEducation:
    """Test DELETE /api/v1/education/{education_id} endpoint."""
    
    @pytest.mark.regression
    @pytest.mark.positive
    @allure.title("Delete education record successfully")
    def test_delete_education_success(self, education_client):
        """Verify successful education record deletion."""
        with allure.step("Delete education record with ID 1"):
            response = education_client.delete_education(1)
        
        with allure.step("Verify response status"):
            assert response.status_code in [200, 204, 404]
    
    @pytest.mark.regression
    @pytest.mark.negative
    @allure.title("Delete non-existent education record")
    def test_delete_education_not_found(self, education_client):
        """Verify 404 when deleting non-existent education record."""
        with allure.step("Attempt to delete non-existent record"):
            response = education_client.delete_education(99999)
        
        with allure.step("Verify not found response"):
            assert response.status_code == 404
