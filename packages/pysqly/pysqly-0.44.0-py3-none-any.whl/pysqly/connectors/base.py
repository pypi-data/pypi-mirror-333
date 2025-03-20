"""Base implementation of the database connector interface."""

from typing import Any, Dict, List

from pysqly.errors import SQLYExecutionError

# Import SQLYUtils when needed to avoid circular imports
# from pysqly.core import SQLYUtils
from .interface import IDBConnector


class BaseDBConnector(IDBConnector):
    """
    A base class for database connectors that provides methods to execute SQL queries.

    Attributes:
        connection: A database connection object.
    """

    def __init__(self, connection: Any) -> None:
        """
        Initialize the BaseDBConnector with a database connection.

        Args:
            connection: The database connection object.
        """
        self.connection = connection

    def execute_query(self, query: Dict[str, Any]) -> Any:
        """
        Execute a SQL query constructed from the given dictionary.

        Args:
            query: A dictionary representing the query to be executed.

        Returns:
            The result of the executed query.
        """
        # Import here to avoid circular imports
        from pysqly.core import SQLYUtils

        sql, params = SQLYUtils.translate_to_sql(query, self.get_db_type())
        return self.execute(sql, params)

    def get_db_type(self) -> str:
        """
        Get the database type for this connector.

        Returns:
            String representing the database type
        """
        # Extract the database type from the class name
        # (e.g., SQLiteConnector -> sqlite)
        class_name = self.__class__.__name__.lower()
        if "sqlite" in class_name:
            return "sqlite"
        elif "mariadb" in class_name or "mysql" in class_name:
            return "mariadb"
        elif "postgres" in class_name:
            return "postgres"
        elif "oracle" in class_name:
            return "oracle"
        elif "mssql" in class_name:
            return "mssql"
        else:
            raise ValueError(f"Unknown database type for {class_name}")

    def execute(self, sql: str, params: List[Any]) -> Any:
        """
        Execute a given SQL statement with the provided parameters.

        Args:
            sql: The SQL statement to be executed.
            params: The parameters to be used with the SQL statement.

        Returns:
            If the SQL statement is a SELECT query, returns the fetched results.
            If the SQL statement is not a SELECT query, returns a success message.

        Raises:
            SQLYExecutionError: If an error occurs during the execution of
            the SQL statement.
        """
        cursor = self.connection.cursor()
        try:
            cursor.execute(sql, params)
            if sql.strip().upper().startswith("SELECT"):
                return cursor.fetchall()
            self.connection.commit()
            return "Query executed successfully"
        except Exception as e:
            raise SQLYExecutionError(
                f"{self.__class__.__name__} error: {str(e)}"
            ) from e
        finally:
            cursor.close()
