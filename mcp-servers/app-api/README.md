# App-API MCP Server

MCP server that wraps your backend API with typed tools. Provides a clean interface for agents to interact with your API.

## Features

- **Typed Tools**: Domain-level tool names instead of raw HTTP details
- **Multi-Framework Support**: REST, GraphQL, FastAPI, Express.js
- **Authentication**: Bearer token, API key, or Basic auth
- **Configurable**: Extend tools via YAML/JSON configuration

## Installation

```bash
cd mcp-servers/app-api
python -m venv venv
source venv/bin/activate  # or venv\Scripts\activate on Windows
pip install -r requirements.txt
```

## Configuration

Create a `.env` file in the `app-api` directory:

### Basic Configuration

```env
# API base URL
API_BASE_URL=http://localhost:8000

# API type: rest, graphql, fastapi, express
API_TYPE=rest

# Authentication type: bearer, api_key, basic
AUTH_TYPE=bearer

# Bearer token
AUTH_TOKEN=your-token-here

# Or API key
# API_KEY=your-api-key
# API_KEY_NAME=X-API-Key

# Or Basic auth
# AUTH_USERNAME=username
# AUTH_PASSWORD=password

# Optional: Tool configuration file
TOOL_CONFIG_FILE=tools.yaml
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
    "app-api": {
      "command": "python",
      "args": ["/path/to/mcp-servers/app-api/src/index.py"],
      "env": {
        "API_BASE_URL": "https://api.example.com",
        "API_TYPE": "rest",
        "AUTH_TYPE": "bearer",
        "AUTH_TOKEN": "your-token"
      }
    }
  }
}
```

## Available Tools

### Default Tools

- `get_user(id)` - Get user by ID
- `search_orders(criteria)` - Search orders with filters
- `trigger_workflow(name, params)` - Trigger backend workflow
- `simulate_pricing(input)` - Run pricing calculations
- `call_api(endpoint, method, params)` - Generic API call

### Custom Tools

Define custom tools in a YAML configuration file:

```yaml
tools:
  - name: create_invoice
    description: Create a new invoice
    inputSchema:
      type: object
      properties:
        customer_id:
          type: string
        amount:
          type: number
        items:
          type: array
          items:
            type: object
      required:
        - customer_id
        - amount
```

## Tool Configuration

Create a `tools.yaml` file to define custom API tools:

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
    # Endpoint mapping (optional, defaults to /{tool_name})
    endpoint: /products/{id}
    method: GET
```

## API Types

### REST API (Default)

Standard REST API with JSON requests/responses.

```env
API_TYPE=rest
API_BASE_URL=https://api.example.com
```

### GraphQL

GraphQL API support (requires `gql` package).

```env
API_TYPE=graphql
API_BASE_URL=https://api.example.com/graphql
```

Install GraphQL support:
```bash
pip install gql[aiohttp]
```

### FastAPI / Flask

Auto-discovery of OpenAPI schema (future enhancement).

```env
API_TYPE=fastapi
API_BASE_URL=https://api.example.com
```

### Express.js

Standard REST patterns for Node.js APIs.

```env
API_TYPE=express
API_BASE_URL=https://api.example.com
```

## Authentication

### Bearer Token (Default)

```env
AUTH_TYPE=bearer
AUTH_TOKEN=your-token-here
```

### API Key

```env
AUTH_TYPE=api_key
API_KEY=your-api-key
API_KEY_NAME=X-API-Key  # Optional, defaults to X-API-Key
```

### Basic Authentication

```env
AUTH_TYPE=basic
AUTH_USERNAME=username
AUTH_PASSWORD=password
```

## Security

- **Token Storage**: Store tokens in environment variables, never in code
- **HTTPS**: Always use HTTPS for API calls in production
- **Rate Limiting**: Be aware of API rate limits
- **Error Handling**: Errors don't expose sensitive information

## Examples

See the `examples/` directory for usage examples.

## Troubleshooting

**Connection errors:**
- Verify `API_BASE_URL` is correct and accessible
- Check network connectivity and firewall rules
- Ensure authentication credentials are valid

**Authentication errors:**
- Verify token/key is correct and not expired
- Check authentication type matches your API
- Ensure headers are set correctly

**Tool not found:**
- Check tool name matches configuration
- Verify tool configuration file is loaded correctly
- Check tool endpoint mapping

