#!/usr/bin/env python3
"""
App-DB-Readonly MCP Server - Safe database access
Provides read-only access to database schema and data for agents
"""

import asyncio
import os
from dotenv import load_dotenv
from mcp.server import Server
from mcp.server.stdio import stdio_server
from mcp.types import Tool, Resource, TextContent

from schema.tools import schema_tools, handle_schema
from query.tools import query_tools, handle_query

# Load environment variables
load_dotenv()

# Initialize MCP server
server = Server("app-db-readonly")

# Database connection (lazy initialization)
_db_connection = None
_query_whitelist = None


def get_db_connection():
    """Get or create database connection."""
    global _db_connection
    
    if _db_connection is not None:
        return _db_connection
    
    db_type = os.getenv("DB_TYPE", "azure_sql").lower()
    connection_string = os.getenv("DB_CONNECTION_STRING")
    
    if not connection_string:
        raise ValueError("DB_CONNECTION_STRING environment variable is required")
    
    if db_type in ["azure_sql", "sql_server"]:
        import pyodbc
        conn = pyodbc.connect(connection_string)
        _db_connection = {
            "type": "azure_sql",
            "connection": conn
        }
    elif db_type == "postgresql":
        import psycopg2
        conn = psycopg2.connect(connection_string)
        _db_connection = {
            "type": "postgresql",
            "connection": conn
        }
    elif db_type == "mysql":
        import pymysql
        conn = pymysql.connect(connection_string)
        _db_connection = {
            "type": "mysql",
            "connection": conn
        }
    elif db_type == "sqlite":
        import sqlite3
        conn = sqlite3.connect(connection_string)
        _db_connection = {
            "type": "sqlite",
            "connection": conn
        }
    else:
        raise ValueError(f"Unsupported database type: {db_type}")
    
    return _db_connection


def get_query_whitelist():
    """Load query whitelist from environment or config file."""
    global _query_whitelist
    
    if _query_whitelist is not None:
        return _query_whitelist
    
    # For now, return empty dict. Can be extended to load from file
    _query_whitelist = {}
    
    # TODO: Load from YAML/JSON file if QUERY_WHITELIST_FILE is set
    whitelist_file = os.getenv("QUERY_WHITELIST_FILE")
    if whitelist_file and os.path.exists(whitelist_file):
        import yaml
        with open(whitelist_file, 'r') as f:
            _query_whitelist = yaml.safe_load(f) or {}
    
    return _query_whitelist


@server.list_tools()
async def list_tools() -> list[Tool]:
    """List all available tools."""
    return schema_tools + query_tools


@server.call_tool()
async def call_tool(name: str, arguments: dict) -> list[TextContent]:
    """Handle tool calls."""
    db_conn = get_db_connection()
    whitelist = get_query_whitelist()
    
    if name in ["list_tables", "describe_table"]:
        return await handle_schema(name, arguments, db_conn)
    elif name == "run_safe_query":
        return await handle_query(name, arguments, db_conn, whitelist)
    else:
        raise ValueError(f"Unknown tool: {name}")


@server.list_resources()
async def list_resources() -> list[Resource]:
    """List available database resources."""
    db_conn = get_db_connection()
    
    # Get schema resource
    resources = [
        Resource(
            uri="app-db://schema",
            name="Database Schema",
            description="Full database schema (DDL)",
            mimeType="text/plain"
        )
    ]
    
    # Add table resources
    try:
        from schema.tools import list_tables
        tables = await list_tables(db_conn)
        for table in tables:
            table_name = table["name"]
            schema_name = table.get("schema")
            if schema_name:
                uri = f"app-db://schema/{schema_name}.{table_name}"
            else:
                uri = f"app-db://schema/{table_name}"
            
            resources.append(Resource(
                uri=uri,
                name=f"Table: {table_name}",
                description=f"Schema for table {table_name}",
                mimeType="text/plain"
            ))
    except Exception as e:
        # If we can't list tables, just return schema resource
        pass
    
    return resources


@server.read_resource()
async def read_resource(uri: str) -> str:
    """Read a database resource."""
    uri_str = str(uri)
    db_conn = get_db_connection()
    
    if uri_str == "app-db://schema":
        # Return full schema
        from schema.tools import list_tables, describe_table
        tables = await list_tables(db_conn)
        
        result = "# Database Schema\n\n"
        for table in tables:
            table_name = table["name"]
            schema_name = table.get("schema")
            description = await describe_table(db_conn, table_name, schema_name)
            result += description + "\n\n"
        
        return result
    
    elif uri_str.startswith("app-db://schema/"):
        # Extract table name
        table_path = uri_str.replace("app-db://schema/", "")
        parts = table_path.split(".")
        
        if len(parts) == 2:
            schema_name, table_name = parts
        else:
            schema_name = None
            table_name = parts[0]
        
        from schema.tools import describe_table
        return await describe_table(db_conn, table_name, schema_name)
    
    else:
        raise ValueError(f"Unknown resource: {uri_str}")


async def main():
    """Main entry point."""
    async with stdio_server() as (read_stream, write_stream):
        await server.run(
            read_stream,
            write_stream,
            server.create_initialization_options()
        )


if __name__ == "__main__":
    asyncio.run(main())

