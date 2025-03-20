"""Tests for the SQLYParser module."""

import pytest

from pysqly.core import SQLYParser
from pysqly.errors import SQLYParseError


def test_parser_valid_yaml():
    """Test that valid YAML is parsed correctly."""
    query = """
    select:
      - id
      - name
    from: users
    where:
      - field: active
        operator: "="
        value: true
    """
    parsed = SQLYParser.parse(query)
    assert isinstance(parsed, dict)
    assert "select" in parsed
    assert "from" in parsed
    assert "where" in parsed
    assert parsed["select"] == ["id", "name"]
    assert parsed["from"] == "users"
    assert len(parsed["where"]) == 1
    assert parsed["where"][0]["field"] == "active"


def test_parser_invalid_yaml():
    """Test that invalid YAML raises SQLYParseError."""
    query = """
    select:
      - id
      name  # Missing hyphen
    from: users
    """
    with pytest.raises(SQLYParseError):
        SQLYParser.parse(query)
