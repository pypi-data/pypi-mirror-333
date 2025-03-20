# pySQLY Design Document

This document outlines the architectural design and patterns used in pySQLY.

## Architecture Overview

pySQLY follows a layered architecture with the following components:

1. **Core Layer**: Handles parsing, validation, and execution of SQLY queries
2. **Connector Layer**: Provides database-specific implementations
3. **Error Handling Layer**: Centralizes error management
4. **CLI Layer**: Provides command-line interface functionality

The following diagram illustrates the high-level architecture:

```bash
┌─────────────┐     ┌─────────────┐
│   Client    │     │    CLI      │
└─────┬───────┘     └──────┬──────┘
      │                    │
      ▼                    ▼
┌─────────────────────────────────┐
│           SQLYExecutor          │
└─────────────┬───────────────────┘
              │
    ┌─────────┴─────────┐
    │                   │
    ▼                   ▼
┌─────────┐      ┌──────────────┐
│SQLYParser│      │SQLYUtils     │
└─────────┘      └──────┬───────┘
                        │
                        ▼
              ┌───────────────────┐
              │DatabaseConnector  │
              └─────────┬─────────┘
                        │
                ┌───────┴────────┐
                │                │
                ▼                ▼
         ┌────────────┐   ┌─────────────┐
         │ Specific   │...│ Specific    │
         │Connectors  │   │Connectors   │
         └────────────┘   └─────────────┘
```

## Design Patterns

1. **Factory Pattern**: The `DBConnectorFactory` class creates appropriate database connector instances based on the database type, abstracting the creation logic.

2. **Strategy Pattern**: Different database connectors implement a common interface (`IDBConnector`), allowing the rest of the application to work with different databases uniformly.

3. **Facade Pattern**: The `SQLYExecutor` class provides a simplified interface to the complex subsystem of parsing, validation, and execution.

4. **Composite Pattern**: SQLY queries are composed as structured YAML objects that can represent complex SQL statements.

## Core Components

### SQLYParser

Responsible for parsing YAML queries into Python dictionaries. Uses PyYAML for YAML parsing.

### SQLYUtils

Contains utility functions for validating and translating SQLY queries to SQL statements.

### SQLYExecutor

The main entry point for query execution. Orchestrates the parsing, validation, and execution process.

## Database Connectors

The connector layer follows an interface-based design:

1. `IDBConnector`: Interface defining the contract for all database connectors
2. `BaseDBConnector`: Abstract implementation with common functionality
3. Specific connectors: Database-specific implementations (SQLite, MariaDB, PostgreSQL, Oracle, MSSQL)

## Error Handling Strategy

pySQLY implements a hierarchical exception system:

1. `SQLYError`: Base exception class
2. `SQLYParseError`: For parsing errors
3. `SQLYExecutionError`: For execution errors
4. `SQLYConnectorError`: For database connector errors

This allows for fine-grained exception handling and appropriate error messages.

## Extension Points

pySQLY is designed to be extensible in several ways:

1. **New Database Support**: Add new connectors by implementing the `IDBConnector` interface
2. **Query Features**: Extend the YAML format and the translation logic in `SQLYUtils`
3. **Result Processing**: Add post-processing capabilities to transform query results

## Performance Considerations

1. Connection pooling is handled at the database driver level
2. YAML parsing is optimized using PyYAML's safe_load
3. Parameter binding is used to prevent SQL injection and improve performance

## Future Architectural Improvements

1. **Connection Pooling**: Implement a custom connection pooling mechanism
2. **Async Support**: Add asynchronous query execution capabilities
3. **Query Caching**: Implement caching for frequently executed queries
4. **Result Set Pagination**: Support for paginated results for large data sets
