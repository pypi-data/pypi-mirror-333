"""Tests for the SQLYExecutor module."""

import pytest

from pysqly.core import SQLYExecutor
from pysqly.errors import SQLYExecutionError, SQLYParseError


def test_executor_init():
    """Test SQLYExecutor initialization."""
    # Basic initialization
    executor = SQLYExecutor("test.db", "sqlite")
    assert executor.datasource == "test.db"
    assert executor.db_type == "sqlite"
    assert executor.db_connector is not None

    # Initialize without db_type should not create a connector
    executor = SQLYExecutor("test.db")
    assert executor.datasource == "test.db"
    assert executor.db_type is None
    assert executor.db_connector is None


def test_executor_invalid_query():
    """Test execution with invalid query."""
    # Create executor with test database
    executor = SQLYExecutor(":memory:", "sqlite")

    # Test with missing required fields
    with pytest.raises(SQLYExecutionError):
        executor.execute(
            """
        select:
          - id
          - name
        # Missing 'from' field
        """
        )

    # Test with invalid YAML
    with pytest.raises(SQLYParseError):
        executor.execute(
            """
        select:
          - id
          name  # Missing hyphen
        from: users
        """
        )


def test_executor_missing_db_type():
    """Test execution without specifying database type."""
    executor = SQLYExecutor("test.db")

    with pytest.raises(SQLYExecutionError):
        executor.execute(
            """
        select:
          - id
        from: users
        """
        )


def test_executor_query(sqlite_connector):
    """Test successful query execution with a real database."""
    # Create executor that uses our sqlite_connector fixture
    executor = SQLYExecutor(":memory:", "sqlite")

    # Replace the connector with our test connector
    executor.db_connector.connector = sqlite_connector

    # Execute a test query against our fixture database
    result = executor.execute(
        """
    select:
      - name
      - email
    from: users
    where:
      - field: active
        operator: "="
        value: 1
    """
    )

    # Check the result - should find Alice and Bob who have active=1
    assert len(result) == 2
    # Results are tuples of (name, email)
    names = [row[0] for row in result]
    assert "Alice" in names
    assert "Bob" in names
    assert "Charlie" not in names


def test_executor_with_mock(monkeypatch):
    """Test successful query execution with mock."""
    # Create executor with mock behavior
    executor = SQLYExecutor("test.db", "sqlite")

    # Mock the execute_query method to avoid actual database operation
    def mock_execute_query(self, query, **kwargs):
        return [("Alice", "alice@example.com"), ("Bob", "bob@example.com")]

    # Apply the mock to the DatabaseConnector class
    monkeypatch.setattr(
        executor.db_connector.__class__, "execute_query", mock_execute_query
    )

    # Execute a test query
    result = executor.execute(
        """
    select:
      - name
      - email
    from: users
    where:
      - field: active
        operator: "="
        value: 1
    """
    )

    # Check the result
    assert len(result) == 2
    assert result[0] == ("Alice", "alice@example.com")
    assert result[1] == ("Bob", "bob@example.com")
