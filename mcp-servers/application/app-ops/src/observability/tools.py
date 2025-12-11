"""Observability tools for logs and metrics."""

import json
from typing import List, Dict, Optional
from mcp.types import Tool, TextContent, Resource


observability_tools = [
    Tool(
        name="get_recent_errors",
        description="Get recent error logs for a service",
        inputSchema={
            "type": "object",
            "properties": {
                "service": {
                    "type": "string",
                    "description": "Service name"
                },
                "limit": {
                    "type": "integer",
                    "description": "Maximum number of errors to return",
                    "default": 50
                },
                "time_window": {
                    "type": "string",
                    "description": "Time window (e.g., '10m', '1h', '24h')",
                    "default": "1h"
                }
            },
            "required": ["service"]
        }
    ),
    Tool(
        name="get_metric_timeseries",
        description="Get metric timeseries data",
        inputSchema={
            "type": "object",
            "properties": {
                "service": {
                    "type": "string",
                    "description": "Service name"
                },
                "metric": {
                    "type": "string",
                    "description": "Metric name (e.g., 'cpu_usage', 'request_rate', 'error_rate')"
                },
                "window": {
                    "type": "string",
                    "description": "Time window (e.g., '10m', '1h', '24h')",
                    "default": "1h"
                }
            },
            "required": ["service", "metric"]
        }
    ),
]


async def handle_observability(
    name: str,
    arguments: dict,
    log_adapter,
    metrics_adapter
) -> List[TextContent]:
    """Handle observability tool calls."""
    
    if name == "get_recent_errors":
        service = arguments.get("service")
        limit = arguments.get("limit", 50)
        time_window = arguments.get("time_window", "1h")
        
        if not service:
            return [TextContent(
                type="text",
                text="Error: Service name is required"
            )]
        
        errors = await log_adapter.get_recent_errors(service, limit, time_window)
        
        if not errors:
            return [TextContent(
                type="text",
                text=f"No errors found for service '{service}' in the last {time_window}"
            )]
        
        result = f"Found {len(errors)} error(s) for service '{service}':\n\n"
        for error in errors:
            result += f"**{error.get('timestamp', 'Unknown time')}**\n"
            result += f"Level: {error.get('level', 'Unknown')}\n"
            result += f"Message: {error.get('message', 'N/A')}\n"
            if error.get('traceback'):
                result += f"Traceback: {error.get('traceback')[:200]}...\n"
            result += "\n"
        
        return [TextContent(type="text", text=result)]
    
    elif name == "get_metric_timeseries":
        service = arguments.get("service")
        metric = arguments.get("metric")
        window = arguments.get("window", "1h")
        
        if not service or not metric:
            return [TextContent(
                type="text",
                text="Error: Service name and metric are required"
            )]
        
        timeseries = await metrics_adapter.get_metric_timeseries(service, metric, window)
        
        if not timeseries:
            return [TextContent(
                type="text",
                text=f"No metric data found for '{metric}' on service '{service}'"
            )]
        
        result = f"Metric: {metric} for service: {service}\n"
        result += f"Time window: {window}\n\n"
        result += json.dumps(timeseries, indent=2)
        
        return [TextContent(type="text", text=result)]
    
    else:
        raise ValueError(f"Unknown observability tool: {name}")


class LogAdapter:
    """Base class for log adapters."""
    
    async def get_recent_errors(self, service: str, limit: int, time_window: str) -> List[Dict]:
        """Get recent errors."""
        raise NotImplementedError


class MetricsAdapter:
    """Base class for metrics adapters."""
    
    async def get_metric_timeseries(self, service: str, metric: str, window: str) -> Dict:
        """Get metric timeseries."""
        raise NotImplementedError


class GenericLogAdapter(LogAdapter):
    """Generic log adapter using REST API."""
    
    def __init__(self, base_url: str, token: Optional[str] = None):
        import httpx
        self.base_url = base_url
        self.token = token
        self.client = httpx.AsyncClient()
    
    async def get_recent_errors(self, service: str, limit: int, time_window: str) -> List[Dict]:
        """Get recent errors via API."""
        headers = {}
        if self.token:
            headers["Authorization"] = f"Bearer {self.token}"
        
        try:
            response = await self.client.get(
                f"{self.base_url}/logs/errors",
                headers=headers,
                params={
                    "service": service,
                    "limit": limit,
                    "window": time_window
                }
            )
            response.raise_for_status()
            return response.json()
        except Exception as e:
            return [{"error": str(e)}]


class GenericMetricsAdapter(MetricsAdapter):
    """Generic metrics adapter using REST API."""
    
    def __init__(self, base_url: str, token: Optional[str] = None):
        import httpx
        self.base_url = base_url
        self.token = token
        self.client = httpx.AsyncClient()
    
    async def get_metric_timeseries(self, service: str, metric: str, window: str) -> Dict:
        """Get metric timeseries via API."""
        headers = {}
        if self.token:
            headers["Authorization"] = f"Bearer {self.token}"
        
        try:
            response = await self.client.get(
                f"{self.base_url}/metrics/timeseries",
                headers=headers,
                params={
                    "service": service,
                    "metric": metric,
                    "window": window
                }
            )
            response.raise_for_status()
            return response.json()
        except Exception as e:
            return {"error": str(e)}


def create_log_adapter(adapter_type: str, config: Dict) -> LogAdapter:
    """Create a log adapter based on type."""
    if adapter_type == "generic":
        return GenericLogAdapter(
            base_url=config.get("base_url"),
            token=config.get("token")
        )
    else:
        raise ValueError(f"Unsupported log adapter type: {adapter_type}")


def create_metrics_adapter(adapter_type: str, config: Dict) -> MetricsAdapter:
    """Create a metrics adapter based on type."""
    if adapter_type == "generic":
        return GenericMetricsAdapter(
            base_url=config.get("base_url"),
            token=config.get("token")
        )
    else:
        raise ValueError(f"Unsupported metrics adapter type: {adapter_type}")

