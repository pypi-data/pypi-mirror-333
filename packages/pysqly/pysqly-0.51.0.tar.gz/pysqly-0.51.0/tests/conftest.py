"""Test configuration for pySQLY."""

import sqlite3

import pytest

from pysqly.connectors import SQLiteConnector


@pytest.fixture
def sqlite_connection():
    """Create an in-memory SQLite database for testing."""
    conn = sqlite3.connect(":memory:")

    # Create a test table
    cursor = conn.cursor()
    cursor.execute(
        """
        CREATE TABLE users (
            id INTEGER PRIMARY KEY,
            name TEXT NOT NULL,
            email TEXT NOT NULL,
            active INTEGER
        )
    """
    )

    # Insert some test data
    users = [
        (1, "Alice", "alice@example.com", 1),
        (2, "Bob", "bob@example.com", 1),
        (3, "Charlie", "charlie@example.com", 0),
    ]
    cursor.executemany("INSERT INTO users VALUES (?, ?, ?, ?)", users)
    conn.commit()

    yield conn

    conn.close()


@pytest.fixture
def sqlite_connector(sqlite_connection):
    """Create an SQLiteConnector with a test database."""
    return SQLiteConnector(sqlite_connection)
