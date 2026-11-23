# API Automation Framework

A comprehensive, maintainable REST API automation framework built with Python, Pytest, and Allure reporting.

## Overview

This framework provides a clean, scalable approach to automate REST API testing for the Portfolio API. It features:

- **Reusable API Clients**: Specialized clients for each API endpoint with common HTTP functionality
- **Comprehensive Test Suite**: Positive and negative test scenarios for all endpoints
- **Allure Reporting**: Detailed, beautiful test reports with request/response information
- **Environment Configuration**: Easy switching between dev, qa, and staging environments
- **Logging & Debugging**: Structured logging with sensitive data filtering
- **PEP 8 Compliant**: Clean, professional code structure

## Prerequisites

- Python 3.8+
- pip (Python package manager)
- Virtual environment tool (venv)

## Quick Start

### 1. Setup Virtual Environment

```bash
# Navigate to backend directory
cd backend

# Create virtual environment
python -m venv venv

# Activate virtual environment
# On Windows:
venv\Scripts\activate
# On macOS/Linux:
source venv/bin/activate
```

### 2. Install Dependencies

```bash
pip install -r requirements.txt
```

### 3. Configure Environment

```bash
# Copy the example environment file
cp api_automation/.env.example api_automation/.env

# Edit .env with your configuration
# Default dev environment uses http://localhost:8000
```

### 4. Run Tests

```bash
# Run all tests
pytest api_automation/

# Run with verbose output
pytest api_automation/ -v

# Run specific test file
pytest api_automation/tests/test_profile.py -v

# Run specific test class
pytest api_automation/tests/test_profile.py::TestCreateProfile -v

# Run specific test
pytest api_automation/tests/test_profile.py::TestCreateProfile::test_create_profile_success -v
```

## Running Tests by Marker

Tests are organized by markers for easy filtering:

```bash
# Run smoke tests (quick sanity checks)
pytest api_automation/ -m smoke

# Run regression tests (full suite)
pytest api_automation/ -m regression

# Run positive tests only (happy path)
pytest api_automation/ -m positive

# Run negative tests only (error scenarios)
pytest api_automation/ -m negative

# Combine markers (AND logic)
pytest api_automation/ -m "smoke and positive"

# Exclude markers
pytest api_automation/ -m "not slow"
```

## Generating Allure Reports

### Generate Report

```bash
# Run tests and generate Allure results
pytest api_automation/ --alluredir=allure-results

# Or use the built-in pytest.ini configuration
pytest api_automation/
```

### View Report

```bash
# Serve the report locally (requires Allure command line)
allure serve allure-results

# Or generate HTML report
allure generate allure-results -o allure-report
# Then open allure-report/index.html in browser
```

## Project Structure

```
api_automation/
├── clients/                      # API client implementations
│   ├── __init__.py
│   ├── base_client.py           # BaseAPIClient with common HTTP methods
│   └── portfolio_clients.py      # Specialized clients (Profile, Skills, etc.)
│
├── tests/                        # Test files
│   ├── __init__.py
│   ├── test_profile.py          # Profile API tests
│   ├── test_education.py        # Education API tests
│   ├── test_experience.py       # Experience API tests
│   ├── test_skills.py           # Skills API tests
│   ├── test_projects.py         # Projects API tests
│   ├── test_contact.py          # Contact API tests
│   ├── test_summary.py          # Summary API tests
│   └── ...
│
├── utils/                        # Utilities
│   ├── __init__.py
│   └── logging_config.py        # Logging configuration & setup
│
├── __init__.py                  # Package initialization
├── config.py                    # Configuration management
├── conftest.py                  # Pytest fixtures & configuration
├── pytest.ini                   # Pytest configuration file
├── .env.example                 # Environment variables template
├── README.md                    # This file
└── allure-results/              # Generated Allure results (gitignored)
```

## Adding New API Tests

### Step 1: Create API Client (if new API)

Add to `clients/portfolio_clients.py`:

```python
class YourAPIClient(BaseAPIClient):
    """Client for Your API endpoints."""
    
    def get_all_items(self) -> APIResponse:
        """Get all items."""
        return self.get("/your-endpoint")
    
    def get_item(self, item_id: int) -> APIResponse:
        """Get a specific item."""
        return self.get(f"/your-endpoint/{item_id}")
    
    def create_item(self, payload: Dict[str, Any]) -> APIResponse:
        """Create a new item."""
        return self.post("/your-endpoint", json=payload)
    
    # Add other methods: update, delete, etc.
```

### Step 2: Create Test File

Create `tests/test_your_api.py`:

```python
import pytest
import allure
from api_automation.clients.portfolio_clients import YourAPIClient

@pytest.fixture
def your_client():
    """Provide a YourAPIClient instance."""
    return YourAPIClient()

@allure.feature("Your API")
@allure.story("Get Items")
class TestGetItems:
    """Test GET /api/v1/your-endpoint endpoint."""
    
    @pytest.mark.smoke
    @pytest.mark.regression
    @pytest.mark.positive
    @allure.title("Get all items successfully")
    def test_get_items_success(self, your_client):
        """Verify successful retrieval of items."""
        with allure.step("Request all items"):
            response = your_client.get_all_items()
        
        with allure.step("Verify response status"):
            assert response.status_code == 200
        
        with allure.step("Verify response is a list"):
            data = response.json()
            assert isinstance(data, list)
    
    # Add more tests...
```

### Step 3: Add Test Data Fixture (if needed)

In `conftest.py`, add:

```python
@pytest.fixture
def your_data():
    """Sample data for tests."""
    return {
        "field1": "value1",
        "field2": "value2",
    }
```

### Step 4: Run Tests

```bash
pytest tests/test_your_api.py -v
```

## Framework Design Principles

1. **DRY (Don't Repeat Yourself)**: Common HTTP logic centralized in BaseAPIClient
2. **Separation of Concerns**: Clients handle API communication; tests handle assertions
3. **Readability**: Clear test names and Allure steps for easy understanding
4. **Maintainability**: Easy to add new tests without duplicating code
5. **Security**: Sensitive data filtered from logs and reports
6. **Flexibility**: Environment configuration supports multiple environments
7. **Reporting**: Comprehensive Allure reports with request/response details

## API Endpoints Covered

| API | Endpoints | Tests |
|-----|-----------|-------|
| Profile | GET, POST, PATCH, DELETE | ✓ |
| Education | GET all/by-id, POST, PATCH, DELETE | ✓ |
| Experience | GET all/by-id, POST, PATCH, DELETE | ✓ |
| Skills | GET all, GET grouped, GET categories, by-id, POST, PATCH, DELETE | ✓ |
| Projects | GET all, featured, by-slug, by-id, POST, PATCH, DELETE | ✓ |
| Achievements | GET all/by-id, POST, PATCH, DELETE | ✓ |
| Certifications | GET all/by-id, POST, PATCH, DELETE | ✓ |
| Contact | POST message, GET all/by-id, PATCH (mark read), DELETE | ✓ |
| Summary | GET consolidated portfolio data | ✓ |

## Test Coverage

- **Smoke Tests**: Quick sanity checks for each API
- **Positive Tests**: Happy path scenarios with valid data
- **Negative Tests**: Error scenarios (invalid data, missing fields, not found)
- **Boundary Tests**: Edge cases and validation failures

### Current Statistics

- **Total Test Cases**: 80+
- **APIs Automated**: 9
- **Test Files**: 8
- **Positive Tests**: ~60%
- **Negative Tests**: ~40%

## Configuration

### Environment Variables

Create `.env` file from `.env.example`:

```
API_ENV=dev
DEV_BASE_URL=http://localhost:8000
QA_BASE_URL=http://qa-api.example.com
API_TIMEOUT=30
LOG_LEVEL=INFO
DEBUG=false
```

### Pytest Configuration

Edit `pytest.ini` to customize:

- Test discovery paths
- Markers
- Logging levels
- Timeout settings
- Allure configuration

## Logging

### Logger Usage

```python
from api_automation.utils import get_logger

logger = get_logger(__name__)
logger.info("Test message")
logger.debug("Debug info")
logger.error("Error occurred")
```

### Sensitive Data Filtering

Passwords, tokens, and API keys are automatically filtered from logs.

## Troubleshooting

### Tests Failing

1. **Check base URL**: Ensure `API_ENV` and corresponding URL are correct
2. **Check server**: Verify the API server is running
3. **Check logs**: Run with `-v` or `--log-cli-level=DEBUG`
4. **Check data**: Verify test data fixtures have valid values

### Allure Report Not Generating

```bash
# Ensure pytest-allure plugin is installed
pip install allure-pytest

# Regenerate reports
pytest api_automation/ --alluredir=allure-results --clean-alluredir

# View report
allure serve allure-results
```

### Import Errors

```bash
# Ensure PYTHONPATH includes backend directory
export PYTHONPATH="${PYTHONPATH}:$(pwd)"

# Or run from backend directory
cd backend && pytest api_automation/
```

## Best Practices

1. **Keep tests focused**: One logical scenario per test
2. **Use fixtures**: Leverage pytest fixtures for common setup
3. **Meaningful assertions**: Check both status code and response content
4. **Use Allure steps**: Break down tests into clear steps for reports
5. **Avoid hard-coded values**: Use fixtures and configuration
6. **Test data**: Keep test data separate from test logic
7. **Error handling**: Test both success and failure scenarios
8. **Readability**: Use clear variable names and comments

## Contributing

When adding new tests:

1. Follow existing patterns in test files
2. Use Allure decorators for better reporting
3. Create fixtures in `conftest.py` for reusable data
4. Add appropriate markers (`smoke`, `regression`, `positive`, `negative`)
5. Document complex test logic with comments
6. Ensure tests are deterministic and don't depend on execution order

## Further Improvements

Recommended enhancements for future versions:

1. **Data-Driven Testing**: Parametrize tests with multiple data sets
2. **API Mocking**: Mock external services for testing error scenarios
3. **Performance Testing**: Add response time assertions
4. **Load Testing**: Integrate with Locust for load scenarios
5. **CI/CD Integration**: GitHub Actions or Jenkins pipeline
6. **Database Validation**: Verify data changes at database level
7. **Test Analytics**: Track test trends over time
8. **Visual Regression**: Add screenshot comparison for UI data

## Support

For issues or questions:

1. Check existing test files for examples
2. Review Allure reports for detailed failure information
3. Enable DEBUG logging: `LOG_LEVEL=DEBUG`
4. Review the base client implementation in `clients/base_client.py`

## License

This framework is part of the Portfolio API project.
