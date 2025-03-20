"""MariaDB connector implementation."""

from typing import Any, Union

# Import MySQL connector conditionally
try:
    import mysql.connector

    MYSQL_AVAILABLE = True
except ImportError:
    MYSQL_AVAILABLE = False

from .base import BaseDBConnector


class MariaDBConnector(BaseDBConnector):
    """
    MariaDBConnector is a class that inherits from BaseDBConnector.

    This class provides a connection interface to a MariaDB/MySQL database.
    """

    def __init__(self, connection: Union[str, Any]) -> None:
        """
        Initialize the MariaDBConnector.

        This constructor accepts either a connection string or an existing
        MySQL connection.

        Args:
            connection: If a string is provided, it's treated as a connection string
                and a new connection is established. If a connection object is provided,
                it's used directly.

        Raises:
            ImportError: If the mysql-connector-python package is not installed.
        """
        if not MYSQL_AVAILABLE:
            raise ImportError(
                "mysql-connector-python is not installed. "
                "Please install it with 'pip install mysql-connector-python' "
                "or 'pip install pysqly[mariadb]'."
            )

        if isinstance(connection, str):
            connection = mysql.connector.connect(connection)
        super().__init__(connection)
