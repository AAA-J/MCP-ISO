"""Safe query execution tools."""

import re
import sqlparse
from typing import List, Dict, Optional, Tuple
from mcp.types import Tool, TextContent


# Forbidden SQL keywords for read-only access
FORBIDDEN_KEYWORDS = {
    "UPDATE", "DELETE", "INSERT", "DROP", "ALTER", "TRUNCATE",
    "CREATE", "GRANT", "REVOKE", "EXEC", "EXECUTE", "CALL",
    "MERGE", "BULK INSERT", "BACKUP", "RESTORE"
}

# Allowed SQL keywords (SELECT and related)
ALLOWED_KEYWORDS = {
    "SELECT", "FROM", "WHERE", "JOIN", "INNER JOIN", "LEFT JOIN",
    "RIGHT JOIN", "FULL JOIN", "GROUP BY", "ORDER BY", "HAVING",
    "LIMIT", "OFFSET", "UNION", "UNION ALL", "WITH", "AS", "AND", "OR",
    "IN", "EXISTS", "LIKE", "ILIKE", "BETWEEN", "IS NULL", "IS NOT NULL",
    "COUNT", "SUM", "AVG", "MAX", "MIN", "DISTINCT", "TOP"  # TOP for SQL Server
}


query_tools = [
    Tool(
        name="run_safe_query",
        description="Execute a validated read-only SQL query. Only SELECT statements are allowed.",
        inputSchema={
            "type": "object",
            "properties": {
                "sql": {
                    "type": "string",
                    "description": "SQL query to execute (must be a SELECT statement)"
                },
                "query_id": {
                    "type": "string",
                    "description": "Optional pre-defined query ID from whitelist"
                },
                "limit": {
                    "type": "integer",
                    "description": "Maximum number of rows to return (default: 100)",
                    "default": 100
                }
            }
        }
    ),
]


def validate_sql_readonly(sql: str) -> Tuple[bool, Optional[str]]:
    """
    Validate that SQL query is read-only.
    Returns (is_valid, error_message)
    """
    if not sql or not sql.strip():
        return False, "Empty SQL query"
    
    # Normalize SQL
    sql_upper = sql.upper().strip()
    
    # Remove comments
    sql_upper = re.sub(r'--.*?$', '', sql_upper, flags=re.MULTILINE)
    sql_upper = re.sub(r'/\*.*?\*/', '', sql_upper, flags=re.DOTALL)
    
    # Check for forbidden keywords
    for keyword in FORBIDDEN_KEYWORDS:
        # Use word boundaries to avoid false positives
        pattern = r'\b' + re.escape(keyword) + r'\b'
        if re.search(pattern, sql_upper, re.IGNORECASE):
            return False, f"Forbidden keyword detected: {keyword}. Only SELECT queries are allowed."
    
    # Must start with SELECT or WITH (for CTEs)
    if not (sql_upper.startswith("SELECT") or sql_upper.startswith("WITH")):
        return False, "Query must start with SELECT or WITH (for CTEs). Only read-only queries are allowed."
    
    # Parse SQL to validate structure
    try:
        parsed = sqlparse.parse(sql)
        if not parsed:
            return False, "Invalid SQL syntax"
        
        # Check each statement
        for statement in parsed:
            stmt_type = statement.get_type()
            if stmt_type not in ["SELECT", "UNKNOWN"]:  # UNKNOWN might be CTE
                # Double-check by looking at tokens
                tokens = [t.value.upper() for t in statement.tokens if t.ttype is None]
                if any(kw in tokens for kw in FORBIDDEN_KEYWORDS):
                    return False, f"Statement type '{stmt_type}' is not allowed. Only SELECT queries are permitted."
    except Exception as e:
        return False, f"SQL parsing error: {str(e)}"
    
    # Check for SQL injection patterns
    dangerous_patterns = [
        r';\s*(UPDATE|DELETE|INSERT|DROP|ALTER)',
        r'--',
        r'/\*',
        r'xp_',  # SQL Server extended procedures
        r'sp_',  # SQL Server stored procedures (some are dangerous)
    ]
    
    for pattern in dangerous_patterns:
        if re.search(pattern, sql_upper, re.IGNORECASE):
            return False, f"Potentially dangerous pattern detected: {pattern}"
    
    return True, None


async def handle_query(name: str, arguments: dict, db_connection, query_whitelist: Optional[Dict] = None) -> List[TextContent]:
    """Handle query execution tool calls."""
    if name == "run_safe_query":
        query_id = arguments.get("query_id")
        sql = arguments.get("sql")
        limit = arguments.get("limit", 100)
        
        # If query_id is provided, use whitelist
        if query_id and query_whitelist:
            if query_id not in query_whitelist:
                return [TextContent(
                    type="text",
                    text=f"Error: Query ID '{query_id}' not found in whitelist"
                )]
            sql = query_whitelist[query_id]["sql"]
        
        if not sql:
            return [TextContent(
                type="text",
                text="Error: Either 'sql' or 'query_id' parameter is required"
            )]
        
        # Validate SQL
        is_valid, error_msg = validate_sql_readonly(sql)
        if not is_valid:
            return [TextContent(
                type="text",
                text=f"Query validation failed: {error_msg}"
            )]
        
        # Add LIMIT if not present (for safety)
        sql_upper = sql.upper()
        db_type = db_connection.get("type", "azure_sql")
        
        if "LIMIT" not in sql_upper and "TOP" not in sql_upper:
            if db_type in ["azure_sql", "sql_server"]:
                # SQL Server uses TOP
                sql = f"SELECT TOP {limit} * FROM ({sql}) AS subquery"
            elif db_type in ["postgresql", "mysql", "sqlite"]:
                sql = f"{sql} LIMIT {limit}"
        
        # Execute query
        try:
            result = await execute_readonly_query(db_connection, sql, limit)
            return [TextContent(type="text", text=result)]
        except Exception as e:
            return [TextContent(
                type="text",
                text=f"Query execution error: {str(e)}"
            )]
    
    else:
        raise ValueError(f"Unknown query tool: {name}")


async def execute_readonly_query(db_connection, sql: str, limit: int = 100) -> str:
    """Execute a read-only query and return formatted results."""
    db_type = db_connection.get("type", "azure_sql")
    conn = db_connection["connection"]
    cursor = conn.cursor()
    
    try:
        cursor.execute(sql)
        
        # Get column names
        columns = [desc[0] for desc in cursor.description] if cursor.description else []
        
        # Fetch results (respect limit)
        rows = cursor.fetchmany(limit)
        
        if not rows:
            return "Query executed successfully. No rows returned."
        
        # Format as markdown table
        result = f"Query returned {len(rows)} row(s):\n\n"
        result += "| " + " | ".join(columns) + " |\n"
        result += "|" + "|".join(["---" for _ in columns]) + "|\n"
        
        for row in rows:
            # Convert values to strings, handle None
            row_str = [str(val) if val is not None else "NULL" for val in row]
            result += "| " + " | ".join(row_str) + " |\n"
        
        if len(rows) == limit:
            result += f"\n*Results limited to {limit} rows*"
        
        return result
    
    finally:
        cursor.close()

