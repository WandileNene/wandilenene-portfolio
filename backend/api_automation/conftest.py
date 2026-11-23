"""
Pytest configuration and fixtures for API automation framework.
Provides common fixtures for API clients, test data, and configuration.
"""
import os
import pytest
import allure
from api_automation.config import get_config, set_config, Config
from api_automation.utils import setup_logging


# Configure logging when pytest starts
def pytest_configure(config):
    """Configure pytest and logging."""
    # Setup logging
    log_level = os.getenv("LOG_LEVEL", "INFO")
    setup_logging(log_level)
    
    # Load configuration
    env = os.getenv("API_ENV", "dev")
    app_config = Config.from_env(env)
    set_config(app_config)


@pytest.fixture(scope="session")
def api_config():
    """
    Provide API configuration for the test session.
    
    Returns:
        Config instance.
    """
    return get_config()


@pytest.fixture(autouse=True)
def attach_test_metadata():
    """Automatically attach test information to Allure report."""
    # This will be overridden by specific tests with more details
    yield


@pytest.fixture
def api_base_url():
    """
    Provide base URL for API requests.
    
    Returns:
        Base URL string.
    """
    return get_config().base_url


# Example test data fixtures (extend as needed)
@pytest.fixture
def profile_data():
    """Sample profile data for tests."""
    return {
        "first_name": "Wandile",
        "last_name": "Nene",
        "email": "wandile@example.com",
        "phone": "+27 123 456 7890",
        "location": "Johannesburg, South Africa",
        "bio": "Senior Software Engineer",
        "photo_url": "https://example.com/photo.jpg",
        "cv_url": "https://example.com/cv.pdf",
    }


@pytest.fixture
def education_data():
    """Sample education data for tests."""
    return {
        "school": "University of the Witwatersrand",
        "degree": "Bachelor of Science",
        "field_of_study": "Computer Science",
        "start_date": "2015-01-01",
        "end_date": "2019-12-31",
        "grade": "3.8",
        "description": "Specialized in software engineering",
    }


@pytest.fixture
def experience_data():
    """Sample experience data for tests."""
    return {
        "company": "Tech Company",
        "position": "Software Engineer",
        "employment_type": "Full-time",
        "location": "Johannesburg",
        "start_date": "2020-01-01",
        "end_date": "2023-12-31",
        "description": "Developed web applications",
        "skills": ["Python", "JavaScript", "React"],
    }


@pytest.fixture
def skill_data():
    """Sample skill data for tests."""
    return {
        "name": "Python",
        "category": "Programming Languages",
        "proficiency": 90,
        "endorsements": 10,
    }


@pytest.fixture
def project_data():
    """Sample project data for tests."""
    return {
        "title": "Portfolio Website",
        "slug": "portfolio-website",
        "description": "Personal portfolio website built with React",
        "technologies": ["React", "TypeScript", "FastAPI"],
        "start_date": "2023-06-01",
        "end_date": "2023-12-31",
        "github_url": "https://github.com/example/portfolio",
        "live_url": "https://portfolio.example.com",
        "featured": True,
    }


@pytest.fixture
def achievement_data():
    """Sample achievement data for tests."""
    return {
        "title": "Best Developer Award",
        "issuer": "Tech Company",
        "issue_date": "2023-06-15",
        "description": "Awarded for outstanding contributions",
    }


@pytest.fixture
def certification_data():
    """Sample certification data for tests."""
    return {
        "name": "AWS Solutions Architect",
        "issuer": "Amazon Web Services",
        "issue_date": "2023-01-15",
        "expiration_date": "2025-01-15",
        "credential_url": "https://aws.example.com/credential",
    }


@pytest.fixture
def contact_message_data():
    """Sample contact message data for tests."""
    return {
        "name": "John Doe",
        "email": "john@example.com",
        "subject": "Collaboration Inquiry",
        "message": "I'm interested in collaborating on a project.",
    }
