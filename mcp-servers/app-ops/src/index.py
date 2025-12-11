#!/usr/bin/env python3
"""
App-Ops MCP Server - Observability and CI/CD
Provides tools for monitoring CI/CD pipelines, logs, and metrics
"""

import asyncio
import os
import json
from dotenv import load_dotenv
from mcp.server import Server
from mcp.server.stdio import stdio_server
from mcp.types import Tool, Resource, TextContent

from cicd.tools import cicd_tools, handle_cicd, create_cicd_adapter
from observability.tools import (
    observability_tools,
    handle_observability,
    create_log_adapter,
    create_metrics_adapter
)

# Load environment variables
load_dotenv()

# Initialize MCP server
server = Server("app-ops")

# CI/CD Configuration
CICD_TYPE = os.getenv("CICD_TYPE", "github_actions").lower()
CICD_TOKEN = os.getenv("CICD_TOKEN")
CICD_OWNER = os.getenv("CICD_OWNER")  # For GitHub Actions
CICD_REPO = os.getenv("CICD_REPO")  # For GitHub Actions
CICD_BASE_URL = os.getenv("CICD_BASE_URL")  # For generic CI/CD

# Observability Configuration
LOG_TYPE = os.getenv("LOG_TYPE", "generic").lower()
LOG_BASE_URL = os.getenv("LOG_BASE_URL")
LOG_TOKEN = os.getenv("LOG_TOKEN")

METRICS_TYPE = os.getenv("METRICS_TYPE", "generic").lower()
METRICS_BASE_URL = os.getenv("METRICS_BASE_URL")
METRICS_TOKEN = os.getenv("METRICS_TOKEN")

# Initialize adapters
cicd_adapter = None
log_adapter = None
metrics_adapter = None


def get_cicd_adapter():
    """Get or create CI/CD adapter."""
    global cicd_adapter
    
    if cicd_adapter is not None:
        return cicd_adapter
    
    config = {
        "token": CICD_TOKEN,
        "owner": CICD_OWNER,
        "repo": CICD_REPO,
        "base_url": CICD_BASE_URL
    }
    
    cicd_adapter = create_cicd_adapter(CICD_TYPE, config)
    return cicd_adapter


def get_log_adapter():
    """Get or create log adapter."""
    global log_adapter
    
    if log_adapter is not None:
        return log_adapter
    
    if not LOG_BASE_URL:
        return None
    
    config = {
        "base_url": LOG_BASE_URL,
        "token": LOG_TOKEN
    }
    
    log_adapter = create_log_adapter(LOG_TYPE, config)
    return log_adapter


def get_metrics_adapter():
    """Get or create metrics adapter."""
    global metrics_adapter
    
    if metrics_adapter is not None:
        return metrics_adapter
    
    if not METRICS_BASE_URL:
        return None
    
    config = {
        "base_url": METRICS_BASE_URL,
        "token": METRICS_TOKEN
    }
    
    metrics_adapter = create_metrics_adapter(METRICS_TYPE, config)
    return metrics_adapter


@server.list_tools()
async def list_tools() -> list[Tool]:
    """List all available tools."""
    tools = cicd_tools.copy()
    
    # Only add observability tools if adapters are configured
    if get_log_adapter() or get_metrics_adapter():
        tools.extend(observability_tools)
    
    return tools


@server.call_tool()
async def call_tool(name: str, arguments: dict) -> list[TextContent]:
    """Handle tool calls."""
    if name in ["list_pipelines", "get_pipeline_status", "get_last_failed_build"]:
        adapter = get_cicd_adapter()
        return await handle_cicd(name, arguments, adapter)
    elif name in ["get_recent_errors", "get_metric_timeseries"]:
        log_adapter = get_log_adapter()
        metrics_adapter = get_metrics_adapter()
        return await handle_observability(name, arguments, log_adapter, metrics_adapter)
    else:
        raise ValueError(f"Unknown tool: {name}")


@server.list_resources()
async def list_resources() -> list[Resource]:
    """List available resources."""
    resources = []
    
    # Add pipeline resources if CI/CD is configured
    if get_cicd_adapter():
        try:
            pipelines = await get_cicd_adapter().list_pipelines(limit=20)
            for pipeline in pipelines:
                resources.append(Resource(
                    uri=f"app-ops://pipelines/{pipeline.get('id')}",
                    name=f"Pipeline: {pipeline.get('name')}",
                    description=f"CI/CD pipeline: {pipeline.get('name')}",
                    mimeType="application/json"
                ))
        except Exception:
            pass
    
    # Add services resource
    resources.append(Resource(
        uri="app-ops://services",
        name="Monitored Services",
        description="List of monitored services",
        mimeType="application/json"
    ))
    
    return resources


@server.read_resource()
async def read_resource(uri: str) -> str:
    """Read a resource."""
    uri_str = str(uri)
    
    if uri_str.startswith("app-ops://pipelines/"):
        pipeline_id = uri_str.replace("app-ops://pipelines/", "")
        adapter = get_cicd_adapter()
        status = await adapter.get_pipeline_status(pipeline_id)
        return json.dumps(status, indent=2)
    
    elif uri_str == "app-ops://services":
        # Return list of services (could be from config or discovered)
        services = os.getenv("MONITORED_SERVICES", "").split(",")
        services = [s.strip() for s in services if s.strip()]
        return json.dumps({"services": services}, indent=2)
    
    else:
        raise ValueError(f"Unknown resource: {uri_str}")


async def main():
    """Main entry point."""
    async with stdio_server() as (read_stream, write_stream):
        await server.run(
            read_stream,
            write_stream,
            server.create_initialization_options()
        )


if __name__ == "__main__":
    asyncio.run(main())

