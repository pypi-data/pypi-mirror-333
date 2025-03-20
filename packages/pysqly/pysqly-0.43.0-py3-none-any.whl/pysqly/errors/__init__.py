"""Exception classes for pySQLY."""

from .base import SQLYError
from .connector import SQLYConnectorError
from .execution import SQLYExecutionError
from .parse import SQLYParseError

__all__ = ["SQLYError", "SQLYParseError", "SQLYExecutionError", "SQLYConnectorError"]
