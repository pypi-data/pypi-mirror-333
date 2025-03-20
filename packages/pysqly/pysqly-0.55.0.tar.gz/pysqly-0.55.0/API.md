# pySQLY API Documentation

This document provides detailed information about the pySQLY API for developers working with the library.

## Table of Contents

- [Core Modules](#core-modules)
  - [SQLYExecutor](#sqlyexecutor)
  - [SQLYParser](#sqlyparser)
  - [SQLYUtils](#sqlyutils)
- [Database Connectors](#database-connectors)
  - [IDBConnector](#idbconnector)
  - [BaseDBConnector](#basedbconnector)
  - [DatabaseConnector](#databaseconnector)
  - [DBConnectorFactory](#dbconnectorfactory)
  - [Specific Connectors](#specific-connectors)
- [Error Handling](#error-handling)
  - [SQLYError](#sqlyerror)
  - [SQLYParseError](#sqlyparserror)
  - [SQLYExecutionError](#sqlyexecutionerror)
- [Command Line Interface](#command-line-interface)

## Core Modules

### SQLYExecutor

The central class for executing SQLY queries.

#### Constructor

```python
SQLYExecutor(datasource, db_type=None)
```

**Parameters:**

- `datasource`: Connection string or path to the database
- `db_type`: Type of database ("sqlite", "mariadb", "postgres", "oracle", "mssql")

#### Methods

##### execute_query

```python
execute(query: str) -> Any
```

Executes a SQLY query string.

**Parameters:**

- `query`: A SQLY query in YAML format

**Returns:**

- Results from the database query execution

**Raises:**

- `SQLYExecutionError`: If execution fails
- `SQLYParseError`: If the YAML cannot be parsed

**Example:**

```python
from pysqly import SQLYExecutor

executor = SQLYExecutor("mydb.sqlite", "sqlite")
results = executor.execute("""
select:
  - name
  - age
from: users
where:
  - field: age
    operator: ">"
    value: 18
""")
```

### SQLYParser

Handles parsing of SQLY query strings into structured dictionaries.

#### SQLYParser Methods

##### parse

```python
SQLYParser.parse(query: str) -> dict
```

**Parameters:**

- `query`: SQLY query string in YAML format

**Returns:**

- Dictionary representation of the YAML query

**Raises:**

- `SQLYParseError`: If the YAML cannot be parsed

**Example:**

```python
from pysqly import SQLYParser

query = """
select:
  - id
  - name
from: users
"""

parsed_query = SQLYParser.parse(query)
# parsed_query = {'select': ['id', 'name'], 'from': 'users'}
```

### SQLYUtils

Utility functions for SQLY operations.

#### SQLYUtils Methods

##### validate_query

```python
SQLYUtils.validate_query(query: dict) -> bool
```

Validates if a query dictionary has all required fields.

**Parameters:**

- `query`: Dictionary representation of a SQLY query

**Returns:**

- `True` if valid, `False` otherwise

##### translate_to_sql

```python
SQLYUtils.translate_to_sql(query: dict) -> tuple[str, list]
```

Converts a SQLY dictionary to a SQL query string and parameters.

**Parameters:**

- `query`: Dictionary representation of a SQLY query

**Returns:**

- Tuple with SQL query string and parameter list

**Example:**

```python
from pysqly import SQLYUtils

query = {
    "select": ["id", "name"],
    "from": "users",
    "where": [
        {"field": "age", "operator": ">", "value": 18}
    ]
}

sql, params = SQLYUtils.translate_to_sql(query)
# sql = "SELECT id, name FROM users WHERE age > %s"
# params = [18]
```

## Database Connectors

### IDBConnector

Interface for all database connectors.

#### Methods

##### execute

```python
execute(sql, params) -> Any
```

Abstract method that must be implemented by all connectors.

### BaseDBConnector

Base implementation of the IDBConnector interface.

#### BaseDBConnector Methods

##### execute_query

```python
execute_query(query: dict) -> Any
```

Executes a query dictionary against the database.

##### execute

```python
execute(sql, params) -> Any
```

Executes raw SQL with parameters.

### DatabaseConnector

High-level connector that manages connections to various database types.

#### DatabaseConnector Constructor

```python
DatabaseConnector(db_type, connection)
```

**Parameters:**

- `db_type`: Type of database (e.g., "sqlite", "postgres")
- `connection`: Connection string or object

#### Methods

##### execute_query

```python
execute_query(query: dict, db_type=None, connection=None) -> Any
```

Executes a SQLY query against a specified database.

### DBConnectorFactory

Factory class for creating database-specific connectors.

#### DBConnectorFactory Methods

##### create_connector

```python
DBConnectorFactory.create_connector(db_type, connection) -> IDBConnector
```

Creates and returns a connector instance for the specified database type.

### Specific Connectors

pySQLY includes the following database-specific connectors:

- `SQLiteConnector`: For SQLite databases
- `MariaDBConnector`: For MariaDB/MySQL databases
- `PostgresConnector`: For PostgreSQL databases
- `OracleConnector`: For Oracle databases
- `MSSQLConnector`: For Microsoft SQL Server databases

Each connector inherits from `BaseDBConnector` and may include database-specific optimizations.

## Error Handling

pySQLY defines a hierarchy of exception classes for error handling:

### SQLYError

```python
class SQLYError(Exception)
```

Base exception class for all pySQLY errors.

### SQLYParseError

```python
class SQLYParseError(SQLYError)
```

Raised when parsing a SQLY query fails.

### SQLYExecutionError

```python
class SQLYExecutionError(SQLYError)
```

Raised when executing a query fails.

**Example:**

```python
from pysqly import SQLYExecutor, SQLYParseError, SQLYExecutionError

try:
    executor = SQLYExecutor("mydb.sqlite", "sqlite")
    results = executor.execute(query)
except SQLYParseError as e:
    print(f"Error parsing query: {e}")
except SQLYExecutionError as e:
    print(f"Error executing query: {e}")
```

## Command Line Interface

pySQLY includes a command-line interface for executing queries directly.

```
usage: sqly-cli [-h] [--db_type DB_TYPE] [--datasource DATASOURCE] [--version] query

SQLY CLI Tool

positional arguments:
  query                 SQLY query as a YAML string

optional arguments:
  -h, --help            show this help message and exit
  --db_type DB_TYPE     Database type (sqlite, mariadb, postgres, oracle, mssql)
  --datasource DATASOURCE
                        Database connection details
  --version             show program's version number and exit
```

## Related Resources

- [Main README](./README.md) - Overview and getting started
- [Examples](./EXAMPLES.md) - Usage examples and patterns
- [Design Document](./DESIGN.md) - Architecture and design decisions
- [Security Policy](./SECURITY.md) - Security considerations
- [Changelog](./CHANGELOG.md) - Version history and changes
- [Contributing](./CONTRIBUTING.md) - How to contribute to pySQLY
