# App-Ops MCP Server

MCP server for observability and CI/CD integration. Provides agents with controlled visibility into how your app is running.

## Features

- **CI/CD Integration**: Monitor pipelines and builds (GitHub Actions, GitLab CI, Jenkins, etc.)
- **Log Access**: Retrieve recent error logs
- **Metrics**: Get metric timeseries data
- **Generic Adapters**: Configurable for different CI/CD and observability systems

## Installation

```bash
cd mcp-servers/application/app-ops
python -m venv venv
source venv/bin/activate  # or venv\Scripts\activate on Windows
pip install -r requirements.txt
```

## Configuration

Create a `.env` file in the `application/app-ops` directory:

### GitHub Actions (Default)

```env
# CI/CD Configuration
CICD_TYPE=github_actions
CICD_TOKEN=ghp_your_github_token
CICD_OWNER=your-org
CICD_REPO=your-repo

# Observability (Optional)
LOG_TYPE=generic
LOG_BASE_URL=https://logs.example.com/api
LOG_TOKEN=your-log-token

METRICS_TYPE=generic
METRICS_BASE_URL=https://metrics.example.com/api
METRICS_TOKEN=your-metrics-token

# Monitored services (comma-separated)
MONITORED_SERVICES=api,worker,frontend
```

### Generic CI/CD

```env
CICD_TYPE=generic
CICD_BASE_URL=https://cicd.example.com/api
CICD_TOKEN=your-cicd-token
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
    "app-ops": {
      "command": "python",
      "args": ["/path/to/mcp-servers/application/app-ops/src/index.py"],
      "env": {
        "CICD_TYPE": "github_actions",
        "CICD_TOKEN": "ghp_your_token",
        "CICD_OWNER": "your-org",
        "CICD_REPO": "your-repo"
      }
    }
  }
}
```

## Available Tools

### CI/CD Tools

#### `list_pipelines`

List all CI/CD pipelines.

**Parameters:**
- `limit` (optional): Maximum number of pipelines to return (default: 50)

**Example:**
```json
{
  "limit": 20
}
```

#### `get_pipeline_status`

Get the status of a specific pipeline execution.

**Parameters:**
- `id` (required): Pipeline execution ID

**Example:**
```json
{
  "id": "12345678"
}
```

#### `get_last_failed_build`

Get details of the last failed build for a service.

**Parameters:**
- `service` (required): Service name

**Example:**
```json
{
  "service": "api"
}
```

### Observability Tools

#### `get_recent_errors`

Get recent error logs for a service.

**Parameters:**
- `service` (required): Service name
- `limit` (optional): Maximum number of errors to return (default: 50)
- `time_window` (optional): Time window (e.g., "10m", "1h", "24h") (default: "1h")

**Example:**
```json
{
  "service": "api",
  "limit": 20,
  "time_window": "1h"
}
```

#### `get_metric_timeseries`

Get metric timeseries data.

**Parameters:**
- `service` (required): Service name
- `metric` (required): Metric name (e.g., "cpu_usage", "request_rate", "error_rate")
- `window` (optional): Time window (e.g., "10m", "1h", "24h") (default: "1h")

**Example:**
```json
{
  "service": "api",
  "metric": "request_rate",
  "window": "1h"
}
```

## Available Resources

- `app-ops://pipelines/{id}` - Pipeline configuration/details
- `app-ops://services` - List of monitored services

## Supported CI/CD Systems

### GitHub Actions (Default)

Requires a GitHub personal access token with `repo` scope.

```env
CICD_TYPE=github_actions
CICD_TOKEN=ghp_your_token
CICD_OWNER=your-org
CICD_REPO=your-repo
```

### Generic CI/CD

Works with any CI/CD system that exposes a REST API.

```env
CICD_TYPE=generic
CICD_BASE_URL=https://cicd.example.com/api
CICD_TOKEN=your-token
```

Expected API endpoints:
- `GET /pipelines` - List pipelines
- `GET /pipelines/{id}` - Get pipeline status
- `GET /services/{service}/builds/last-failed` - Get last failed build

## Security

- **Read-Only Access**: All operations are read-only
- **Token Security**: Store tokens in environment variables
- **Least Privilege**: Use tokens with minimal required permissions
- **HTTPS**: Always use HTTPS for API calls

## GitHub Token Setup

1. Go to GitHub Settings → Developer settings → Personal access tokens
2. Generate a new token with `repo` scope
3. Store the token in your `.env` file

## Troubleshooting

**GitHub API errors:**
- Verify token has correct permissions
- Check token hasn't expired
- Ensure repository name is correct (owner/repo format)

**No pipelines found:**
- Verify repository has workflows configured
- Check token has access to the repository
- Ensure workflows have been run at least once

**Observability tools not available:**
- Ensure `LOG_BASE_URL` or `METRICS_BASE_URL` is configured
- Verify API endpoints are accessible
- Check authentication tokens are valid

