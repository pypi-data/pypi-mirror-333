"""Execution error classes for pySQLY."""

from .base import SQLYError


class SQLYExecutionError(SQLYError):
    """
    Exception raised when a SQLY query fails to execute.

    Attributes:
        message -- explanation of the error
    """

    pass
