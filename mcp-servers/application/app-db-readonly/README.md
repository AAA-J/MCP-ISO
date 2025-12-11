# App-DB-Readonly MCP Server

MCP server for safe, read-only database access. Provides agents with controlled access to database schema and data.

## Features

- **Schema Inspection**: List tables and describe table structures
- **Safe Query Execution**: Execute validated read-only SQL queries
- **Multi-Database Support**: Azure SQL, PostgreSQL, MySQL, SQLite
- **Security-First**: Strict read-only enforcement with SQL injection prevention

## Installation

```bash
cd mcp-servers/application/app-db-readonly
python -m venv venv
source venv/bin/activate  # or venv\Scripts\activate on Windows
pip install -r requirements.txt
```

## Configuration

Create a `.env` file in the `application/app-db-readonly` directory:

### Azure SQL Database (Default)

```env
DB_TYPE=azure_sql
DB_CONNECTION_STRING=Driver={ODBC Driver 18 for SQL Server};Server=tcp:your-server.database.windows.net,1433;Database=your-db;Uid=readonly-user;Pwd=your-password;Encrypt=yes;TrustServerCertificate=no;Connection Timeout=30;
```

### PostgreSQL

```env
DB_TYPE=postgresql
DB_CONNECTION_STRING=postgresql://readonly-user:password@localhost:5432/dbname
```

### MySQL

```env
DB_TYPE=mysql
DB_CONNECTION_STRING=mysql://readonly-user:password@localhost:3306/dbname
```

### SQLite

```env
DB_TYPE=sqlite
DB_CONNECTION_STRING=/path/to/database.db
```

### Optional: Query Whitelist

```env
QUERY_WHITELIST_FILE=/path/to/query_whitelist.yaml
```

## Usage

### Running the Server

```bash
python src/index.py
```

### Configuring in MCP Client

Add to your MCP client configuration:

```json
{
  "mcpServers": {
    "app-db-readonly": {
      "command": "python",
      "args": ["/path/to/mcp-servers/application/app-db-readonly/src/index.py"],
      "env": {
        "DB_TYPE": "azure_sql",
        "DB_CONNECTION_STRING": "your-connection-string"
      }
    }
  }
}
```

## Available Tools

### `list_tables`

List all tables in the database.

**Parameters:**
- `schema` (optional): Schema name to filter tables (database-specific)

**Example:**
```json
{
  "schema": "dbo"
}
```

### `describe_table`

Get detailed information about a table including columns, indexes, and constraints.

**Parameters:**
- `table_name` (required): Name of the table to describe
- `schema` (optional): Schema name (database-specific)

**Example:**
```json
{
  "table_name": "users",
  "schema": "dbo"
}
```

### `run_safe_query`

Execute a validated read-only SQL query. Only SELECT statements are allowed.

**Parameters:**
- `sql` (required if `query_id` not provided): SQL query to execute
- `query_id` (optional): Pre-defined query ID from whitelist
- `limit` (optional): Maximum number of rows to return (default: 100)

**Example:**
```json
{
  "sql": "SELECT id, name, email FROM users WHERE active = 1",
  "limit": 50
}
```

## Available Resources

- `app-db://schema` - Full database schema (DDL)
- `app-db://schema/{table}` - Individual table schema
- `app-db://schema/{schema}.{table}` - Table schema with schema name

## Security

### Read-Only Enforcement

- **Query Validation**: All queries are validated to ensure they are read-only
- **Forbidden Keywords**: UPDATE, DELETE, INSERT, DROP, ALTER, TRUNCATE, etc. are blocked
- **SQL Injection Prevention**: Parameterized queries and input validation
- **Automatic LIMIT**: Queries are automatically limited to prevent large result sets

### Best Practices

1. **Use Read-Only Database User**: Create a dedicated database user with read-only permissions
2. **Least Privilege**: Grant only SELECT permissions on necessary tables
3. **Connection String Security**: Store connection strings in environment variables, never in code
4. **Query Whitelist**: Use query whitelist for frequently used queries
5. **Monitor Usage**: Log all queries for auditing purposes

### Query Whitelist Format

Create a YAML file with pre-approved queries:

```yaml
active_users:
  description: "Get all active users"
  sql: "SELECT id, name, email FROM users WHERE active = 1"

recent_orders:
  description: "Get recent orders"
  sql: "SELECT * FROM orders WHERE created_at > DATEADD(day, -7, GETDATE()) ORDER BY created_at DESC"
```

## Supported Databases

- **Azure SQL Database** (default) - Using `pyodbc`
- **PostgreSQL** - Using `psycopg2`
- **MySQL** - Using `pymysql`
- **SQLite** - Using built-in `sqlite3`

## Troubleshooting

**Connection errors:**
- Verify connection string format for your database type
- Check network connectivity and firewall rules
- Ensure database user has read permissions

**Query validation errors:**
- Only SELECT queries are allowed
- Check for forbidden keywords in your query
- Ensure query syntax is correct for your database type

**Performance issues:**
- Use query limits to prevent large result sets
- Consider using query whitelist for common queries
- Add appropriate indexes to your database

