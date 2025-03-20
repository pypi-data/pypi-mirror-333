#!/bin/bash
# Simple script to run tests for pySQLY

# Exit on any error
set -e

echo "Installing dependencies for testing..."
python -m pip install -e ".[dev]"

echo "Running tests..."
pytest

echo "Tests completed successfully!"
