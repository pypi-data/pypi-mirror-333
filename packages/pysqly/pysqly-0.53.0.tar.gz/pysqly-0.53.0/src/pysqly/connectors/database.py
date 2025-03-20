"""Database connector utility for executing queries."""

from typing import Any, Dict, Optional

# Import factory at time of use to avoid circular imports
# from .factory import DBConnectorFactory


class DatabaseConnector:
    """
    A class that manages connections to various database types and executes
    SQLY queries.

    This class serves as an abstraction layer over different database connectors,
    allowing for a unified interface to execute queries across different
    database systems such as SQLite, MariaDB, PostgreSQL, Oracle,
    and MS SQL Server.

    Attributes:
        db_type: The type of the database being connected to.
        connection: The connection parameters or object needed to establish a
        connection.
        connector: The actual database connector instance used to interact with
        the database.

    Examples:
        >>> connector = DatabaseConnector("sqlite", ":memory:")
        >>> result = connector.execute_query({"select": ["id", "name"],
        "from": "users"})
    """

    def __init__(self, db_type: str, connection: Any) -> None:
        """
        Initialize the DatabaseConnector with the database type and connection
        information.

        Args:
            db_type: The type of the database (e.g., "sqlite", "mariadb",
                     "postgres", "oracle", "mssql").
            connection: The connection object or parameters required to establish
                     the database connection.
        """
        self.db_type = db_type
        self.connection = connection
        self.connector = None

    def _ensure_connector(self) -> Any:
        """
        Ensure that a connector instance exists, creating it if necessary.

        Returns:
            The database connector instance.
        """
        if self.connector is None:
            # Import here to avoid circular imports
            from .factory import DBConnectorFactory

            self.connector = DBConnectorFactory.create_connector(
                self.db_type, self.connection
            )
        return self.connector

    def execute_query(
        self,
        query: Dict[str, Any],
        db_type: Optional[str] = None,
        connection: Optional[Any] = None,
    ) -> Any:
        """
        Execute a SQLY query against a specified database.

        Args:
            query: The query dictionary
            db_type: The type of the database. Defaults to the instance's db_type.
            connection: The connection object or parameters. Defaults to the
                        instance's connection.

        Returns:
            The result of the executed query.

        Raises:
            SQLYExecutionError: If the query is invalid or an error occurs during
            execution.
        """
        # Use provided values or fall back to instance attributes
        db_type = db_type or self.db_type
        connection = connection or self.connection

        if db_type != self.db_type or connection != self.connection:
            # Import here to avoid circular imports
            from .factory import DBConnectorFactory

            # If parameters differ from instance attributes, create a new connector
            connector = DBConnectorFactory.create_connector(db_type, connection)
        else:
            connector = self._ensure_connector()

        # Execute the query using the appropriate connector
        return connector.execute_query(query)
