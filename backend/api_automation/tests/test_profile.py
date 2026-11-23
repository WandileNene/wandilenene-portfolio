"""
Tests for Profile API endpoints.
Covers GET, POST, PATCH, and DELETE operations.
"""
import pytest
import allure
from api_automation.clients.portfolio_clients import ProfileClient


@pytest.fixture
def profile_client():
    """Provide a ProfileClient instance."""
    return ProfileClient()


@allure.feature("Profile API")
@allure.story("Get Profile")
class TestGetProfile:
    """Test GET /api/v1/profile endpoint."""
    
    @pytest.mark.smoke
    @pytest.mark.regression
    @pytest.mark.positive
    @allure.title("Get profile successfully")
    def test_get_profile_success(self, profile_client):
        """Verify successful profile retrieval."""
        with allure.step("Request profile"):
            response = profile_client.get_profile()
        
        with allure.step("Verify response status"):
            assert response.status_code == 200, f"Expected 200, got {response.status_code}"
        
        with allure.step("Verify response structure"):
            data = response.json()
            assert isinstance(data, dict), "Response should be a dictionary"
            # Based on ProfileResponse schema
            assert "id" in data or "email" in data or data == {}, "Response should contain profile data or be empty"


@allure.feature("Profile API")
@allure.story("Create Profile")
class TestCreateProfile:
    """Test POST /api/v1/profile endpoint."""
    
    @pytest.mark.regression
    @pytest.mark.positive
    @allure.title("Create profile with valid payload")
    def test_create_profile_success(self, profile_client, profile_data):
        """Verify successful profile creation."""
        with allure.step("Prepare profile payload"):
            payload = profile_data
        
        with allure.step("Create profile"):
            response = profile_client.create_profile(payload)
        
        with allure.step("Verify response status"):
            assert response.status_code == 201, f"Expected 201, got {response.status_code}"
        
        with allure.step("Verify response contains created profile"):
            data = response.json()
            assert isinstance(data, dict), "Response should be a dictionary"
    
    @pytest.mark.regression
    @pytest.mark.negative
    @allure.title("Create profile with invalid email")
    def test_create_profile_invalid_email(self, profile_client, profile_data):
        """Verify profile creation fails with invalid email."""
        with allure.step("Prepare invalid profile payload"):
            payload = profile_data.copy()
            payload["email"] = "invalid-email"
        
        with allure.step("Attempt to create profile"):
            response = profile_client.create_profile(payload)
        
        with allure.step("Verify validation error"):
            assert response.status_code == 422, f"Expected 422, got {response.status_code}"
            error_data = response.json()
            assert "errors" in error_data or "detail" in error_data
    
    @pytest.mark.regression
    @pytest.mark.negative
    @allure.title("Create profile with missing required fields")
    def test_create_profile_missing_email(self, profile_client, profile_data):
        """Verify profile creation fails when email is missing."""
        with allure.step("Prepare payload without email"):
            payload = profile_data.copy()
            del payload["email"]
        
        with allure.step("Attempt to create profile"):
            response = profile_client.create_profile(payload)
        
        with allure.step("Verify validation error"):
            assert response.status_code == 422, f"Expected 422, got {response.status_code}"


@allure.feature("Profile API")
@allure.story("Update Profile")
class TestUpdateProfile:
    """Test PATCH /api/v1/profile endpoint."""
    
    @pytest.mark.regression
    @pytest.mark.positive
    @allure.title("Update profile with valid payload")
    def test_update_profile_success(self, profile_client, profile_data):
        """Verify successful profile update."""
        with allure.step("Prepare update payload"):
            payload = {"bio": "Updated bio"}
        
        with allure.step("Update profile"):
            response = profile_client.update_profile(payload)
        
        with allure.step("Verify response status"):
            assert response.status_code in [200, 204], f"Expected 200 or 204, got {response.status_code}"
    
    @pytest.mark.regression
    @pytest.mark.negative
    @allure.title("Update profile with invalid email")
    def test_update_profile_invalid_email(self, profile_client):
        """Verify profile update fails with invalid email."""
        with allure.step("Prepare invalid update payload"):
            payload = {"email": "not-an-email"}
        
        with allure.step("Attempt to update profile"):
            response = profile_client.update_profile(payload)
        
        with allure.step("Verify validation error"):
            assert response.status_code == 422, f"Expected 422, got {response.status_code}"


@allure.feature("Profile API")
@allure.story("Delete Profile")
class TestDeleteProfile:
    """Test DELETE /api/v1/profile endpoint."""
    
    @pytest.mark.regression
    @pytest.mark.positive
    @allure.title("Delete profile successfully")
    def test_delete_profile_success(self, profile_client):
        """Verify successful profile deletion."""
        with allure.step("Delete profile"):
            response = profile_client.delete_profile()
        
        with allure.step("Verify response status"):
            assert response.status_code in [200, 204], f"Expected 200 or 204, got {response.status_code}"
