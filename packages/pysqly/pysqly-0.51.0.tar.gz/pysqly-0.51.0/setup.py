"""Setup script for pySQLY."""

from setuptools import find_packages, setup

if __name__ == "__main__":
    setup(
        name="pysqly",
        version='0.51.0',
        description="SQL with YAML - A simplified query language for "
        "multiple databases",
        long_description=open("README.md").read(),
        long_description_content_type="text/markdown",
        author="Standard Query Language",
        author_email="example@example.com",
        url="https://github.com/Standard-Query-Language/pySQLY",
        packages=find_packages(where="src"),
        package_dir={"": "src"},
        include_package_data=True,
        install_requires=[
            "pyyaml>=6.0",
        ],
        extras_require={
            "mariadb": ["mysql-connector-python>=8.0"],
            "postgres": ["psycopg2>=2.9"],
            "oracle": ["cx_Oracle>=8.0"],
            "mssql": ["pyodbc>=4.0"],
            "all": [
                "mysql-connector-python>=8.0",
                "psycopg2>=2.9",
                "cx_Oracle>=8.0",
                "pyodbc>=4.0",
            ],
            "dev": [
                "pytest>=7.0",
                "black>=23.0",
                "isort>=5.0",
                "ruff>=0.0.1",
                "pre-commit>=3.0",
            ],
        },
        classifiers=[
            "Development Status :: 4 - Beta",
            "Intended Audience :: Developers",
            "License :: OSI Approved :: MIT License",
            "Programming Language :: Python :: 3",
            "Programming Language :: Python :: 3.9",
            "Programming Language :: Python :: 3.10",
            "Programming Language :: Python :: 3.11",
            "Topic :: Database",
            "Topic :: Software Development :: Libraries :: Python Modules",
        ],
        python_requires=">=3.9",
        entry_points={
            "console_scripts": [
                "sqly-cli=pysqly.cli:main",
            ],
        },
    )
