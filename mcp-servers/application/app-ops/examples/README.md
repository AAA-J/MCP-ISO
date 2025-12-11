# App-Ops Examples

## Example Usage

### List Pipelines

```python
{
  "limit": 20
}
```

### Get Pipeline Status

```python
{
  "id": "12345678"
}
```

### Get Last Failed Build

```python
{
  "service": "api"
}
```

### Get Recent Errors

```python
{
  "service": "api",
  "limit": 20,
  "time_window": "1h"
}
```

### Get Metrics

```python
{
  "service": "api",
  "metric": "request_rate",
  "window": "1h"
}
```

