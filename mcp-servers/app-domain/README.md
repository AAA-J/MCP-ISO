# App-Domain MCP Server

MCP server for domain-specific business logic shortcuts. Provides typed tools for business operations.

## Features

- **Domain Tools**: Business logic shortcuts (e.g., `calculate_interest_schedule`, `create_project`)
- **Configurable**: Define tools via YAML configuration
- **API Integration**: Execute tools via API calls or Python functions
- **Type Safety**: Typed input/output schemas for all tools

## Installation

```bash
cd mcp-servers/app-domain
python -m venv venv
source venv/bin/activate  # or venv\Scripts\activate on Windows
pip install -r requirements.txt
```

## Configuration

Create a `.env` file in the `app-domain` directory:

```env
# Domain tools configuration file
DOMAIN_TOOLS_CONFIG=domain_tools.yaml

# API base URL (for API-based tools)
API_BASE_URL=https://api.example.com

# Authentication
AUTH_TYPE=bearer
AUTH_TOKEN=your-token-here

# Or API key
# AUTH_TYPE=api_key
# API_KEY=your-api-key
# API_KEY_NAME=X-API-Key
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
    "app-domain": {
      "command": "python",
      "args": ["/path/to/mcp-servers/app-domain/src/index.py"],
      "env": {
        "DOMAIN_TOOLS_CONFIG": "domain_tools.yaml",
        "API_BASE_URL": "https://api.example.com",
        "AUTH_TOKEN": "your-token"
      }
    }
  }
}
```

## Tool Configuration

Define your domain tools in `domain_tools.yaml`:

```yaml
tools:
  - name: calculate_interest_schedule
    description: Calculate interest schedule for a loan
    execution: api  # or "function"
    method: POST
    endpoint: /finance/calculate-interest
    inputSchema:
      type: object
      properties:
        principal:
          type: number
          description: Loan principal amount
        rate:
          type: number
          description: Annual interest rate (as decimal)
        term_months:
          type: integer
          description: Loan term in months
      required:
        - principal
        - rate
        - term_months

  - name: create_project
    description: Create a new project
    execution: api
    method: POST
    endpoint: /projects
    inputSchema:
      type: object
      properties:
        name:
          type: string
          description: Project name
        description:
          type: string
          description: Project description
        owner_id:
          type: string
          description: Owner user ID
      required:
        - name
        - owner_id
```

## Execution Types

### API Execution (Default)

Execute tools via HTTP API calls.

```yaml
- name: my_tool
  execution: api
  method: POST
  endpoint: /my/endpoint
```

### Function Execution

Execute tools via Python functions (future enhancement).

```yaml
- name: my_tool
  execution: function
  function: my_module.my_function
```

## Available Tools

### Default Tool

- `execute_domain_action(action, params)` - Generic domain action executor

### Configured Tools

All tools defined in `domain_tools.yaml` are automatically available.

## Examples

### Finance App Tools

```yaml
tools:
  - name: calculate_interest_schedule
    description: Calculate interest schedule
    execution: api
    method: POST
    endpoint: /finance/calculate-interest
    # ...

  - name: simulate_portfolio
    description: Simulate portfolio performance
    execution: api
    method: POST
    endpoint: /finance/simulate-portfolio
    # ...
```

### Project Management Tools

```yaml
tools:
  - name: create_project
    description: Create a new project
    execution: api
    method: POST
    endpoint: /projects
    # ...

  - name: add_task
    description: Add a task to a project
    execution: api
    method: POST
    endpoint: /projects/{project_id}/tasks
    # ...

  - name: reassign_task
    description: Reassign a task
    execution: api
    method: PUT
    endpoint: /tasks/{task_id}/assign
    # ...
```

## Security

- **Authentication**: All API calls use configured authentication
- **Input Validation**: Tool schemas validate all inputs
- **Error Handling**: Errors don't expose sensitive information
- **Rate Limiting**: Be aware of API rate limits

## Best Practices

1. **Domain-Specific Names**: Use business domain terminology, not technical terms
2. **Clear Descriptions**: Provide clear descriptions for each tool
3. **Type Safety**: Define proper input schemas with types and required fields
4. **Error Handling**: Handle errors gracefully with clear messages
5. **Documentation**: Document each tool's purpose and usage

## Troubleshooting

**Tool not found:**
- Verify tool name in configuration matches the call
- Check `DOMAIN_TOOLS_CONFIG` path is correct
- Ensure YAML syntax is valid

**API errors:**
- Verify `API_BASE_URL` is correct
- Check authentication credentials
- Ensure endpoint paths are correct

**Configuration errors:**
- Validate YAML syntax
- Check required fields are present
- Verify input schema format

