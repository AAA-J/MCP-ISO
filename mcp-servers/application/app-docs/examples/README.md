# App-Docs Examples

## Example Usage

### Search Documentation

```python
# Search for authentication-related docs
{
  "query": "authentication",
  "limit": 5
}
```

### Get Diagram

```python
# Get architecture diagram
{
  "name": "architecture-diagram"
}
```

### Read Resource

Access documentation via resources:

- `app-docs://docs/architecture` - Architecture documentation
- `app-docs://docs/backend` - Backend documentation
- `app-docs://diagrams/architecture.svg` - Architecture diagram

