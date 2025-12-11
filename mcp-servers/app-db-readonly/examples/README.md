# App-DB-Readonly Examples

## Example Usage

### List Tables

```python
# List all tables
{
  "limit": 50
}

# List tables in specific schema
{
  "schema": "dbo"
}
```

### Describe Table

```python
# Get table structure
{
  "table_name": "users",
  "schema": "dbo"
}
```

### Run Safe Query

```python
# Simple SELECT query
{
  "sql": "SELECT id, name, email FROM users WHERE active = 1",
  "limit": 50
}

# Query with JOIN
{
  "sql": "SELECT u.name, o.total FROM users u JOIN orders o ON u.id = o.user_id WHERE o.created_at > '2024-01-01'",
  "limit": 100
}
```

## Query Whitelist Example

Create `query_whitelist.yaml`:

```yaml
active_users:
  description: "Get all active users"
  sql: "SELECT id, name, email FROM users WHERE active = 1"

recent_orders:
  description: "Get recent orders"
  sql: "SELECT * FROM orders WHERE created_at > DATEADD(day, -7, GETDATE()) ORDER BY created_at DESC"
```

Then use query ID:

```python
{
  "query_id": "active_users"
}
```

