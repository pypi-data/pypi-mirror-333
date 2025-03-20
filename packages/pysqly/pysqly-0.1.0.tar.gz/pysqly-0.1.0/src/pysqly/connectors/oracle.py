"""Oracle connector implementation."""

from typing import Any, Union

# Import Oracle connector conditionally
try:
    import cx_Oracle

    ORACLE_AVAILABLE = True
except ImportError:
    ORACLE_AVAILABLE = False

from .base import BaseDBConnector


class OracleConnector(BaseDBConnector):
    """
    OracleConnector is a class that inherits from BaseDBConnector.

    This class provides a connection interface to an Oracle database.
    """

    def __init__(self, connection: Union[str, Any]) -> None:
        """
        Initialize the OracleConnector.

        This constructor initializes a connection to an Oracle database using cx_Oracle.

        Args:
            connection: Either a connection string in the format
                "username/password@host:port/service_name" or an already established
                cx_Oracle Connection object. If a string is provided, it will be used
                to create a new connection.

        Notes:
            The connection string format follows the Oracle standard:
            "username/password@host:port/service_name"

        Raises:
            ImportError: If the cx_Oracle package is not installed.
        """
        if not ORACLE_AVAILABLE:
            raise ImportError(
                "cx_Oracle is not installed. "
                "Please install it with 'pip install cx_Oracle' "
                "or 'pip install pysqly[oracle]'."
            )

        if isinstance(connection, str):
            connection = cx_Oracle.connect(connection)
        super().__init__(connection)
