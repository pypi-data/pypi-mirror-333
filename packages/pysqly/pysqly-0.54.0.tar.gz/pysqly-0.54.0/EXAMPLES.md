# pySQLY Examples

This document provides practical examples of how to use pySQLY in various scenarios to simplify your database interactions.

## Table of Contents

- [Basic Queries](#basic-queries)
- [Advanced Queries](#advanced-queries)
- [Working with Different Databases](#working-with-different-databases)
- [CLI Examples](#cli-examples)
- [Error Handling](#error-handling)
- [Best Practices](#best-practices)

## Basic Queries

### Simple SELECT query

```python
from pysqly import SQLYExecutor

executor = SQLYExecutor("database.db", "sqlite")

query = """
select:
  - id
  - name
  - email
from: users
"""

results = executor.execute(query)
for row in results:
    print(row)
```

### Query with WHERE clause

```python
query = """
select:
  - id
  - name
  - email
from: users
where:
  - field: status
    operator: "="
    value: "active"
"""

active_users = executor.execute(query)
```

### Multiple WHERE conditions (AND)

```python
query = """
select:
  - id
  - name
from: products
where:
  - field: price
    operator: ">"
    value: 100
  - field: category
    operator: "="
    value: "electronics"
"""

expensive_electronics = executor.execute(query)
```

## Advanced Queries

### Using Aliases

```python
query = """
select:
  - "COUNT(*) as user_count"
from: users
where:
  - field: registration_date
    operator: ">"
    value: "2023-01-01"
"""

user_count = executor.execute(query)
```

### Joining Tables

```python
query = """
select:
  - "users.name"
  - "orders.order_date"
  - "orders.total"
from: "users JOIN orders ON users.id = orders.user_id"
where:
  - field: orders.total
    operator: ">"
    value: 50
"""

user_orders = executor.execute(query)
```

### Grouping and Aggregation

```python
query = """
select:
  - "category"
  - "COUNT(*) as product_count"
  - "AVG(price) as avg_price"
from: products
where:
  - field: active
    operator: "="
    value: true
"""

product_stats = executor.execute(query)
```

## Working with Different Databases

### SQLite

```python
from pysqly import SQLYExecutor

sqlite_executor = SQLYExecutor("local_database.db", "sqlite")
results = sqlite_executor.execute(query)
```

### PostgreSQL

```python
postgres_conn = "host=localhost dbname=mydb user=postgres password=secret"
pg_executor = SQLYExecutor(postgres_conn, "postgres")
results = pg_executor.execute(query)
```

### MariaDB/MySQL

```python
mariadb_conn = "host=localhost user=root password=secret database=mydb"
maria_executor = SQLYExecutor(mariadb_conn, "mariadb")
results = maria_executor.execute(query)
```

### Oracle

```python
oracle_conn = "username/password@localhost:1521/XEPDB1"
oracle_executor = SQLYExecutor(oracle_conn, "oracle")
results = oracle_executor.execute(query)
```

### Microsoft SQL Server

```python
mssql_conn = "DRIVER={ODBC Driver 17 for SQL Server};SERVER=localhost;DATABASE=mydb;UID=sa;PWD=password"
mssql_executor = SQLYExecutor(mssql_conn, "mssql")
results = mssql_executor.execute(query)
```

## CLI Examples

### Basic Query

```bash
sqly-cli "select: [name, email]\nfrom: users" --db_type sqlite --datasource "test.db"
```

### Query with WHERE Condition

```bash
sqly-cli "select: [name, email]\nfrom: users\nwhere:\n  - field: status\n    operator: '='\n    value: active" --db_type sqlite --datasource "test.db"
```

### Query with Multiple Conditions

```bash
sqly-cli "select: [product_name, price]\nfrom: products\nwhere:\n  - field: category\n    operator: '='\n    value: 'electronics'\n  - field: price\n    operator: '<'\n    value: 500" --db_type postgres --datasource "host=localhost dbname=mydb user=postgres password=secret"
```

## Error Handling

### Handling Parse Errors

```python
from pysqly import SQLYExecutor, SQLYParseError

executor = SQLYExecutor("database.db", "sqlite")

try:
    # Malformed YAML
    query = """
    select:
      - id
      name  # Missing hyphen
    from: users
    """
    results = executor.execute(query)
except SQLYParseError as e:
    print(f"Parse error: {e}")
    # Handle the error appropriately
```

### Handling Execution Errors

```python
from pysqly import SQLYExecutor, SQLYExecutionError

executor = SQLYExecutor("database.db", "sqlite")

try:
    # Query with non-existent table
    query = """
    select:
      - id
      - name
    from: nonexistent_table
    """
    results = executor.execute(query)
except SQLYExecutionError as e:
    print(f"Execution error: {e}")
    # Handle the error appropriately
```

## Best Practices

### Connection Management

For better performance, reuse executor instances when making multiple queries:

```python
# Create once, use many times
executor = SQLYExecutor("database.db", "sqlite")

# Query 1
users = executor.execute(user_query)

# Query 2
products = executor.execute(product_query)
```

### Error Handling Strategy

Implement a comprehensive error handling strategy:

```python
from pysqly import SQLYExecutor, SQLYParseError, SQLYExecutionError, SQLYError

try:
    executor = SQLYExecutor("database.db", "sqlite")
    results = executor.execute(query)
except SQLYParseError as e:
    # Handle parsing errors specifically
    logger.error(f"Invalid YAML syntax: {e}")
except SQLYExecutionError as e:
    # Handle execution errors specifically
    logger.error(f"Database execution failed: {e}")
except SQLYError as e:
    # Handle any other pySQLY errors
    logger.error(f"pySQLY error: {e}")
except Exception as e:
    # Handle unexpected errors
    logger.critical(f"Unexpected error: {e}")
```

## Related Resources

- [API Documentation](./API.md) - Detailed library API reference
- [Design Document](./DESIGN.md) - Architecture and design patterns
- [Security Policy](./SECURITY.md) - Security best practices
- [Contributing](./CONTRIBUTING.md) - How to contribute to pySQLY
