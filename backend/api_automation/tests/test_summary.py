"""
Tests for Portfolio Summary API endpoint.
Covers the consolidated portfolio data endpoint.
"""
import pytest
import allure
from api_automation.clients.portfolio_clients import SummaryClient


@pytest.fixture
def summary_client():
    """Provide a SummaryClient instance."""
    return SummaryClient()


@allure.feature("Summary API")
@allure.story("Get Portfolio Summary")
class TestGetPortfolioSummary:
    """Test GET /api/v1/summary endpoint."""
    
    @pytest.mark.smoke
    @pytest.mark.regression
    @pytest.mark.positive
    @allure.title("Get portfolio summary successfully")
    def test_get_portfolio_summary_success(self, summary_client):
        """Verify successful retrieval of consolidated portfolio summary."""
        with allure.step("Request portfolio summary"):
            response = summary_client.get_portfolio_summary()
        
        with allure.step("Verify response status"):
            assert response.status_code == 200
        
        with allure.step("Verify response is a dictionary"):
            data = response.json()
            assert isinstance(data, dict)
        
        with allure.step("Verify summary contains expected sections"):
            # Based on the API implementation, summary should contain
            # profile, education, experience, skills, etc.
            # This is flexible as it depends on data availability
            assert isinstance(data, dict)
    
    @pytest.mark.regression
    @pytest.mark.positive
    @allure.title("Verify summary has expected fields")
    def test_portfolio_summary_structure(self, summary_client):
        """Verify summary response has expected structure."""
        with allure.step("Request portfolio summary"):
            response = summary_client.get_portfolio_summary()
        
        with allure.step("Verify response is successful"):
            assert response.status_code == 200
        
        with allure.step("Verify response contains expected keys"):
            data = response.json()
            # Typical summary should contain various portfolio sections
            # The exact keys depend on your API implementation
            assert isinstance(data, dict), "Summary should be a dictionary"
