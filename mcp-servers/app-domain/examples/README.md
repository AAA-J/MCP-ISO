# App-Domain Examples

## Example Usage

### Calculate Interest Schedule

```python
{
  "principal": 100000,
  "rate": 0.05,
  "term_months": 360
}
```

### Simulate Portfolio

```python
{
  "investments": [
    {"symbol": "AAPL", "amount": 10000},
    {"symbol": "GOOGL", "amount": 5000}
  ],
  "timeframe": "1y"
}
```

### Create Project

```python
{
  "name": "New Project",
  "description": "Project description",
  "owner_id": "user-123"
}
```

### Add Task

```python
{
  "project_id": "project-123",
  "title": "Implement feature X",
  "description": "Task description",
  "assignee_id": "user-456"
}
```

### Reassign Task

```python
{
  "task_id": "task-789",
  "assignee_id": "user-999"
}
```

