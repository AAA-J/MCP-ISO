"""Domain-specific business logic tools."""

import json
import yaml
from typing import List, Dict, Optional
from mcp.types import Tool, TextContent
import httpx


def load_domain_tools(config_file: str) -> List[Tool]:
    """Load domain tools from YAML configuration file."""
    try:
        with open(config_file, 'r') as f:
            config = yaml.safe_load(f) or {}
    except Exception as e:
        return []
    
    tools = []
    
    if "tools" not in config:
        return tools
    
    for tool_def in config["tools"]:
        tools.append(Tool(
            name=tool_def.get("name"),
            description=tool_def.get("description", ""),
            inputSchema=tool_def.get("inputSchema", {
                "type": "object",
                "properties": {},
                "required": []
            })
        ))
    
    return tools


async def handle_domain_tool(
    name: str,
    arguments: dict,
    tool_config: Dict,
    api_base_url: Optional[str] = None,
    auth_config: Optional[Dict] = None
) -> List[TextContent]:
    """Handle domain tool calls."""
    
    # Find tool configuration
    tool_def = None
    for tool in tool_config.get("tools", []):
        if tool.get("name") == name:
            tool_def = tool
            break
    
    if not tool_def:
        return [TextContent(
            type="text",
            text=f"Unknown domain tool: {name}"
        )]
    
    # Determine execution method
    execution_type = tool_def.get("execution", "api").lower()
    
    if execution_type == "api":
        # Execute via API call
        return await execute_api_tool(tool_def, arguments, api_base_url, auth_config)
    elif execution_type == "function":
        # Execute via Python function (if defined)
        return await execute_function_tool(tool_def, arguments)
    else:
        return [TextContent(
            type="text",
            text=f"Unsupported execution type: {execution_type}"
        )]


async def execute_api_tool(
    tool_def: Dict,
    arguments: dict,
    api_base_url: Optional[str],
    auth_config: Optional[Dict]
) -> List[TextContent]:
    """Execute domain tool via API call."""
    
    if not api_base_url:
        return [TextContent(
            type="text",
            text="Error: API base URL not configured"
        )]
    
    # Get endpoint from tool config
    endpoint = tool_def.get("endpoint", f"/domain/{tool_def.get('name')}")
    method = tool_def.get("method", "POST").upper()
    
    # Build headers
    headers = {
        "Content-Type": "application/json",
        "Accept": "application/json"
    }
    
    # Add authentication
    if auth_config:
        if auth_config.get("type") == "bearer":
            headers["Authorization"] = f"Bearer {auth_config.get('token')}"
        elif auth_config.get("type") == "api_key":
            key_name = auth_config.get("key_name", "X-API-Key")
            headers[key_name] = auth_config.get("api_key")
    
    url = f"{api_base_url.rstrip('/')}/{endpoint.lstrip('/')}"
    
    try:
        async with httpx.AsyncClient() as client:
            if method == "GET":
                response = await client.get(url, params=arguments, headers=headers, timeout=30.0)
            elif method == "POST":
                response = await client.post(url, json=arguments, headers=headers, timeout=30.0)
            elif method == "PUT":
                response = await client.put(url, json=arguments, headers=headers, timeout=30.0)
            else:
                return [TextContent(
                    type="text",
                    text=f"Unsupported HTTP method: {method}"
                )]
            
            response.raise_for_status()
            data = response.json()
            
            return [TextContent(
                type="text",
                text=json.dumps(data, indent=2)
            )]
    except httpx.HTTPStatusError as e:
        return [TextContent(
            type="text",
            text=f"API error: {e.response.status_code} - {e.response.text}"
        )]
    except Exception as e:
        return [TextContent(
            type="text",
            text=f"Error executing domain tool: {str(e)}"
        )]


async def execute_function_tool(
    tool_def: Dict,
    arguments: dict
) -> List[TextContent]:
    """Execute domain tool via Python function."""
    
    # This is a placeholder for function-based execution
    # In practice, you'd import and call actual domain functions
    
    function_name = tool_def.get("function")
    if not function_name:
        return [TextContent(
            type="text",
            text="Error: Function name not specified in tool configuration"
        )]
    
    # For now, return a message indicating function execution
    # In a real implementation, you'd dynamically import and call the function
    return [TextContent(
        type="text",
        text=f"Function-based execution not yet implemented. Tool: {tool_def.get('name')}, Function: {function_name}, Arguments: {json.dumps(arguments, indent=2)}"
    )]


# Default/example domain tools (can be overridden by config)
default_domain_tools = [
    Tool(
        name="execute_domain_action",
        description="Execute a generic domain action",
        inputSchema={
            "type": "object",
            "properties": {
                "action": {
                    "type": "string",
                    "description": "Action name"
                },
                "params": {
                    "type": "object",
                    "description": "Action parameters"
                }
            },
            "required": ["action"]
        }
    ),
]

