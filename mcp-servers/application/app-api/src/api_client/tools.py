"""API client tools for app-api server."""

import json
import yaml
from typing import List, Dict, Optional
from mcp.types import Tool, TextContent
import httpx


# Default tool definitions (can be extended via config)
default_tools = [
    Tool(
        name="get_user",
        description="Get user information by ID",
        inputSchema={
            "type": "object",
            "properties": {
                "id": {
                    "type": "string",
                    "description": "User ID"
                }
            },
            "required": ["id"]
        }
    ),
    Tool(
        name="search_orders",
        description="Search orders with filters",
        inputSchema={
            "type": "object",
            "properties": {
                "criteria": {
                    "type": "object",
                    "description": "Search criteria (filters, pagination, etc.)"
                }
            }
        }
    ),
    Tool(
        name="trigger_workflow",
        description="Trigger a backend workflow",
        inputSchema={
            "type": "object",
            "properties": {
                "name": {
                    "type": "string",
                    "description": "Workflow name"
                },
                "params": {
                    "type": "object",
                    "description": "Workflow parameters"
                }
            },
            "required": ["name"]
        }
    ),
    Tool(
        name="simulate_pricing",
        description="Run pricing calculations",
        inputSchema={
            "type": "object",
            "properties": {
                "input": {
                    "type": "object",
                    "description": "Pricing input parameters"
                }
            },
            "required": ["input"]
        }
    ),
    Tool(
        name="call_api",
        description="Generic API call to any endpoint",
        inputSchema={
            "type": "object",
            "properties": {
                "endpoint": {
                    "type": "string",
                    "description": "API endpoint path (relative to base URL)"
                },
                "method": {
                    "type": "string",
                    "enum": ["GET", "POST", "PUT", "PATCH", "DELETE"],
                    "description": "HTTP method",
                    "default": "GET"
                },
                "params": {
                    "type": "object",
                    "description": "Request parameters (query params for GET, body for POST/PUT/PATCH)"
                },
                "headers": {
                    "type": "object",
                    "description": "Additional HTTP headers"
                }
            },
            "required": ["endpoint"]
        }
    ),
]


def load_tool_config(config_file: Optional[str] = None) -> Dict:
    """Load tool configuration from YAML/JSON file."""
    if not config_file:
        return {}
    
    try:
        with open(config_file, 'r') as f:
            if config_file.endswith('.yaml') or config_file.endswith('.yml'):
                return yaml.safe_load(f) or {}
            elif config_file.endswith('.json'):
                return json.load(f)
            else:
                return {}
    except Exception:
        return {}


def build_tools_from_config(config: Dict, base_url: str) -> List[Tool]:
    """Build Tool definitions from configuration."""
    tools = []
    
    if "tools" not in config:
        return tools
    
    for tool_def in config["tools"]:
        tools.append(Tool(
            name=tool_def.get("name"),
            description=tool_def.get("description", ""),
            inputSchema=tool_def.get("inputSchema", {})
        ))
    
    return tools


async def handle_api_tool(
    name: str,
    arguments: dict,
    base_url: str,
    auth_config: Dict,
    api_type: str = "rest"
) -> List[TextContent]:
    """Handle API tool calls."""
    
    if api_type == "graphql":
        return await handle_graphql_tool(name, arguments, base_url, auth_config)
    else:
        return await handle_rest_tool(name, arguments, base_url, auth_config)


async def handle_rest_tool(
    name: str,
    arguments: dict,
    base_url: str,
    auth_config: Dict
) -> List[TextContent]:
    """Handle REST API tool calls."""
    
    # Build headers
    headers = {
        "Content-Type": "application/json",
        "Accept": "application/json"
    }
    
    # Add authentication
    if auth_config.get("type") == "bearer":
        headers["Authorization"] = f"Bearer {auth_config.get('token')}"
    elif auth_config.get("type") == "api_key":
        key_name = auth_config.get("key_name", "X-API-Key")
        headers[key_name] = auth_config.get("api_key")
    elif auth_config.get("type") == "basic":
        import base64
        username = auth_config.get("username", "")
        password = auth_config.get("password", "")
        credentials = base64.b64encode(f"{username}:{password}".encode()).decode()
        headers["Authorization"] = f"Basic {credentials}"
    
    # Add custom headers
    if "headers" in arguments:
        headers.update(arguments["headers"])
    
    # Route to specific tool handlers or use generic call_api
    if name == "call_api":
        endpoint = arguments.get("endpoint", "")
        method = arguments.get("method", "GET").upper()
        params = arguments.get("params", {})
        
        url = f"{base_url.rstrip('/')}/{endpoint.lstrip('/')}"
        
        async with httpx.AsyncClient() as client:
            if method == "GET":
                response = await client.get(url, params=params, headers=headers, timeout=30.0)
            elif method == "POST":
                response = await client.post(url, json=params, headers=headers, timeout=30.0)
            elif method == "PUT":
                response = await client.put(url, json=params, headers=headers, timeout=30.0)
            elif method == "PATCH":
                response = await client.patch(url, json=params, headers=headers, timeout=30.0)
            elif method == "DELETE":
                response = await client.delete(url, headers=headers, timeout=30.0)
            else:
                return [TextContent(
                    type="text",
                    text=f"Unsupported HTTP method: {method}"
                )]
            
            return format_api_response(response)
    
    # Handle predefined tools (map to endpoints)
    tool_endpoints = {
        "get_user": ("GET", "/users/{id}"),
        "search_orders": ("POST", "/orders/search"),
        "trigger_workflow": ("POST", "/workflows/{name}/trigger"),
        "simulate_pricing": ("POST", "/pricing/simulate"),
    }
    
    if name in tool_endpoints:
        method, endpoint_template = tool_endpoints[name]
        
        # Replace path parameters
        endpoint = endpoint_template
        if name == "get_user":
            endpoint = endpoint.replace("{id}", str(arguments.get("id", "")))
        elif name == "trigger_workflow":
            endpoint = endpoint.replace("{name}", arguments.get("name", ""))
        
        # Build request body/params
        if method == "GET":
            params = arguments
        else:
            params = {k: v for k, v in arguments.items() if k not in ["id", "name"]}
        
        url = f"{base_url.rstrip('/')}{endpoint}"
        
        async with httpx.AsyncClient() as client:
            if method == "GET":
                response = await client.get(url, params=params, headers=headers, timeout=30.0)
            else:
                response = await client.post(url, json=params, headers=headers, timeout=30.0)
            
            return format_api_response(response)
    
    return [TextContent(
        type="text",
        text=f"Unknown API tool: {name}"
    )]


async def handle_graphql_tool(
    name: str,
    arguments: dict,
    base_url: str,
    auth_config: Dict
) -> List[TextContent]:
    """Handle GraphQL API tool calls."""
    try:
        from gql import Client, gql
        from gql.transport.aiohttp import AIOHTTPTransport
    except ImportError:
        return [TextContent(
            type="text",
            text="Error: GraphQL support requires 'gql' package. Install with: pip install gql[aiohttp]"
        )]
    
    # Build headers
    headers = {}
    if auth_config.get("type") == "bearer":
        headers["Authorization"] = f"Bearer {auth_config.get('token')}"
    elif auth_config.get("type") == "api_key":
        key_name = auth_config.get("key_name", "X-API-Key")
        headers[key_name] = auth_config.get("api_key")
    
    # For GraphQL, we'll use a generic query approach
    # In a real implementation, you'd have predefined queries or use introspection
    transport = AIOHTTPTransport(url=base_url, headers=headers)
    client = Client(transport=transport, fetch_schema_from_transport=True)
    
    # Build GraphQL query from tool name and arguments
    # This is a simplified approach - in practice, you'd have query templates
    query_str = build_graphql_query(name, arguments)
    
    try:
        query = gql(query_str)
        result = await client.execute_async(query)
        return [TextContent(
            type="text",
            text=json.dumps(result, indent=2)
        )]
    except Exception as e:
        return [TextContent(
            type="text",
            text=f"GraphQL query error: {str(e)}"
        )]


def build_graphql_query(tool_name: str, arguments: dict) -> str:
    """Build a GraphQL query from tool name and arguments."""
    # This is a simplified implementation
    # In practice, you'd have query templates or use GraphQL introspection
    
    if tool_name == "get_user":
        user_id = arguments.get("id", "")
        return f"""
        query {{
            user(id: "{user_id}") {{
                id
                name
                email
            }}
        }}
        """
    else:
        # Generic query
        return f"""
        query {{
            {tool_name}({format_graphql_args(arguments)}) {{
                id
            }}
        }}
        """


def format_graphql_args(arguments: dict) -> str:
    """Format arguments as GraphQL query arguments."""
    args = []
    for key, value in arguments.items():
        if isinstance(value, str):
            args.append(f'{key}: "{value}"')
        elif isinstance(value, (int, float, bool)):
            args.append(f"{key}: {value}")
        elif isinstance(value, dict):
            args.append(f"{key}: {json.dumps(value)}")
    
    return ", ".join(args)


def format_api_response(response: httpx.Response) -> List[TextContent]:
    """Format API response as TextContent."""
    try:
        # Try to parse as JSON
        data = response.json()
        result = {
            "status_code": response.status_code,
            "status_text": response.reason_phrase,
            "data": data
        }
        return [TextContent(
            type="text",
            text=json.dumps(result, indent=2)
        )]
    except Exception:
        # Fallback to text
        result = {
            "status_code": response.status_code,
            "status_text": response.reason_phrase,
            "data": response.text
        }
        return [TextContent(
            type="text",
            text=json.dumps(result, indent=2)
        )]

