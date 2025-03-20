"""Microsoft SQL Server connector implementation."""

from typing import Any, Union

# Import MS SQL connector conditionally
try:
    import pyodbc

    MSSQL_AVAILABLE = True
except ImportError:
    MSSQL_AVAILABLE = False

from .base import BaseDBConnector


class MSSQLConnector(BaseDBConnector):
    """
    MSSQLConnector is a class that inherits from BaseDBConnector.

    This class provides a connection interface to Microsoft SQL Server databases.
    """

    def __init__(self, connection: Union[str, Any]) -> None:
        """
        Initialize the MSSQLConnector with a database connection.

        Args:
            connection: Either a connection string or a
                pyodbc Connection object. If a string is provided, it will be used to
                establish a new connection.

        Notes:
            If a connection string is provided, it should be in the format required by
            pyodbc, typically including server, database, authentication details,
            and other relevant parameters.

        Raises:
            ImportError: If the pyodbc package is not installed.
        """
        if not MSSQL_AVAILABLE:
            raise ImportError(
                "pyodbc is not installed. "
                "Please install it with 'pip install pyodbc' "
                "or 'pip install pysqly[mssql]'."
            )

        if isinstance(connection, str):
            connection = pyodbc.connect(connection)
        super().__init__(connection)
