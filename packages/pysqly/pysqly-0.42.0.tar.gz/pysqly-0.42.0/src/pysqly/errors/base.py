"""Base exception classes for pySQLY."""


class SQLYError(Exception):
    """
    Exception raised for errors related to SQLY operations.

    This is the base class for all exceptions that are raised due to
    SQLY-related errors. It can be used to catch all SQLY-specific
    exceptions in a single except block.
    """

    pass
