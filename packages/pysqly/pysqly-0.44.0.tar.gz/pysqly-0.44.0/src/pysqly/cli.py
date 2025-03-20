"""Command-line interface for pySQLY."""

import argparse
import sys

from pysqly import SQLYExecutor, __version__


def main() -> int:
    """
    Entry point for the SQLY CLI Tool.

    This function sets up the argument parser for the command-line interface,
    parses the provided arguments, and executes the SQLY query using the specified
    database type and connection details.

    Returns:
        The exit code (0 for success, 1 for failure).
    """
    parser = argparse.ArgumentParser(description="SQLY CLI Tool")
    parser.add_argument("query", type=str, help="SQLY query as a YAML string")
    parser.add_argument(
        "--db_type",
        type=str,
        required=True,
        help="Database type (sqlite, mariadb, postgres, oracle, mssql)",
    )
    parser.add_argument("--datasource", type=str, help="Database connection details")
    parser.add_argument("--version", action="version", version=f"pySQLY {__version__}")

    args = parser.parse_args()

    try:
        executor = SQLYExecutor(datasource=args.datasource, db_type=args.db_type)
        result = executor.execute(args.query)
        print(result)
        return 0
    except Exception as e:
        print(f"Error: {str(e)}", file=sys.stderr)
        return 1


if __name__ == "__main__":
    sys.exit(main())
