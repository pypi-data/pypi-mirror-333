"""Factory for creating database connectors."""

from typing import Any

from pysqly.errors import SQLYExecutionError

# Import connectors directly instead of from module to avoid circular dependencies
from .mariadb import MYSQL_AVAILABLE, MariaDBConnector
from .mssql import MSSQL_AVAILABLE, MSSQLConnector
from .oracle import ORACLE_AVAILABLE, OracleConnector
from .postgres import POSTGRES_AVAILABLE, PostgresConnector
from .sqlite import SQLiteConnector


class DBConnectorFactory:
    """
    Factory class for creating database connectors based on database type.

    This class implements the Factory Pattern to create the appropriate
    database connector instance based on the database type.
    """

    @staticmethod
    def create_connector(db_type: str, connection: Any) -> Any:
        """
        Create and return a database connector instance based on the database type.

        Args:
            db_type: The type of the database (e.g., "sqlite", "mariadb",
                    "postgres", "oracle", "mssql").
            connection: The connection object or parameters required to establish
                    the database connection.

        Returns:
            An instance of the corresponding database connector class.

        Raises:
            SQLYExecutionError: If the specified database type is not supported or
                                if the required database driver is not installed.
        """
        # Check if the requested database type is available
        if db_type == "mariadb" and not MYSQL_AVAILABLE:
            raise SQLYExecutionError(
                "MariaDB/MySQL connector is not available. "
                "Please install mysql-connector-python package."
            )
        elif db_type == "postgres" and not POSTGRES_AVAILABLE:
            raise SQLYExecutionError(
                "PostgreSQL connector is not available. "
                "Please install psycopg2 package."
            )
        elif db_type == "oracle" and not ORACLE_AVAILABLE:
            raise SQLYExecutionError(
                "Oracle connector is not available. "
                "Please install cx_Oracle package."
            )
        elif db_type == "mssql" and not MSSQL_AVAILABLE:
            raise SQLYExecutionError(
                "MS SQL Server connector is not available. "
                "Please install pyodbc package."
            )

        # Define the mapping of database types to connector classes
        connectors = {
            "sqlite": SQLiteConnector,
            "mariadb": MariaDBConnector,
            "postgres": PostgresConnector,
            "oracle": OracleConnector,
            "mssql": MSSQLConnector,
        }

        if db_type not in connectors:
            raise SQLYExecutionError(f"Unsupported database type: {db_type}")

        return connectors[db_type](connection)
