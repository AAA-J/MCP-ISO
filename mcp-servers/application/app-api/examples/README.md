# App-API Examples

## Example Usage

### Get User

```python
{
  "id": "user-123"
}
```

### Search Orders

```python
{
  "criteria": {
    "status": "pending",
    "date_from": "2024-01-01",
    "limit": 50
  }
}
```

### Trigger Workflow

```python
{
  "name": "process-payment",
  "params": {
    "order_id": "order-123",
    "amount": 99.99
  }
}
```

### Generic API Call

```python
{
  "endpoint": "products/123",
  "method": "GET"
}

{
  "endpoint": "orders",
  "method": "POST",
  "params": {
    "customer_id": "cust-123",
    "items": [
      {"product_id": "prod-1", "quantity": 2}
    ]
  }
}
```

## Custom Tools Configuration

Create `tools.yaml`:

```yaml
tools:
  - name: get_product
    description: Get product details by ID
    inputSchema:
      type: object
      properties:
        id:
          type: string
          description: Product ID
      required:
        - id
    endpoint: /products/{id}
    method: GET
```

