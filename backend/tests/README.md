# Portfolio API - Test Suite Documentation

## Overview

Comprehensive test suite for the Portfolio API backend, covering unit tests and integration tests for all API endpoints.

## Test Structure

```
tests/
├── __init__.py
├── conftest.py                     # Shared fixtures and test configuration
├── unit/                           # Unit tests for individual endpoints
│   ├── test_profile_api.py
│   ├── test_education_api.py
│   ├── test_experience_api.py
│   ├── test_skills_api.py
│   ├── test_projects_api.py
│   ├── test_contact_api.py
│   └── test_summary_api.py
└── integration/                    # Integration tests for workflows
    ├── test_portfolio_workflow.py
    └── test_data_validation.py
```

## Testing Libraries

- **pytest** - Testing framework
- **pytest-asyncio** - Async test support for FastAPI
- **httpx** - HTTP client for testing API endpoints
- **pytest-cov** - Code coverage reporting
- **faker** - Realistic fake data generation

## Installation

Install test dependencies:

```bash
pip install -r requirements-dev.txt
```

## Running Tests

### Run All Tests
```bash
pytest
```

### Run Unit Tests Only
```bash
pytest tests/unit/ -v
```

### Run Integration Tests Only
```bash
pytest tests/integration/ -v
```

### Run Specific Test File
```bash
pytest tests/unit/test_profile_api.py -v
```

### Run Specific Test Class
```bash
pytest tests/unit/test_profile_api.py::TestProfileAPI -v
```

### Run Specific Test Method
```bash
pytest tests/unit/test_profile_api.py::TestProfileAPI::test_create_profile_success -v
```

### Run Tests by Marker
```bash
# Run only unit tests
pytest -m unit

# Run only integration tests
pytest -m integration
```

## Code Coverage

### Generate Coverage Report
```bash
pytest --cov=app --cov-report=html
```

This creates an HTML coverage report in `htmlcov/index.html`.

### Coverage with Terminal Output
```bash
pytest --cov=app --cov-report=term-missing
```

### Coverage for Specific Module
```bash
pytest --cov=app.routers.profile tests/unit/test_profile_api.py
```

## Test Categories

### Unit Tests
Test individual API endpoints in isolation:
- **Profile API**: GET, POST, PATCH, DELETE profile operations
- **Education API**: CRUD operations for education records
- **Experience API**: CRUD with filtering by employment type and current status
- **Skills API**: CRUD, grouped view, category filtering
- **Projects API**: CRUD, featured filtering, slug-based lookup
- **Contact API**: Message submission, read/unread filtering
- **Summary API**: Aggregated portfolio data retrieval

### Integration Tests
Test complete workflows and cross-endpoint interactions:
- **Portfolio Workflows**: Complete portfolio setup, updates, deletions
- **Data Validation**: Email validation, unique constraints, field validation
- **Business Logic**: Featured projects, skill organization, experience filtering

## Test Database

Tests use an **in-memory SQLite database** that is:
- Created fresh for each test function
- Completely isolated from production/development databases
- Automatically cleaned up after each test
- Fast and doesn't require external dependencies

## Fixtures

### Database Fixtures
- `db` - Fresh database session for each test
- `client` - Async HTTP test client with database override

### Data Generation Fixtures
- `fake` - Faker instance for generating test data
- `sample_*_data` - Pre-configured sample data for each model
- `created_*` - Persisted database records for testing

## Writing New Tests

### Unit Test Template
```python
import pytest
from httpx import AsyncClient

@pytest.mark.unit
@pytest.mark.asyncio
class TestNewEndpoint:
    """Test suite for /api/v1/new-endpoint."""
    
    async def test_endpoint_success(self, client: AsyncClient):
        """Test successful operation."""
        response = await client.get("/api/v1/new-endpoint/")
        assert response.status_code == 200
        assert "expected_field" in response.json()
```

### Integration Test Template
```python
import pytest
from httpx import AsyncClient

@pytest.mark.integration
@pytest.mark.asyncio
class TestNewWorkflow:
    """Integration test for a complete workflow."""
    
    async def test_complete_workflow(self, client: AsyncClient):
        """Test multi-step workflow."""
        # Step 1: Create resource
        response1 = await client.post("/api/v1/resource/", json=data)
        assert response1.status_code == 201
        
        # Step 2: Verify in another endpoint
        response2 = await client.get("/api/v1/related/")
        assert len(response2.json()) == 1
```

## Best Practices

1. **Isolation**: Each test should be independent and not rely on other tests
2. **Cleanup**: Use fixtures to ensure proper cleanup after tests
3. **Descriptive Names**: Test names should clearly describe what they test
4. **Assertions**: Use specific assertions rather than generic ones
5. **Coverage**: Aim for >80% code coverage on critical paths
6. **Edge Cases**: Test boundary conditions and error scenarios

## Common Test Scenarios

### Testing Success Cases
- Valid data creates/updates/deletes resources
- Correct response status codes and data structure

### Testing Validation
- Missing required fields return 422
- Invalid data types return 422
- Invalid email formats return 422
- Out-of-range values (e.g., proficiency > 100) return 422

### Testing Not Found
- Non-existent IDs return 404
- Appropriate error messages

### Testing Conflicts
- Duplicate slugs return 409
- Single profile constraint returns 409

### Testing Filters and Queries
- Query parameters work correctly
- Empty results return empty arrays
- Ordering works as expected

## Troubleshooting

### Tests Failing After Code Changes
1. Check if API contract changed (routes, schemas)
2. Update test data to match new validation rules
3. Verify fixtures are creating valid test data

### Slow Tests
1. Ensure using in-memory database (should be default)
2. Check for unnecessary waits or sleeps
3. Profile tests with `pytest --durations=10`

### Import Errors
1. Ensure you're running from the `backend/` directory
2. Verify all dependencies are installed: `pip install -r requirements-dev.txt`
3. Check Python path includes the backend directory

## CI/CD Integration

### GitHub Actions Example
```yaml
- name: Run Tests
  run: |
    cd backend
    pip install -r requirements.txt -r requirements-dev.txt
    pytest --cov=app --cov-report=xml

- name: Upload Coverage
  uses: codecov/codecov-action@v3
  with:
    files: ./backend/coverage.xml
```

## Test Metrics

Target metrics for the test suite:
- **Code Coverage**: > 80% for all modules
- **Test Count**: 100+ total tests
- **Execution Time**: < 30 seconds for full suite
- **Failure Rate**: 0% on main branch

## Contributing

When adding new features:
1. Write unit tests for new endpoints
2. Write integration tests for new workflows
3. Ensure all tests pass before submitting PR
4. Maintain or improve code coverage percentage
5. Document any new test fixtures or utilities
