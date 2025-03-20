"""Interface for database connectors."""

from abc import ABC, abstractmethod
from typing import Any, List


class IDBConnector(ABC):
    """
    Interface for database connectors.

    This abstract class defines the interface for database connectors, providing
    a standardized way to interact with different database systems.

    Classes inheriting from IDBConnector must implement the execute method.
    """

    @abstractmethod
    def execute(self, sql: str, params: List[Any]) -> Any:
        """
        Execute a SQL query with parameters.

        This method executes a SQL query with the provided parameters against the
        database.

        Args:
            sql: The SQL query to execute.
            params: The parameters to be used in the SQL query.

        Returns:
            The result of the query execution, which depends on the specific database
            implementation.

        Raises:
            DatabaseError: If the query execution fails.
        """
        pass
