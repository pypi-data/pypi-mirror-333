# Contributing to pySQLY

Thank you for your interest in contributing to pySQLY! This document provides guidelines and instructions for contributing to this project.

## Table of Contents

- [Code of Conduct](#code-of-conduct)
- [Getting Started](#getting-started)
- [Development Workflow](#development-workflow)
- [Coding Standards](#coding-standards)
- [Documentation](#documentation)
- [Testing](#testing)
- [Submitting Changes](#submitting-changes)
- [Issue Reporting](#issue-reporting)
- [Versioning](#versioning)

## Code of Conduct

This project adheres to a [Code of Conduct](CODE_OF_CONDUCT.md) that all contributors are expected to follow. Please read it before participating.

## Getting Started

### Prerequisites

- Python 3.9 or newer
- Git

### Setting Up Your Development Environment

1. Fork the repository on GitHub
2. Clone your fork locally:

   ```bash
   git clone https://github.com/yourusername/pySQLY.git
   cd pySQLY
   ```

3. Create a virtual environment and install dependencies:

   ```bash
   python -m venv venv
   source venv/bin/activate  # On Windows, use: venv\Scripts\activate
   pip install -e ".[dev]"  # Install in development mode with development dependencies
   ```

4. Set up pre-commit hooks:

   ```bash
   pre-commit install
   ```

## Development Workflow

1. Create a new branch for your feature or bugfix:

   ```bash
   git checkout -b feature/your-feature-name
   ```

2. Make your changes and ensure they follow the project's coding standards.

3. Write tests for your changes.

4. Run the test suite:

   ```bash
   pytest
   ```

5. Commit your changes with a descriptive message:

   ```bash
   git commit -m "Add feature: your feature description"
   ```

## Coding Standards

pySQLY follows these coding standards:

- We use [Black](https://github.com/psf/black) for code formatting
- We follow [PEP 8](https://www.python.org/dev/peps/pep-0008/) for style guidelines
- We use [isort](https://pycqa.github.io/isort/) for import sorting
- We use [Ruff](https://github.com/astral-sh/ruff) for linting

These tools are configured in the project and run automatically with pre-commit hooks.

### Running the Linters

```bash
# Format code with Black
black src/ tests/

# Sort imports with isort
isort src/ tests/

# Lint with Ruff
ruff check src/ tests/
```

## Documentation

- Use docstrings for all public modules, functions, classes, and methods
- Follow [Google Style Python Docstrings](https://sphinxcontrib-napoleon.readthedocs.io/en/latest/example_google.html)
- Update documentation when changing functionality
- Add examples for new features
- Keep the [API Documentation](./API.md) up to date with any changes

## Testing

- Write tests for all new features and bug fixes
- Maintain or improve test coverage with each contribution
- Tests are written using pytest

To run tests:

```bash
pytest
```

For test coverage:

```bash
pytest --cov=pysqly
```

## Submitting Changes

1. Push your changes to your fork:

   ```bash
   git push origin feature/your-feature-name
   ```

2. Create a Pull Request (PR) from your fork to the main repository.

3. In your PR description:
   - Clearly describe the problem and solution
   - Include the relevant issue number if applicable (e.g., "Fixes #123")
   - Mention if it changes external behavior
   - Reference any related PRs or issues

4. Wait for the maintainers to review your PR. They may ask for changes before merging.

## Issue Reporting

- Use the GitHub issue tracker to report bugs or request features
- Before submitting a new issue, check if it already exists
- For bugs, include:
  - Steps to reproduce
  - Expected behavior
  - Actual behavior
  - Python and pySQLY versions
  - Operating system
  - Any relevant error messages or logs
  - Minimal code example that reproduces the issue

### Issue Templates

When creating a new issue, choose the appropriate template:

- Bug report: For reporting bugs or unexpected behavior
- Feature request: For suggesting new features or improvements
- Documentation issue: For reporting issues with documentation

## Versioning

We use [Semantic Versioning](https://semver.org/) for version numbers:

- MAJOR version for incompatible API changes (X.0.0)
- MINOR version for backward-compatible new features (0.X.0)
- PATCH version for backward-compatible bug fixes (0.0.X)

## Related Resources

- [README](./README.md) - Project overview
- [Design Document](./DESIGN.md) - Architecture and design decisions
- [Security Policy](./SECURITY.md) - Security guidelines
- [Code of Conduct](./CODE_OF_CONDUCT.md) - Community standards
- [Changelog](./CHANGELOG.md) - Version history

Thank you for contributing to pySQLY!
