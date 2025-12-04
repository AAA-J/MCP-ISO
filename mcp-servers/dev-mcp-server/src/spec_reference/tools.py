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

async def handle_spec_reference(name: str, arguments: dict) -> list[TextContent]:
    """Handle spec reference tool calls."""
    if name == "spec_get_mcp_spec":
        topic = arguments.get("topic")
        detail = arguments.get("detail", "overview")
        # Return specification content
        return [TextContent(
            type="text",
            text=f"# MCP Specification: {topic}\n\nSpecification details for {topic}..."
        )]
    elif name == "spec_get_best_practices":
        pattern = arguments.get("pattern")
        # Return best practices
        return [TextContent(
            type="text",
            text=f"# Best Practices: {pattern}\n\nBest practices for {pattern}..."
        )]
    else:
        raise ValueError(f"Unknown spec reference tool: {name}")

