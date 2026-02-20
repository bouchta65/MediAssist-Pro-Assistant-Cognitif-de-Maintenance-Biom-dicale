# MediAssist-Pro Test Suite

This directory contains the test suite for the MediAssist-Pro application.

## Test Structure

```
tests/
├── conftest.py              # Pytest fixtures and configuration
├── test_queries.py          # Query endpoint tests
├── test_users.py            # User endpoint tests
└── test_rag_pipeline.py     # RAG pipeline component tests
```

## Running Tests

### Run all tests
```bash
pytest tests/ -v
```

### Run specific test file
```bash
pytest tests/test_queries.py -v
```

### Run with coverage report
```bash
pytest tests/ --cov=app --cov-report=html
```

### Run only fast tests (skip slow integration tests)
```bash
pytest tests/ -m "not slow"
```

### Using test runner scripts
**Linux/Mac:**
```bash
./run_tests.sh
```

**Windows:**
```bash
run_tests.bat
```

## Test Categories

- **Unit Tests**: Test individual components in isolation
- **Integration Tests**: Test component interactions
- **API Tests**: Test HTTP endpoints

## CI/CD Pipeline

The project uses GitHub Actions for continuous integration:
- Runs tests on every push and pull request
- Checks code quality with linting
- Generates coverage reports
- Builds Docker images
- Performs security scans

See `.github/workflows/ci_project.yml` for pipeline configuration.

## Writing Tests

### Example Test Structure
```python
import pytest
from fastapi.testclient import TestClient
from app.main import app

client = TestClient(app)

class TestFeature:
    def test_success_case(self):
        response = client.get("/api/endpoint")
        assert response.status_code == 200
        
    def test_error_case(self):
        response = client.get("/api/invalid")
        assert response.status_code == 404
```

## Test Coverage

View coverage report after running tests:
```bash
open htmlcov/index.html  # Mac/Linux
start htmlcov/index.html # Windows
```

## Dependencies

Test dependencies are listed in `requirements.txt`:
- pytest: Testing framework
- pytest-asyncio: Async test support
- pytest-cov: Coverage reporting
- httpx: HTTP client for FastAPI testing
- flake8: Code linting
