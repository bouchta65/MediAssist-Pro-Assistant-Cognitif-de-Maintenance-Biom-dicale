@echo off
REM MediAssist-Pro Test Runner Script for Windows

echo =========================================
echo MediAssist-Pro Test Suite
echo =========================================

REM Run unit tests
echo.
echo Running Unit Tests...
pytest tests/ -v -m "not slow"
if %errorlevel% neq 0 exit /b %errorlevel%

REM Run coverage report
echo.
echo Generating Coverage Report...
pytest tests/ --cov=app --cov-report=html --cov-report=term

REM Run linting
echo.
echo Running Code Linting...
flake8 app --count --statistics

echo.
echo All tests completed successfully!
