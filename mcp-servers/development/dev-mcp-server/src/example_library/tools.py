"""Example library tools for MCP servers."""

from mcp.types import Tool, TextContent
import json

example_library_tools = [
    Tool(
        name="get_example_server",
        description="Get example MCP server code",
        inputSchema={
            "type": "object",
            "properties": {
                "exampleType": {
                    "type": "string",
                    "enum": ["basic", "with-auth", "multi-transport", "error-handling"],
                    "description": "Type of example server"
                },
                "language": {
                    "type": "string",
                    "enum": ["python", "typescript"]
                }
            },
            "required": ["exampleType", "language"]
        }
    ),
    Tool(
        name="get_pattern",
        description="Get common MCP development patterns",
        inputSchema={
            "type": "object",
            "properties": {
                "patternName": {
                    "type": "string",
                    "enum": ["authentication", "error-handling", "rate-limiting", "logging"],
                    "description": "Pattern name"
                },
                "language": {
                    "type": "string",
                    "enum": ["python", "typescript"]
                }
            },
            "required": ["patternName", "language"]
        }
    ),
]

EXAMPLES = {
    "basic": {
        "python": '''#!/usr/bin/env python3
"""Basic MCP Server Example"""
import asyncio
from mcp.server import Server
from mcp.server.stdio import stdio_server
from mcp.types import Tool, TextContent

server = Server("basic-server")

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
    raise ValueError(f"Unknown tool: {name}")

async def main():
    async with stdio_server() as (read_stream, write_stream):
        await server.run(read_stream, write_stream, server.create_initialization_options())

if __name__ == "__main__":
    asyncio.run(main())
''',
        "typescript": '''/**
 * Basic MCP Server Example
 */
import { Server } from "@modelcontextprotocol/sdk/server/index.js";
import { StdioServerTransport } from "@modelcontextprotocol/sdk/server/stdio.js";
import {
  CallToolRequestSchema,
  ListToolsRequestSchema,
} from "@modelcontextprotocol/sdk/types.js";

const server = new Server(
  {
    name: "basic-server",
    version: "0.1.0",
  },
  {
    capabilities: {
      tools: {},
    },
  }
);

server.setRequestHandler(ListToolsRequestSchema, async () => ({
  tools: [
    {
      name: "greet",
      description: "Greets a person by name",
      inputSchema: {
        type: "object",
        properties: {
          name: {
            type: "string",
            description: "Person's name",
          },
        },
        required: ["name"],
      },
    },
  ],
}));

server.setRequestHandler(CallToolRequestSchema, async (request) => {
  if (request.params.name === "greet") {
    const name = request.params.arguments?.name;
    return {
      content: [
        {
          type: "text",
          text: `Hello, ${name}!`,
        },
      ],
    };
  }
  throw new Error(`Unknown tool: ${request.params.name}`);
});

async function main() {
  const transport = new StdioServerTransport();
  await server.connect(transport);
  console.error("Basic server running on stdio");
}

main().catch(console.error);
'''
    },
    "with-auth": {
        "python": '''#!/usr/bin/env python3
"""MCP Server with Authentication"""
import asyncio
import os
from mcp.server import Server
from mcp.server.stdio import stdio_server
from mcp.types import Tool, TextContent

server = Server("auth-server")

# Get API key from environment
API_KEY = os.getenv("API_KEY")
if not API_KEY:
    raise ValueError("API_KEY environment variable not set")

def validate_auth():
    """Validate authentication."""
    if not API_KEY:
        raise ValueError("Authentication required")
    return True

@server.list_tools()
async def list_tools():
    return [
        Tool(
            name="authenticated_action",
            description="Performs an authenticated action",
            inputSchema={
                "type": "object",
                "properties": {
                    "action": {"type": "string", "description": "Action to perform"}
                },
                "required": ["action"]
            }
        )
    ]

@server.call_tool()
async def call_tool(name: str, arguments: dict):
    # Validate authentication
    validate_auth()
    
    if name == "authenticated_action":
        action = arguments.get("action")
        return [TextContent(type="text", text=f"Performed: {action}")]
    raise ValueError(f"Unknown tool: {name}")

async def main():
    async with stdio_server() as (read_stream, write_stream):
        await server.run(read_stream, write_stream, server.create_initialization_options())

if __name__ == "__main__":
    asyncio.run(main())
''',
        "typescript": '''/**
 * MCP Server with Authentication
 */
import { Server } from "@modelcontextprotocol/sdk/server/index.js";
import { StdioServerTransport } from "@modelcontextprotocol/sdk/server/stdio.js";

const API_KEY = process.env.API_KEY;
if (!API_KEY) {
  throw new Error("API_KEY environment variable not set");
}

function validateAuth(): void {
  if (!API_KEY) {
    throw new Error("Authentication required");
  }
}

const server = new Server(
  {
    name: "auth-server",
    version: "0.1.0",
  },
  {
    capabilities: {
      tools: {},
    },
  }
);

server.setRequestHandler(ListToolsRequestSchema, async () => ({
  tools: [
    {
      name: "authenticated_action",
      description: "Performs an authenticated action",
      inputSchema: {
        type: "object",
        properties: {
          action: {
            type: "string",
            description: "Action to perform",
          },
        },
        required: ["action"],
      },
    },
  ],
}));

server.setRequestHandler(CallToolRequestSchema, async (request) => {
  validateAuth();
  
  if (request.params.name === "authenticated_action") {
    const action = request.params.arguments?.action;
    return {
      content: [
        {
          type: "text",
          text: `Performed: ${action}`,
        },
      ],
    };
  }
  throw new Error(`Unknown tool: ${request.params.name}`);
});

async function main() {
  const transport = new StdioServerTransport();
  await server.connect(transport);
}

main().catch(console.error);
'''
    },
    "error-handling": {
        "python": '''#!/usr/bin/env python3
"""MCP Server with Error Handling"""
import asyncio
import logging
from mcp.server import Server
from mcp.server.stdio import stdio_server
from mcp.types import Tool, TextContent

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

server = Server("error-handling-server")

@server.list_tools()
async def list_tools():
    return [
        Tool(
            name="divide",
            description="Divides two numbers",
            inputSchema={
                "type": "object",
                "properties": {
                    "a": {"type": "number", "description": "Dividend"},
                    "b": {"type": "number", "description": "Divisor"}
                },
                "required": ["a", "b"]
            }
        )
    ]

@server.call_tool()
async def call_tool(name: str, arguments: dict):
    try:
        if name == "divide":
            a = arguments.get("a")
            b = arguments.get("b")
            
            # Validate inputs
            if not isinstance(a, (int, float)) or not isinstance(b, (int, float)):
                raise ValueError("Both a and b must be numbers")
            
            if b == 0:
                raise ValueError("Division by zero is not allowed")
            
            result = a / b
            logger.info(f"Division: {a} / {b} = {result}")
            return [TextContent(type="text", text=str(result))]
        
        raise ValueError(f"Unknown tool: {name}")
    
    except ValueError as e:
        logger.error(f"Validation error: {e}")
        raise
    except Exception as e:
        logger.error(f"Unexpected error: {e}", exc_info=True)
        raise ValueError(f"An error occurred: {str(e)}")

async def main():
    async with stdio_server() as (read_stream, write_stream):
        await server.run(read_stream, write_stream, server.create_initialization_options())

if __name__ == "__main__":
    asyncio.run(main())
''',
        "typescript": '''/**
 * MCP Server with Error Handling
 */
import { Server } from "@modelcontextprotocol/sdk/server/index.js";
import { StdioServerTransport } from "@modelcontextprotocol/sdk/server/stdio.js";

const server = new Server(
  {
    name: "error-handling-server",
    version: "0.1.0",
  },
  {
    capabilities: {
      tools: {},
    },
  }
);

server.setRequestHandler(ListToolsRequestSchema, async () => ({
  tools: [
    {
      name: "divide",
      description: "Divides two numbers",
      inputSchema: {
        type: "object",
        properties: {
          a: { type: "number", description: "Dividend" },
          b: { type: "number", description: "Divisor" },
        },
        required: ["a", "b"],
      },
    },
  ],
}));

server.setRequestHandler(CallToolRequestSchema, async (request) => {
  try {
    if (request.params.name === "divide") {
      const a = request.params.arguments?.a;
      const b = request.params.arguments?.b;
      
      if (typeof a !== "number" || typeof b !== "number") {
        throw new Error("Both a and b must be numbers");
      }
      
      if (b === 0) {
        throw new Error("Division by zero is not allowed");
      }
      
      const result = a / b;
      console.error(`Division: ${a} / ${b} = ${result}`);
      
      return {
        content: [
          {
            type: "text",
            text: result.toString(),
          },
        ],
      };
    }
    
    throw new Error(`Unknown tool: ${request.params.name}`);
  } catch (error) {
    console.error(`Error: ${error}`);
    throw error;
  }
});

async function main() {
  const transport = new StdioServerTransport();
  await server.connect(transport);
}

main().catch(console.error);
'''
    }
}

PATTERNS = {
    "authentication": {
        "python": '''# Authentication Pattern (Python)

import os
from functools import wraps

API_KEY = os.getenv("API_KEY")

def require_auth(func):
    """Decorator to require authentication."""
    @wraps(func)
    async def wrapper(*args, **kwargs):
        if not API_KEY:
            raise ValueError("Authentication required")
        return await func(*args, **kwargs)
    return wrapper

@server.call_tool()
@require_auth
async def call_tool(name: str, arguments: dict):
    # Tool implementation
    pass
''',
        "typescript": '''// Authentication Pattern (TypeScript)

const API_KEY = process.env.API_KEY;

function requireAuth<T extends (...args: any[]) => Promise<any>>(
  fn: T
): T {
  return (async (...args: Parameters<T>) => {
    if (!API_KEY) {
      throw new Error("Authentication required");
    }
    return fn(...args);
  }) as T;
}

server.setRequestHandler(CallToolRequestSchema, requireAuth(async (request) => {
  // Tool implementation
}));
'''
    },
    "error-handling": {
        "python": '''# Error Handling Pattern (Python)

import logging

logger = logging.getLogger(__name__)

@server.call_tool()
async def call_tool(name: str, arguments: dict):
    try:
        # Validate inputs
        if "required_param" not in arguments:
            raise ValueError("required_param is required")
        
        # Process
        result = process_data(arguments)
        return [TextContent(type="text", text=result)]
    
    except ValueError as e:
        logger.error(f"Validation error: {e}")
        raise
    except Exception as e:
        logger.error(f"Unexpected error: {e}", exc_info=True)
        raise ValueError(f"An error occurred: {str(e)}")
''',
        "typescript": '''// Error Handling Pattern (TypeScript)

server.setRequestHandler(CallToolRequestSchema, async (request) => {
  try {
    // Validate inputs
    if (!request.params.arguments?.requiredParam) {
      throw new Error("requiredParam is required");
    }
    
    // Process
    const result = processData(request.params.arguments);
    return {
      content: [{ type: "text", text: result }],
    };
  } catch (error) {
    console.error(`Error: ${error}`);
    throw error;
  }
});
'''
    },
    "rate-limiting": {
        "python": '''# Rate Limiting Pattern (Python)

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
        self.calls[key] = [t for t in self.calls[key] if t > window_start]
        
        if len(self.calls[key]) >= self.max_calls:
            return False
        self.calls[key].append(now)
        return True

limiter = RateLimiter(max_calls=10, window_seconds=60)

@server.call_tool()
async def call_tool(name: str, arguments: dict):
    if not limiter.check("default"):
        raise ValueError("Rate limit exceeded")
    # Process tool
''',
        "typescript": '''// Rate Limiting Pattern (TypeScript)

class RateLimiter {
  private calls: Map<string, number[]> = new Map();
  
  constructor(
    private maxCalls: number,
    private windowMs: number
  ) {}
  
  check(key: string): boolean {
    const now = Date.now();
    const windowStart = now - this.windowMs;
    const calls = this.calls.get(key) || [];
    const recentCalls = calls.filter(t => t > windowStart);
    
    if (recentCalls.length >= this.maxCalls) {
      return false;
    }
    recentCalls.push(now);
    this.calls.set(key, recentCalls);
    return true;
  }
}

const limiter = new RateLimiter(10, 60000);

server.setRequestHandler(CallToolRequestSchema, async (request) => {
  if (!limiter.check("default")) {
    throw new Error("Rate limit exceeded");
  }
  // Process tool
});
'''
    },
    "logging": {
        "python": '''# Logging Pattern (Python)

import logging
import json

logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s'
)
logger = logging.getLogger(__name__)

@server.call_tool()
async def call_tool(name: str, arguments: dict):
    logger.info(f"Tool called: {name}", extra={
        "tool": name,
        "arguments": {k: v for k, v in arguments.items() if k != "password"}
    })
    
    try:
        result = process_tool(name, arguments)
        logger.info(f"Tool {name} completed")
        return result
    except Exception as e:
        logger.error(f"Tool {name} failed: {e}", exc_info=True)
        raise
''',
        "typescript": '''// Logging Pattern (TypeScript)

function logToolCall(name: string, arguments: Record<string, any>): void {
  console.error(JSON.stringify({
    event: "tool_call",
    tool: name,
    arguments: Object.fromEntries(
      Object.entries(arguments).filter(([k]) => k !== "password")
    ),
    timestamp: new Date().toISOString(),
  }));
}

server.setRequestHandler(CallToolRequestSchema, async (request) => {
  logToolCall(request.params.name, request.params.arguments || {});
  
  try {
    const result = processTool(request.params.name, request.params.arguments);
    console.error(`Tool ${request.params.name} completed`);
    return result;
  } catch (error) {
    console.error(`Tool ${request.params.name} failed:`, error);
    throw error;
  }
});
'''
    }
}

async def handle_example_library(name: str, arguments: dict) -> list[TextContent]:
    """Handle example library tool calls."""
    if name == "get_example_server":
        example_type = arguments.get("exampleType")
        language = arguments.get("language")
        
        if example_type not in EXAMPLES:
            raise ValueError(f"Unknown example type: {example_type}")
        if language not in EXAMPLES[example_type]:
            raise ValueError(f"Example not available for language: {language}")
        
        example = {
            "type": example_type,
            "language": language,
            "code": EXAMPLES[example_type][language]
        }
        return [TextContent(type="text", text=json.dumps(example, indent=2))]
    
    elif name == "get_pattern":
        pattern_name = arguments.get("patternName")
        language = arguments.get("language")
        
        if pattern_name not in PATTERNS:
            raise ValueError(f"Unknown pattern: {pattern_name}")
        if language not in PATTERNS[pattern_name]:
            raise ValueError(f"Pattern not available for language: {language}")
        
        pattern = {
            "pattern": pattern_name,
            "language": language,
            "code": PATTERNS[pattern_name][language]
        }
        return [TextContent(type="text", text=json.dumps(pattern, indent=2))]
    
    else:
        raise ValueError(f"Unknown example library tool: {name}")

