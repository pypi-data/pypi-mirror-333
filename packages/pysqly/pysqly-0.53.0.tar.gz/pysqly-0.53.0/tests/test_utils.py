"""Tests for the SQLYUtils module."""

from pysqly.core import SQLYUtils


def test_validate_query_valid():
    """Test validation of a valid query."""
    query = {"select": ["id", "name"], "from": "users"}
    assert SQLYUtils.validate_query(query) is True


def test_validate_query_invalid():
    """Test validation of an invalid query."""
    query1 = {"select": ["id"]}  # Missing "from"
    query2 = {"from": "users"}  # Missing "select"
    query3 = {}  # Empty
    query4 = []  # Not a dict

    assert SQLYUtils.validate_query(query1) is False
    assert SQLYUtils.validate_query(query2) is False
    assert SQLYUtils.validate_query(query3) is False
    assert SQLYUtils.validate_query(query4) is False


def test_translate_to_sql_basic():
    """Test translation of a basic query to SQL."""
    query = {"select": ["id", "name"], "from": "users"}
    sql, params = SQLYUtils.translate_to_sql(query)
    assert sql == "SELECT id, name FROM users"
    assert params == []


def test_translate_to_sql_with_where():
    """Test translation of a query with WHERE clause to SQL."""
    query = {
        "select": ["id", "name"],
        "from": "users",
        "where": [
            {"field": "age", "operator": ">", "value": 18},
            {"field": "active", "operator": "=", "value": True},
        ],
    }
    sql, params = SQLYUtils.translate_to_sql(query)
    assert sql == "SELECT id, name FROM users WHERE age > %s AND active = %s"
    assert params == [18, True]
