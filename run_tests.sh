#!/bin/bash

# MediAssist-Pro Test Runner Script

echo "========================================="
echo "MediAssist-Pro Test Suite"
echo "========================================="

# Colors
GREEN='\033[0;32m'
RED='\033[0;31m'
NC='\033[0m' # No Color

# Run unit tests
echo -e "\n${GREEN}Running Unit Tests...${NC}"
pytest tests/ -v -m "not slow" || exit 1

# Run coverage report
echo -e "\n${GREEN}Generating Coverage Report...${NC}"
pytest tests/ --cov=app --cov-report=html --cov-report=term

# Run linting
echo -e "\n${GREEN}Running Code Linting...${NC}"
flake8 app --count --statistics

echo -e "\n${GREEN}All tests completed successfully!${NC}"
