"""PostgreSQL connector implementation."""

from typing import Any, Union

# Import PostgreSQL connector conditionally
try:
    import psycopg2

    POSTGRES_AVAILABLE = True
except ImportError:
    POSTGRES_AVAILABLE = False

from .base import BaseDBConnector


class PostgresConnector(BaseDBConnector):
    """
    PostgresConnector is a class that inherits from BaseDBConnector.

    This class provides a connection interface to a PostgreSQL database.
    """

    def __init__(self, connection: Union[str, Any]) -> None:
        """
        Initialize a PostgresConnector.

        Args:
            connection: Either a connection string to establish a new connection
                or an existing psycopg2 connection object. If a string is provided,
                it will be used to create a new connection.

        Notes:
            The connection string should be in the format:
            "host=hostname dbname=database user=username password=password"

        Raises:
            ImportError: If the psycopg2 package is not installed.
        """
        if not POSTGRES_AVAILABLE:
            raise ImportError(
                "psycopg2 is not installed. "
                "Please install it with 'pip install psycopg2' "
                "or 'pip install pysqly[postgres]'."
            )

        if isinstance(connection, str):
            connection = psycopg2.connect(connection)
        super().__init__(connection)
