# Prompt: Build API Automation Framework from Scratch

You are an expert Python QA Automation Architect.

I have an existing Python codebase containing APIs that need to be automated. Build a **maintainable API test automation framework from scratch using Pytest and Allure reporting**.

## Objective

Create a clean, scalable API automation framework that allows me to:

* Automate REST APIs using Python
* Execute tests using Pytest
* Validate status codes, headers, response body, and business rules
* Support positive and negative test scenarios
* Maintain reusable API/client utilities
* Generate detailed Allure reports
* Easily add new APIs and test cases in the future
* Keep the framework simple initially so development can be rapid

## Important Instructions

Before implementing anything:

1. Thoroughly inspect the existing repository.
2. Identify:

   * Existing APIs
   * API endpoints
   * Request methods
   * Request payloads
   * Authentication mechanisms
   * Headers
   * Query/path parameters
   * Expected response structures
   * Existing configuration
   * Existing test data
   * Existing API documentation/OpenAPI specifications
3. Do NOT modify existing application/business code unless absolutely required.
4. Reuse existing API specifications, models, constants, and utilities where appropriate.
5. Do not invent API behavior when it can be determined from the existing code or API documentation.
6. First provide an implementation plan and proposed project structure.
7. After the plan is clear, implement the framework.

## Initial Technology Stack

Use only the following initially:

* Python 3.x
* Pytest
* Requests
* Allure Pytest
* Python standard library wherever possible

Do NOT introduce additional frameworks such as Selenium, Playwright, Behave, Schemathesis, Hypothesis, databases, or external reporting systems at this stage.

Keep the first implementation lightweight and easy to understand.

## Proposed Framework Structure

Use a structure similar to:

```text
api-automation/
│
├── tests/
│   ├── test_<api_name>.py
│   └── ...
│
├── clients/
│   ├── base_client.py
│   ├── <api_name>_client.py
│   └── ...
│
├── models/
│   └── ...
│
├── test_data/
│   └── ...
│
├── utils/
│   ├── config.py
│   └── ...
│
├── conftest.py
├── pytest.ini
├── requirements.txt
├── .env.example
├── README.md
└── allure-results/
```

Adjust this structure if the existing codebase requires a better organization.

## API Client Layer

Create reusable API clients.

The base client should support:

* GET
* POST
* PUT
* PATCH
* DELETE

Centralize common functionality such as:

* Base URL handling
* Headers
* Authentication
* Request execution
* Timeout
* Logging
* Error handling
* Response handling

Example conceptual usage:

```python
response = user_client.get_user(user_id)
```

Tests should NOT contain duplicated low-level HTTP request code whenever the same operation can be encapsulated in a client.

## Pytest Test Design

Create readable Pytest tests.

Each test should clearly represent a business scenario.

Example:

```python
def test_create_user_success():
    response = user_client.create_user(payload)

    assert response.status_code == 201
    assert response.json()["name"] == payload["name"]
```

Use Pytest fixtures for:

* API clients
* Authentication
* Common test data
* Configuration
* Reusable setup/teardown

Use parametrization where it genuinely reduces duplication.

## Allure Reporting

Integrate:

```text
allure-pytest
```

Add meaningful Allure metadata:

* Feature
* Story
* Test title
* Severity where appropriate
* Steps
* Request information
* Response information

Example:

```python
@allure.feature("User API")
@allure.story("Create User")
@allure.title("Create user with valid payload")
def test_create_user_success():
    ...
```

Use `allure.step()` for important test actions.

Attach useful request/response information to the Allure report, while ensuring that secrets such as passwords, access tokens, API keys, and sensitive information are never exposed in reports.

## Configuration

Do not hardcode:

* Base URLs
* Credentials
* Tokens
* API keys
* Environment-specific configuration

Create a clean configuration mechanism.

Support environments such as:

```text
dev
qa
staging
```

Use environment variables or configuration files as appropriate.

Provide:

```text
.env.example
```

but never commit real credentials.

## Test Coverage

Analyze the existing APIs and create an initial test suite covering:

### Positive Tests

* Successful GET
* Successful POST
* Successful PUT/PATCH
* Successful DELETE
* Valid request payloads
* Valid authentication

### Negative Tests

Where applicable:

* Missing required fields
* Invalid field values
* Invalid IDs
* Missing authentication
* Invalid authentication
* Invalid request payload
* Unsupported HTTP method
* Resource not found
* Duplicate resource
* Boundary/validation failures

Do not create meaningless tests just to increase test count.

## Response Validation

Validate more than just the HTTP status code where appropriate.

Validate:

* Status code
* Response headers
* Required response fields
* Field values
* Data types
* Business rules
* Error messages
* Response structure

Use clear assertions.

Avoid brittle assertions against dynamic values such as:

* IDs
* timestamps
* tokens
* generated UUIDs

unless those values are specifically part of the requirement.

## Test Data

Keep test data separate from test implementation wherever practical.

Do not duplicate large request payloads across multiple tests.

Use reusable fixtures/factories when appropriate.

## Logging

Add useful logging for debugging failed API tests.

Logs should help identify:

```text
HTTP Method
Endpoint
Request parameters
Request payload
Response status
Response body
```

Never log secrets.

## Pytest Configuration

Configure Pytest so I can run:

```bash
pytest
```

and generate Allure results.

Also support:

```bash
pytest --alluredir=allure-results
```

Document how to generate and view the report.

For example:

```bash
allure serve allure-results
```

or an equivalent documented approach.

## Requirements

Create/update:

```text
requirements.txt
```

with only the dependencies actually required for the initial framework.

## README

Create a clear README containing:

1. Prerequisites
2. Python setup
3. Virtual environment setup
4. Dependency installation
5. Configuration setup
6. Running all tests
7. Running a specific test
8. Running tests by marker
9. Generating Allure results
10. Viewing the Allure report
11. Project structure
12. How to add a new API test
13. Framework design principles

## Test Markers

Introduce useful markers such as:

```text
smoke
regression
positive
negative
```

Configure them properly in `pytest.ini`.

Example:

```bash
pytest -m smoke
```

## Implementation Approach

Implement in phases.

### Phase 1 — Repository Analysis

Analyze the existing codebase and produce:

* API inventory
* Authentication mechanism
* Existing API documentation
* Existing reusable components
* Existing test data
* Risks/constraints
* Proposed framework architecture

Do not write tests yet.

### Phase 2 — Framework Foundation

Implement:

* Project structure
* requirements.txt
* pytest.ini
* conftest.py
* configuration
* base API client
* logging
* Allure integration

Then run a basic validation.

### Phase 3 — First API

Select one representative API and implement:

* API client
* Test data
* Positive tests
* Negative tests
* Assertions
* Allure reporting

Run the tests and fix all issues.

### Phase 4 — Remaining APIs

Implement tests for the remaining APIs following the same framework pattern.

Avoid copy-paste implementations.

### Phase 5 — Validation

Run:

```bash
pytest
```

Then generate Allure results.

Verify that:

* Tests execute successfully
* Allure results are generated
* Test names are meaningful
* Allure steps are visible
* Request/response information is available
* Secrets are not exposed
* Failed tests provide enough debugging information

## Quality Requirements

The implementation must be:

* Clean
* Modular
* Maintainable
* Reusable
* Easy for another QA engineer to understand
* Easy to extend
* PEP 8 compliant
* Strongly typed where useful
* Free from unnecessary abstraction
* Free from duplicated HTTP logic
* Free from hardcoded credentials

Do not over-engineer the framework.

The priority is:

**Rapid API automation development + maintainability + clear reporting.**

## Final Deliverables

At the end provide:

1. Final project structure
2. List of APIs automated
3. Number of test cases created
4. Positive/negative test coverage
5. Files created/modified
6. Framework architecture explanation
7. Commands to execute tests
8. Commands to generate/view Allure reports
9. Any assumptions made
10. Any APIs that could not be automated and why
11. Recommended next improvements

Most importantly, do not simply generate sample tests. **Inspect the actual repository and implement tests against the real APIs present in the codebase.**
