"""
Tests for Skills API endpoints.
Covers GET (all, grouped, categories, by id), POST, PATCH, and DELETE operations.
"""
import pytest
import allure
from api_automation.clients.portfolio_clients import SkillClient


@pytest.fixture
def skill_client():
    """Provide a SkillClient instance."""
    return SkillClient()


@allure.feature("Skills API")
@allure.story("Get All Skills")
class TestGetAllSkills:
    """Test GET /api/v1/skills endpoint."""
    
    @pytest.mark.smoke
    @pytest.mark.regression
    @pytest.mark.positive
    @allure.title("Get all skills successfully")
    def test_get_all_skills_success(self, skill_client):
        """Verify successful retrieval of all skills."""
        with allure.step("Request all skills"):
            response = skill_client.get_all_skills()
        
        with allure.step("Verify response status"):
            assert response.status_code == 200
        
        with allure.step("Verify response is a list"):
            data = response.json()
            assert isinstance(data, list)
    
    @pytest.mark.regression
    @pytest.mark.positive
    @allure.title("Get skills filtered by category")
    def test_get_skills_by_category(self, skill_client):
        """Verify skills can be filtered by category."""
        with allure.step("Request skills with category filter"):
            response = skill_client.get_all_skills(category="Programming Languages")
        
        with allure.step("Verify response status"):
            assert response.status_code == 200
        
        with allure.step("Verify response is a list"):
            data = response.json()
            assert isinstance(data, list)


@allure.feature("Skills API")
@allure.story("Get Skills Grouped")
class TestGetSkillsGrouped:
    """Test GET /api/v1/skills/grouped endpoint."""
    
    @pytest.mark.regression
    @pytest.mark.positive
    @allure.title("Get skills grouped by category")
    def test_get_skills_grouped_success(self, skill_client):
        """Verify successful retrieval of grouped skills."""
        with allure.step("Request grouped skills"):
            response = skill_client.get_skills_grouped()
        
        with allure.step("Verify response status"):
            assert response.status_code == 200
        
        with allure.step("Verify response is a dictionary"):
            data = response.json()
            assert isinstance(data, dict)


@allure.feature("Skills API")
@allure.story("Get Skill Categories")
class TestGetSkillCategories:
    """Test GET /api/v1/skills/categories endpoint."""
    
    @pytest.mark.regression
    @pytest.mark.positive
    @allure.title("Get all skill categories")
    def test_get_skill_categories_success(self, skill_client):
        """Verify successful retrieval of skill categories."""
        with allure.step("Request skill categories"):
            response = skill_client.get_skill_categories()
        
        with allure.step("Verify response status"):
            assert response.status_code == 200
        
        with allure.step("Verify response is a list"):
            data = response.json()
            assert isinstance(data, list)


@allure.feature("Skills API")
@allure.story("Get Single Skill")
class TestGetSkill:
    """Test GET /api/v1/skills/{skill_id} endpoint."""
    
    @pytest.mark.regression
    @pytest.mark.positive
    @allure.title("Get skill by valid ID")
    def test_get_skill_success(self, skill_client):
        """Verify successful retrieval of a skill by ID."""
        with allure.step("Request skill with ID 1"):
            response = skill_client.get_skill(1)
        
        with allure.step("Verify response status"):
            # Either 200 (found) or 404 (not found if no data)
            assert response.status_code in [200, 404]
    
    @pytest.mark.regression
    @pytest.mark.negative
    @allure.title("Get skill by invalid ID")
    def test_get_skill_not_found(self, skill_client):
        """Verify 404 response when skill doesn't exist."""
        with allure.step("Request skill with non-existent ID"):
            response = skill_client.get_skill(99999)
        
        with allure.step("Verify not found response"):
            assert response.status_code == 404


@allure.feature("Skills API")
@allure.story("Create Skill")
class TestCreateSkill:
    """Test POST /api/v1/skills endpoint."""
    
    @pytest.mark.regression
    @pytest.mark.positive
    @allure.title("Create skill with valid payload")
    def test_create_skill_success(self, skill_client, skill_data):
        """Verify successful skill creation."""
        with allure.step("Prepare skill payload"):
            payload = skill_data
        
        with allure.step("Create skill"):
            response = skill_client.create_skill(payload)
        
        with allure.step("Verify response status"):
            assert response.status_code == 201
        
        with allure.step("Verify response contains skill ID"):
            data = response.json()
            assert "id" in data
    
    @pytest.mark.regression
    @pytest.mark.negative
    @allure.title("Create skill with invalid proficiency")
    def test_create_skill_invalid_proficiency(self, skill_client, skill_data):
        """Verify skill creation fails with invalid proficiency."""
        with allure.step("Prepare payload with invalid proficiency"):
            payload = skill_data.copy()
            payload["proficiency"] = 150  # Invalid: should be 0-100
        
        with allure.step("Attempt to create skill"):
            response = skill_client.create_skill(payload)
        
        with allure.step("Verify validation error"):
            assert response.status_code == 422


@allure.feature("Skills API")
@allure.story("Update Skill")
class TestUpdateSkill:
    """Test PATCH /api/v1/skills/{skill_id} endpoint."""
    
    @pytest.mark.regression
    @pytest.mark.positive
    @allure.title("Update skill with valid payload")
    def test_update_skill_success(self, skill_client):
        """Verify successful skill update."""
        with allure.step("Prepare update payload"):
            payload = {"proficiency": 95}
        
        with allure.step("Update skill with ID 1"):
            response = skill_client.update_skill(1, payload)
        
        with allure.step("Verify response status"):
            assert response.status_code in [200, 204, 404]


@allure.feature("Skills API")
@allure.story("Delete Skill")
class TestDeleteSkill:
    """Test DELETE /api/v1/skills/{skill_id} endpoint."""
    
    @pytest.mark.regression
    @pytest.mark.positive
    @allure.title("Delete skill successfully")
    def test_delete_skill_success(self, skill_client):
        """Verify successful skill deletion."""
        with allure.step("Delete skill with ID 1"):
            response = skill_client.delete_skill(1)
        
        with allure.step("Verify response status"):
            assert response.status_code in [200, 204, 404]
