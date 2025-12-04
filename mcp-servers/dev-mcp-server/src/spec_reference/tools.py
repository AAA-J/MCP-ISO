"""Specification reference tools for MCP development."""

from mcp.types import Tool, TextContent

spec_reference_tools = [
    Tool(
        name="spec_get_mcp_spec",
        description="Get MCP specification details for a specific topic",
        inputSchema={
            "type": "object",
            "properties": {
                "topic": {
                    "type": "string",
                    "description": "Specification topic (tools, resources, prompts, transport)",
                    "enum": ["tools", "resources", "prompts", "transport", "jsonrpc"]
                },
                "detail": {
                    "type": "string",
                    "description": "Specific detail level (overview, reference, examples)"
                }
            },
            "required": ["topic"]
        }
    ),
    Tool(
        name="spec_get_best_practices",
        description="Get best practices for MCP server development patterns",
        inputSchema={
            "type": "object",
            "properties": {
                "pattern": {
                    "type": "string",
                    "description": "Pattern name (error-handling, authentication, rate-limiting)",
                    "enum": ["error-handling", "authentication", "rate-limiting", "logging", "testing"]
                }
            },
            "required": ["pattern"]
        }
    ),
]

# MCP Specification Content
MCP_SPEC_CONTENT = {
    "tools": {
        "overview": """# MCP Tools Specification

## Overview
Tools are functions that an MCP server exposes to AI models. They allow the AI to perform actions and interact with external systems.

## Key Concepts

### Tool Definition
- **Name**: Unique identifier for the tool
- **Description**: Human-readable description of what the tool does
- **Input Schema**: JSON Schema defining the tool's parameters
- **Handler**: Function that executes the tool logic

### Tool Schema Structure
```json
{
  "name": "tool_name",
  "description": "Tool description",
  "inputSchema": {
    "type": "object",
    "properties": {
      "param1": {"type": "string", "description": "Parameter description"}
    },
    "required": ["param1"]
  }
}
```

### Tool Execution
- Tools are called via JSON-RPC `tools/call` method
- Input parameters are validated against the schema
- Tool returns results as `TextContent` or `ImageContent`
- Errors are returned as JSON-RPC errors

## Best Practices
- Use descriptive names (e.g., `get_user_profile` not `get_user`)
- Provide clear descriptions for AI understanding
- Validate all inputs before processing
- Return structured, parseable results
- Handle errors gracefully with informative messages""",
        "reference": """# MCP Tools Reference

## Tool Registration
```python
from mcp.types import Tool

tool = Tool(
    name="my_tool",
    description="Does something useful",
    inputSchema={
        "type": "object",
        "properties": {
            "input": {"type": "string"}
        },
        "required": ["input"]
    }
)
```

## Tool Handler
```python
@server.call_tool()
async def call_tool(name: str, arguments: dict) -> list[TextContent]:
    if name == "my_tool":
        input_value = arguments.get("input")
        result = process_input(input_value)
        return [TextContent(type="text", text=result)]
```

## JSON-RPC Request
```json
{
  "jsonrpc": "2.0",
  "id": 1,
  "method": "tools/call",
  "params": {
    "name": "my_tool",
    "arguments": {
      "input": "value"
    }
  }
}
```

## JSON-RPC Response
```json
{
  "jsonrpc": "2.0",
  "id": 1,
  "result": {
    "content": [
      {
        "type": "text",
        "text": "Result content"
      }
    ]
  }
}
```""",
        "examples": """# MCP Tools Examples

## Basic Tool (Python)
```python
from mcp.server import Server
from mcp.types import Tool, TextContent

server = Server("my-server")

@server.list_tools()
async def list_tools():
    return [
        Tool(
            name="greet",
            description="Greets a person by name",
            inputSchema={
                "type": "object",
                "properties": {
                    "name": {"type": "string", "description": "Person's name"}
                },
                "required": ["name"]
            }
        )
    ]

@server.call_tool()
async def call_tool(name: str, arguments: dict):
    if name == "greet":
        name = arguments.get("name")
        return [TextContent(type="text", text=f"Hello, {name}!")]
```

## Tool with Validation
```python
@server.call_tool()
async def call_tool(name: str, arguments: dict):
    if name == "calculate":
        a = arguments.get("a")
        b = arguments.get("b")
        
        if not isinstance(a, (int, float)) or not isinstance(b, (int, float)):
            raise ValueError("a and b must be numbers")
        
        result = a + b
        return [TextContent(type="text", text=str(result))]
```"""
    },
    "resources": {
        "overview": """# MCP Resources Specification

## Overview
Resources are data sources that MCP servers expose to AI models. They provide read-only access to structured data.

## Key Concepts

### Resource Definition
- **URI**: Unique identifier for the resource (e.g., `mcp://server/resource/123`)
- **Name**: Human-readable name
- **Description**: What the resource contains
- **MIME Type**: Content type (e.g., `text/markdown`, `application/json`)

### Resource URI Format
- Scheme: `mcp://`
- Server identifier
- Resource path
- Example: `mcp://filesystem/file/path/to/file.txt`

### Resource Reading
- Resources are read via JSON-RPC `resources/read` method
- Returns content as text or binary data
- Supports content negotiation via MIME types

## Best Practices
- Use hierarchical URI structures
- Provide clear descriptions
- Support appropriate MIME types
- Cache resources when appropriate
- Handle missing resources gracefully""",
        "reference": """# MCP Resources Reference

## Resource Registration
```python
from mcp.types import Resource

resource = Resource(
    uri="mcp://my-server/data/123",
    name="Data Resource",
    description="Contains data",
    mimeType="application/json"
)
```

## Resource Handler
```python
@server.list_resources()
async def list_resources():
    return [
        Resource(
            uri="mcp://my-server/data/123",
            name="Data Resource",
            description="Contains data",
            mimeType="application/json"
        )
    ]

@server.read_resource()
async def read_resource(uri: str) -> str:
    if uri.startswith("mcp://my-server/data/"):
        resource_id = uri.split("/")[-1]
        data = fetch_data(resource_id)
        return json.dumps(data)
```

## JSON-RPC Request
```json
{
  "jsonrpc": "2.0",
  "id": 1,
  "method": "resources/read",
  "params": {
    "uri": "mcp://my-server/data/123"
  }
}
```""",
        "examples": """# MCP Resources Examples

## File System Resource
```python
@server.read_resource()
async def read_resource(uri: str) -> str:
    if uri.startswith("mcp://filesystem/"):
        file_path = uri.replace("mcp://filesystem/", "")
        with open(file_path, "r") as f:
            return f.read()
```"""
    },
    "prompts": {
        "overview": """# MCP Prompts Specification

## Overview
Prompts are reusable template strings that help AI models interact with MCP servers more effectively.

## Key Concepts

### Prompt Definition
- **Name**: Unique identifier
- **Description**: What the prompt is for
- **Arguments**: Template variables
- **Template**: The prompt template string

### Prompt Template Syntax
- Use `{{variable}}` for template variables
- Supports conditional sections
- Can include examples and instructions

## Best Practices
- Make prompts clear and specific
- Include examples when helpful
- Use descriptive variable names
- Keep prompts focused on single tasks""",
        "reference": """# MCP Prompts Reference

## Prompt Registration
```python
from mcp.types import Prompt

prompt = Prompt(
    name="analyze_code",
    description="Analyzes code for issues",
    arguments=[
        {"name": "code", "description": "Code to analyze", "required": True}
    ]
)
```

## Prompt Handler
```python
@server.list_prompts()
async def list_prompts():
    return [
        Prompt(
            name="analyze_code",
            description="Analyzes code",
            arguments=[
                {"name": "code", "description": "Code to analyze", "required": True}
            ]
        )
    ]

@server.get_prompt()
async def get_prompt(name: str, arguments: dict) -> str:
    if name == "analyze_code":
        code = arguments.get("code")
        return f"Analyze this code for potential issues:\n\n{code}"
```"""
    },
    "transport": {
        "overview": """# MCP Transport Specification

## Overview
MCP servers communicate via JSON-RPC 2.0 over different transport mechanisms.

## Transport Types

### stdio (Standard Input/Output)
- Default for local development
- Messages sent via stdin/stdout
- Simple and reliable
- Best for local servers

### HTTP/SSE (Server-Sent Events)
- For remote servers
- HTTP POST for requests
- SSE for streaming responses
- Better for production deployments

## Best Practices
- Use stdio for local development
- Use HTTP/SSE for remote access
- Handle connection errors gracefully
- Implement proper authentication""",
        "reference": """# MCP Transport Reference

## stdio Transport (Python)
```python
from mcp.server.stdio import stdio_server

async def main():
    async with stdio_server() as (read_stream, write_stream):
        await server.run(read_stream, write_stream, server.create_initialization_options())
```

## HTTP/SSE Transport (Python)
```python
from mcp.server.sse import SSEServerTransport
from fastapi import FastAPI

app = FastAPI()
transport = SSEServerTransport("/mcp", app)
await server.connect(transport)
```"""
    },
    "jsonrpc": {
        "overview": """# JSON-RPC 2.0 Specification

## Overview
MCP uses JSON-RPC 2.0 for all communication between clients and servers.

## Key Concepts

### Request Format
```json
{
  "jsonrpc": "2.0",
  "id": 1,
  "method": "method_name",
  "params": {}
}
```

### Response Format
```json
{
  "jsonrpc": "2.0",
  "id": 1,
  "result": {}
}
```

### Error Format
```json
{
  "jsonrpc": "2.0",
  "id": 1,
  "error": {
    "code": -32600,
    "message": "Invalid Request"
  }
}
```

## Error Codes
- `-32700`: Parse error
- `-32600`: Invalid Request
- `-32601`: Method not found
- `-32602`: Invalid params
- `-32603`: Internal error
- `-32000` to `-32099`: Server error""",
        "reference": """# JSON-RPC 2.0 Reference

## MCP Methods
- `initialize`: Initialize connection
- `tools/list`: List available tools
- `tools/call`: Call a tool
- `resources/list`: List available resources
- `resources/read`: Read a resource
- `prompts/list`: List available prompts
- `prompts/get`: Get a prompt template

## Example Request/Response
```json
// Request
{
  "jsonrpc": "2.0",
  "id": 1,
  "method": "tools/list",
  "params": {}
}

// Response
{
  "jsonrpc": "2.0",
  "id": 1,
  "result": {
    "tools": [
      {
        "name": "my_tool",
        "description": "Does something"
      }
    ]
  }
}
```"""
    }
}

BEST_PRACTICES = {
    "error-handling": """# Error Handling Best Practices

## Principles
1. **Always validate inputs** before processing
2. **Return informative error messages** that help debugging
3. **Use appropriate JSON-RPC error codes**
4. **Log errors** for debugging but don't expose sensitive info

## Implementation

### Input Validation
```python
@server.call_tool()
async def call_tool(name: str, arguments: dict):
    if name == "my_tool":
        required_param = arguments.get("required_param")
        if not required_param:
            raise ValueError("required_param is required")
        
        if not isinstance(required_param, str):
            raise ValueError("required_param must be a string")
```

### Error Responses
```python
try:
    result = process_data(arguments)
    return [TextContent(type="text", text=result)]
except ValueError as e:
    raise ValueError(f"Invalid input: {str(e)}")
except Exception as e:
    # Log full error
    logger.error(f"Unexpected error: {e}", exc_info=True)
    # Return user-friendly message
    raise ValueError("An error occurred processing your request")
```

### JSON-RPC Error Codes
- Use `-32602` for invalid parameters
- Use `-32603` for internal errors
- Use custom codes (-32000 to -32099) for domain-specific errors""",
    "authentication": """# Authentication Best Practices

## Principles
1. **Never expose credentials** in tool responses or logs
2. **Use environment variables** for sensitive data
3. **Validate tokens** before making API calls
4. **Implement token refresh** for long-lived sessions

## Implementation

### Environment Variables
```python
import os
from dotenv import load_dotenv

load_dotenv()
API_KEY = os.getenv("API_KEY")
if not API_KEY:
    raise ValueError("API_KEY environment variable not set")
```

### Token Validation
```python
def validate_token(token: str) -> bool:
    if not token or len(token) < 10:
        return False
    # Add your validation logic
    return True

@server.call_tool()
async def call_tool(name: str, arguments: dict):
    token = os.getenv("API_TOKEN")
    if not validate_token(token):
        raise ValueError("Invalid or missing API token")
```

### Secure Credential Storage
- Use `.env` files (never commit them)
- Use secret management services in production
- Rotate credentials regularly
- Use least-privilege access""",
    "rate-limiting": """# Rate Limiting Best Practices

## Principles
1. **Respect API rate limits** from external services
2. **Implement client-side rate limiting** to prevent abuse
3. **Return clear error messages** when limits are exceeded
4. **Use exponential backoff** for retries

## Implementation

### Simple Rate Limiter
```python
from collections import defaultdict
from datetime import datetime, timedelta

class RateLimiter:
    def __init__(self, max_calls: int, window_seconds: int):
        self.max_calls = max_calls
        self.window_seconds = window_seconds
        self.calls = defaultdict(list)
    
    def check(self, key: str) -> bool:
        now = datetime.now()
        window_start = now - timedelta(seconds=self.window_seconds)
        
        # Remove old calls
        self.calls[key] = [t for t in self.calls[key] if t > window_start]
        
        if len(self.calls[key]) >= self.max_calls:
            return False
        
        self.calls[key].append(now)
        return True

limiter = RateLimiter(max_calls=10, window_seconds=60)

@server.call_tool()
async def call_tool(name: str, arguments: dict):
    if not limiter.check("default"):
        raise ValueError("Rate limit exceeded. Please try again later.")
```

### Exponential Backoff
```python
import asyncio

async def call_with_retry(func, max_retries=3):
    for attempt in range(max_retries):
        try:
            return await func()
        except Exception as e:
            if attempt == max_retries - 1:
                raise
            wait_time = 2 ** attempt
            await asyncio.sleep(wait_time)
```""",
    "logging": """# Logging Best Practices

## Principles
1. **Log important events** (tool calls, errors, auth failures)
2. **Use appropriate log levels** (DEBUG, INFO, WARNING, ERROR)
3. **Don't log sensitive data** (passwords, tokens, PII)
4. **Structured logging** for better analysis

## Implementation

### Basic Logging
```python
import logging

logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s'
)
logger = logging.getLogger(__name__)

@server.call_tool()
async def call_tool(name: str, arguments: dict):
    logger.info(f"Tool called: {name}")
    try:
        result = process_tool(name, arguments)
        logger.info(f"Tool {name} completed successfully")
        return result
    except Exception as e:
        logger.error(f"Tool {name} failed: {e}", exc_info=True)
        raise
```

### Structured Logging
```python
import json
import logging

class StructuredLogger:
    def log_tool_call(self, name: str, arguments: dict, success: bool):
        log_data = {
            "event": "tool_call",
            "tool": name,
            "success": success,
            # Don't log sensitive arguments
            "arguments": {k: v for k, v in arguments.items() if k != "password"}
        }
        logger.info(json.dumps(log_data))
```""",
    "testing": """# Testing Best Practices

## Principles
1. **Test tool handlers** with various inputs
2. **Test error cases** (invalid input, missing params)
3. **Mock external dependencies** (APIs, databases)
4. **Test resource reading** and edge cases

## Implementation

### Unit Tests
```python
import pytest
from mcp.types import TextContent

async def test_tool_handler():
    handler = handle_my_tool
    result = await handler("my_tool", {"param": "value"})
    assert isinstance(result, list)
    assert len(result) > 0
    assert isinstance(result[0], TextContent)

async def test_tool_validation():
    handler = handle_my_tool
    with pytest.raises(ValueError):
        await handler("my_tool", {})  # Missing required param
```

### Integration Tests
```python
async def test_server_initialization():
    server = Server("test-server")
    # Test server starts correctly
    # Test tools are registered
    # Test resources are available
```

### Mock External APIs
```python
from unittest.mock import patch, AsyncMock

@patch('my_module.external_api_call')
async def test_tool_with_mock(mock_api):
    mock_api.return_value = {"result": "success"}
    result = await handle_tool("tool_name", {})
    assert "success" in str(result)
```"""
}

async def handle_spec_reference(name: str, arguments: dict) -> list[TextContent]:
    """Handle spec reference tool calls."""
    if name == "spec_get_mcp_spec":
        topic = arguments.get("topic")
        detail = arguments.get("detail", "overview")
        
        if topic not in MCP_SPEC_CONTENT:
            raise ValueError(f"Unknown topic: {topic}")
        
        content = MCP_SPEC_CONTENT[topic].get(detail, MCP_SPEC_CONTENT[topic]["overview"])
        
        return [TextContent(
            type="text",
            text=content
        )]
    elif name == "spec_get_best_practices":
        pattern = arguments.get("pattern")
        
        if pattern not in BEST_PRACTICES:
            raise ValueError(f"Unknown pattern: {pattern}")
        
        return [TextContent(
            type="text",
            text=BEST_PRACTICES[pattern]
        )]
    else:
        raise ValueError(f"Unknown spec reference tool: {name}")

