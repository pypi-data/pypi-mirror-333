"""SQLY parser module for converting YAML queries to dictionaries."""

from typing import Any, Dict

import yaml

from pysqly.errors import SQLYParseError


class SQLYParser:
    """Parse SQLY query strings into dictionaries."""

    @staticmethod
    def parse(query: str) -> Dict[str, Any]:
        """
        Parse a SQLY query string into a dictionary.

        Args:
            query: The SQLY query string to be parsed.

        Returns:
            The parsed representation of the SQLY query.

        Raises:
            SQLYParseError: If the query contains invalid SQLY syntax.
        """
        try:
            return yaml.safe_load(query)
        except yaml.YAMLError as e:
            raise SQLYParseError(f"Invalid SQLY syntax: {str(e)}") from e
