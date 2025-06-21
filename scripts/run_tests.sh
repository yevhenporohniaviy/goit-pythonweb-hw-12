#!/bin/bash

# Run tests with coverage
echo "Running tests with coverage..."

# Run all tests
pytest --cov=app --cov-report=term-missing --cov-report=html

# Check if coverage is above 75%
coverage_percentage=$(pytest --cov=app --cov-report=term | grep "TOTAL" | awk '{print $4}' | sed 's/%//')

echo "Coverage: ${coverage_percentage}%"

if (( $(echo "$coverage_percentage >= 75" | bc -l) )); then
    echo "✅ Coverage is above 75%"
    exit 0
else
    echo "❌ Coverage is below 75% (${coverage_percentage}%)"
    echo "Please add more tests to improve coverage."
    exit 1
fi 