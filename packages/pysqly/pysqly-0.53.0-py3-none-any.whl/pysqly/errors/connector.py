"""Connector error classes for pySQLY."""

from .base import SQLYError


class SQLYConnectorError(SQLYError):
    """
    Exception raised when a database connector operation fails.

    Attributes:
        message -- explanation of the error
    """

    pass
