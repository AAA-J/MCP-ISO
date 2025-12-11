"""Database schema inspection tools."""

import re
from typing import List, Dict, Optional
from mcp.types import Tool, TextContent, Resource


schema_tools = [
    Tool(
        name="list_tables",
        description="List all tables in the database",
        inputSchema={
            "type": "object",
            "properties": {
                "schema": {
                    "type": "string",
                    "description": "Optional schema name to filter tables (database-specific)",
                    "default": None
                }
            }
        }
    ),
    Tool(
        name="describe_table",
        description="Get detailed information about a table including columns, indexes, and constraints",
        inputSchema={
            "type": "object",
            "properties": {
                "table_name": {
                    "type": "string",
                    "description": "Name of the table to describe"
                },
                "schema": {
                    "type": "string",
                    "description": "Optional schema name (database-specific)",
                    "default": None
                }
            },
            "required": ["table_name"]
        }
    ),
]


async def handle_schema(name: str, arguments: dict, db_connection) -> List[TextContent]:
    """Handle schema inspection tool calls."""
    if name == "list_tables":
        schema_name = arguments.get("schema")
        tables = await list_tables(db_connection, schema_name)
        
        if not tables:
            return [TextContent(
                type="text",
                text="No tables found in the database."
            )]
        
        result = f"Found {len(tables)} table(s):\n\n"
        for table in tables:
            result += f"- **{table['name']}**"
            if table.get('schema'):
                result += f" (schema: {table['schema']})"
            if table.get('type'):
                result += f" [{table['type']}]"
            result += "\n"
        
        return [TextContent(type="text", text=result)]
    
    elif name == "describe_table":
        table_name = arguments.get("table_name")
        schema_name = arguments.get("schema")
        
        if not table_name:
            return [TextContent(
                type="text",
                text="Error: table_name parameter is required"
            )]
        
        description = await describe_table(db_connection, table_name, schema_name)
        return [TextContent(type="text", text=description)]
    
    else:
        raise ValueError(f"Unknown schema tool: {name}")


async def list_tables(db_connection, schema: Optional[str] = None) -> List[Dict]:
    """List all tables in the database."""
    db_type = db_connection.get("type", "azure_sql")
    
    if db_type in ["azure_sql", "sql_server"]:
        return await _list_tables_azure_sql(db_connection, schema)
    elif db_type == "postgresql":
        return await _list_tables_postgresql(db_connection, schema)
    elif db_type == "mysql":
        return await _list_tables_mysql(db_connection, schema)
    elif db_type == "sqlite":
        return await _list_tables_sqlite(db_connection)
    else:
        raise ValueError(f"Unsupported database type: {db_type}")


async def describe_table(db_connection, table_name: str, schema: Optional[str] = None) -> str:
    """Get detailed table description."""
    db_type = db_connection.get("type", "azure_sql")
    
    if db_type in ["azure_sql", "sql_server"]:
        return await _describe_table_azure_sql(db_connection, table_name, schema)
    elif db_type == "postgresql":
        return await _describe_table_postgresql(db_connection, table_name, schema)
    elif db_type == "mysql":
        return await _describe_table_mysql(db_connection, table_name, schema)
    elif db_type == "sqlite":
        return await _describe_table_sqlite(db_connection, table_name)
    else:
        raise ValueError(f"Unsupported database type: {db_type}")


# Azure SQL / SQL Server implementations
async def _list_tables_azure_sql(db_connection, schema: Optional[str] = None) -> List[Dict]:
    """List tables for Azure SQL / SQL Server."""
    import pyodbc
    
    conn = db_connection["connection"]
    cursor = conn.cursor()
    
    if schema:
        query = """
            SELECT TABLE_SCHEMA, TABLE_NAME, TABLE_TYPE
            FROM INFORMATION_SCHEMA.TABLES
            WHERE TABLE_TYPE = 'BASE TABLE' AND TABLE_SCHEMA = ?
            ORDER BY TABLE_SCHEMA, TABLE_NAME
        """
        cursor.execute(query, (schema,))
    else:
        query = """
            SELECT TABLE_SCHEMA, TABLE_NAME, TABLE_TYPE
            FROM INFORMATION_SCHEMA.TABLES
            WHERE TABLE_TYPE = 'BASE TABLE'
            ORDER BY TABLE_SCHEMA, TABLE_NAME
        """
        cursor.execute(query)
    
    tables = []
    for row in cursor.fetchall():
        tables.append({
            "schema": row[0],
            "name": row[1],
            "type": row[2]
        })
    
    return tables


async def _describe_table_azure_sql(db_connection, table_name: str, schema: Optional[str] = None) -> str:
    """Describe table for Azure SQL / SQL Server."""
    import pyodbc
    
    conn = db_connection["connection"]
    cursor = conn.cursor()
    
    # Get columns
    if schema:
        query = """
            SELECT COLUMN_NAME, DATA_TYPE, CHARACTER_MAXIMUM_LENGTH, 
                   IS_NULLABLE, COLUMN_DEFAULT, ORDINAL_POSITION
            FROM INFORMATION_SCHEMA.COLUMNS
            WHERE TABLE_NAME = ? AND TABLE_SCHEMA = ?
            ORDER BY ORDINAL_POSITION
        """
        cursor.execute(query, (table_name, schema))
    else:
        query = """
            SELECT COLUMN_NAME, DATA_TYPE, CHARACTER_MAXIMUM_LENGTH, 
                   IS_NULLABLE, COLUMN_DEFAULT, ORDINAL_POSITION
            FROM INFORMATION_SCHEMA.COLUMNS
            WHERE TABLE_NAME = ?
            ORDER BY ORDINAL_POSITION
        """
        cursor.execute(query, (table_name,))
    
    columns = cursor.fetchall()
    
    result = f"## Table: {table_name}\n\n"
    if schema:
        result += f"**Schema:** {schema}\n\n"
    
    result += "### Columns\n\n"
    result += "| Name | Type | Length | Nullable | Default |\n"
    result += "|------|------|--------|----------|---------|\n"
    
    for col in columns:
        col_name, data_type, max_length, nullable, default, _ = col
        length_str = str(max_length) if max_length else ""
        default_str = str(default) if default else ""
        result += f"| {col_name} | {data_type} | {length_str} | {nullable} | {default_str} |\n"
    
    # Get indexes
    if schema:
        query = """
            SELECT i.name AS INDEX_NAME, i.is_unique, i.is_primary_key,
                   STRING_AGG(c.name, ', ') WITHIN GROUP (ORDER BY ic.key_ordinal) AS COLUMNS
            FROM sys.indexes i
            INNER JOIN sys.index_columns ic ON i.object_id = ic.object_id AND i.index_id = ic.index_id
            INNER JOIN sys.columns c ON ic.object_id = c.object_id AND ic.column_id = c.column_id
            INNER JOIN sys.tables t ON i.object_id = t.object_id
            INNER JOIN sys.schemas s ON t.schema_id = s.schema_id
            WHERE t.name = ? AND s.name = ?
            GROUP BY i.name, i.is_unique, i.is_primary_key
        """
        cursor.execute(query, (table_name, schema))
    else:
        query = """
            SELECT i.name AS INDEX_NAME, i.is_unique, i.is_primary_key,
                   STRING_AGG(c.name, ', ') WITHIN GROUP (ORDER BY ic.key_ordinal) AS COLUMNS
            FROM sys.indexes i
            INNER JOIN sys.index_columns ic ON i.object_id = ic.object_id AND i.index_id = ic.index_id
            INNER JOIN sys.columns c ON ic.object_id = c.object_id AND ic.column_id = c.column_id
            INNER JOIN sys.tables t ON i.object_id = t.object_id
            WHERE t.name = ?
            GROUP BY i.name, i.is_unique, i.is_primary_key
        """
        cursor.execute(query, (table_name,))
    
    indexes = cursor.fetchall()
    if indexes:
        result += "\n### Indexes\n\n"
        for idx in indexes:
            idx_name, is_unique, is_pk, cols = idx
            idx_type = "PRIMARY KEY" if is_pk else ("UNIQUE" if is_unique else "INDEX")
            result += f"- **{idx_name}** ({idx_type}): {cols}\n"
    
    return result


# PostgreSQL implementations
async def _list_tables_postgresql(db_connection, schema: Optional[str] = None) -> List[Dict]:
    """List tables for PostgreSQL."""
    import psycopg2
    
    conn = db_connection["connection"]
    cursor = conn.cursor()
    
    if schema:
        query = """
            SELECT table_schema, table_name, table_type
            FROM information_schema.tables
            WHERE table_type = 'BASE TABLE' AND table_schema = %s
            ORDER BY table_schema, table_name
        """
        cursor.execute(query, (schema,))
    else:
        query = """
            SELECT table_schema, table_name, table_type
            FROM information_schema.tables
            WHERE table_type = 'BASE TABLE'
            ORDER BY table_schema, table_name
        """
        cursor.execute(query)
    
    tables = []
    for row in cursor.fetchall():
        tables.append({
            "schema": row[0],
            "name": row[1],
            "type": row[2]
        })
    
    return tables


async def _describe_table_postgresql(db_connection, table_name: str, schema: Optional[str] = None) -> str:
    """Describe table for PostgreSQL."""
    import psycopg2
    
    conn = db_connection["connection"]
    cursor = conn.cursor()
    
    # Get columns
    if schema:
        query = """
            SELECT column_name, data_type, character_maximum_length,
                   is_nullable, column_default, ordinal_position
            FROM information_schema.columns
            WHERE table_name = %s AND table_schema = %s
            ORDER BY ordinal_position
        """
        cursor.execute(query, (table_name, schema))
    else:
        query = """
            SELECT column_name, data_type, character_maximum_length,
                   is_nullable, column_default, ordinal_position
            FROM information_schema.columns
            WHERE table_name = %s
            ORDER BY ordinal_position
        """
        cursor.execute(query, (table_name,))
    
    columns = cursor.fetchall()
    
    result = f"## Table: {table_name}\n\n"
    if schema:
        result += f"**Schema:** {schema}\n\n"
    
    result += "### Columns\n\n"
    result += "| Name | Type | Length | Nullable | Default |\n"
    result += "|------|------|--------|----------|---------|\n"
    
    for col in columns:
        col_name, data_type, max_length, nullable, default, _ = col
        length_str = str(max_length) if max_length else ""
        default_str = str(default) if default else ""
        result += f"| {col_name} | {data_type} | {length_str} | {nullable} | {default_str} |\n"
    
    # Get indexes
    if schema:
        query = """
            SELECT indexname, indexdef
            FROM pg_indexes
            WHERE tablename = %s AND schemaname = %s
        """
        cursor.execute(query, (table_name, schema))
    else:
        query = """
            SELECT indexname, indexdef
            FROM pg_indexes
            WHERE tablename = %s
        """
        cursor.execute(query, (table_name,))
    
    indexes = cursor.fetchall()
    if indexes:
        result += "\n### Indexes\n\n"
        for idx in indexes:
            idx_name, idx_def = idx
            result += f"- **{idx_name}**: {idx_def}\n"
    
    return result


# MySQL implementations
async def _list_tables_mysql(db_connection, schema: Optional[str] = None) -> List[Dict]:
    """List tables for MySQL."""
    import pymysql
    
    conn = db_connection["connection"]
    cursor = conn.cursor()
    
    if schema:
        query = "SHOW TABLES FROM `{}`".format(schema)
        cursor.execute(query)
    else:
        query = "SHOW TABLES"
        cursor.execute(query)
    
    tables = []
    for row in cursor.fetchall():
        tables.append({
            "name": row[0],
            "type": "BASE TABLE"
        })
    
    return tables


async def _describe_table_mysql(db_connection, table_name: str, schema: Optional[str] = None) -> str:
    """Describe table for MySQL."""
    import pymysql
    
    conn = db_connection["connection"]
    cursor = conn.cursor()
    
    if schema:
        query = f"DESCRIBE `{schema}`.`{table_name}`"
    else:
        query = f"DESCRIBE `{table_name}`"
    
    cursor.execute(query)
    columns = cursor.fetchall()
    
    result = f"## Table: {table_name}\n\n"
    if schema:
        result += f"**Schema:** {schema}\n\n"
    
    result += "### Columns\n\n"
    result += "| Field | Type | Null | Key | Default | Extra |\n"
    result += "|-------|------|------|-----|---------|-------|\n"
    
    for col in columns:
        result += f"| {' | '.join(str(x) if x else '' for x in col)} |\n"
    
    return result


# SQLite implementations
async def _list_tables_sqlite(db_connection) -> List[Dict]:
    """List tables for SQLite."""
    conn = db_connection["connection"]
    cursor = conn.cursor()
    
    cursor.execute("SELECT name FROM sqlite_master WHERE type='table' ORDER BY name")
    tables = []
    for row in cursor.fetchall():
        tables.append({
            "name": row[0],
            "type": "table"
        })
    
    return tables


async def _describe_table_sqlite(db_connection, table_name: str) -> str:
    """Describe table for SQLite."""
    conn = db_connection["connection"]
    cursor = conn.cursor()
    
    cursor.execute(f"PRAGMA table_info({table_name})")
    columns = cursor.fetchall()
    
    result = f"## Table: {table_name}\n\n"
    result += "### Columns\n\n"
    result += "| cid | name | type | notnull | dflt_value | pk |\n"
    result += "|-----|------|------|---------|------------|----|\n"
    
    for col in columns:
        result += f"| {' | '.join(str(x) if x is not None else '' for x in col)} |\n"
    
    return result

