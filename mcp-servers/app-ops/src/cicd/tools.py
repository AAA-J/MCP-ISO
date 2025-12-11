"""CI/CD integration tools."""

import json
from typing import List, Dict, Optional
from mcp.types import Tool, TextContent


cicd_tools = [
    Tool(
        name="list_pipelines",
        description="List all CI/CD pipelines",
        inputSchema={
            "type": "object",
            "properties": {
                "limit": {
                    "type": "integer",
                    "description": "Maximum number of pipelines to return",
                    "default": 50
                }
            }
        }
    ),
    Tool(
        name="get_pipeline_status",
        description="Get the status of a specific pipeline execution",
        inputSchema={
            "type": "object",
            "properties": {
                "id": {
                    "type": "string",
                    "description": "Pipeline execution ID"
                }
            },
            "required": ["id"]
        }
    ),
    Tool(
        name="get_last_failed_build",
        description="Get details of the last failed build for a service",
        inputSchema={
            "type": "object",
            "properties": {
                "service": {
                    "type": "string",
                    "description": "Service name"
                }
            },
            "required": ["service"]
        }
    ),
]


async def handle_cicd(
    name: str,
    arguments: dict,
    cicd_adapter
) -> List[TextContent]:
    """Handle CI/CD tool calls."""
    
    if name == "list_pipelines":
        limit = arguments.get("limit", 50)
        pipelines = await cicd_adapter.list_pipelines(limit)
        
        if not pipelines:
            return [TextContent(
                type="text",
                text="No pipelines found."
            )]
        
        result = f"Found {len(pipelines)} pipeline(s):\n\n"
        for pipeline in pipelines:
            result += f"- **{pipeline.get('name', 'Unknown')}** (ID: {pipeline.get('id', 'N/A')})\n"
            result += f"  Status: {pipeline.get('status', 'Unknown')}\n"
            if pipeline.get('last_run'):
                result += f"  Last run: {pipeline.get('last_run')}\n"
            result += "\n"
        
        return [TextContent(type="text", text=result)]
    
    elif name == "get_pipeline_status":
        pipeline_id = arguments.get("id")
        if not pipeline_id:
            return [TextContent(
                type="text",
                text="Error: Pipeline ID is required"
            )]
        
        status = await cicd_adapter.get_pipeline_status(pipeline_id)
        return [TextContent(
            type="text",
            text=json.dumps(status, indent=2)
        )]
    
    elif name == "get_last_failed_build":
        service = arguments.get("service")
        if not service:
            return [TextContent(
                type="text",
                text="Error: Service name is required"
            )]
        
        build_info = await cicd_adapter.get_last_failed_build(service)
        return [TextContent(
            type="text",
            text=json.dumps(build_info, indent=2)
        )]
    
    else:
        raise ValueError(f"Unknown CI/CD tool: {name}")


class CICDAdapter:
    """Base class for CI/CD adapters."""
    
    async def list_pipelines(self, limit: int = 50) -> List[Dict]:
        """List all pipelines."""
        raise NotImplementedError
    
    async def get_pipeline_status(self, pipeline_id: str) -> Dict:
        """Get pipeline status."""
        raise NotImplementedError
    
    async def get_last_failed_build(self, service: str) -> Dict:
        """Get last failed build for a service."""
        raise NotImplementedError


class GitHubActionsAdapter(CICDAdapter):
    """GitHub Actions CI/CD adapter."""
    
    def __init__(self, token: str, owner: str, repo: str):
        try:
            from github import Github
            self.github = Github(token)
            self.repo = self.github.get_repo(f"{owner}/{repo}")
        except ImportError:
            raise ImportError("PyGithub is required for GitHub Actions support. Install with: pip install PyGithub")
    
    async def list_pipelines(self, limit: int = 50) -> List[Dict]:
        """List GitHub Actions workflows."""
        workflows = self.repo.get_workflows()
        pipelines = []
        
        for workflow in list(workflows)[:limit]:
            runs = workflow.get_runs()
            last_run = runs[0] if runs.totalCount > 0 else None
            
            pipelines.append({
                "id": str(workflow.id),
                "name": workflow.name,
                "status": last_run.status if last_run else "unknown",
                "last_run": last_run.created_at.isoformat() if last_run else None
            })
        
        return pipelines
    
    async def get_pipeline_status(self, pipeline_id: str) -> Dict:
        """Get GitHub Actions workflow run status."""
        try:
            run = self.repo.get_workflow_run(int(pipeline_id))
            return {
                "id": str(run.id),
                "name": run.name,
                "status": run.status,
                "conclusion": run.conclusion,
                "created_at": run.created_at.isoformat(),
                "updated_at": run.updated_at.isoformat(),
                "html_url": run.html_url
            }
        except Exception as e:
            return {"error": str(e)}
    
    async def get_last_failed_build(self, service: str) -> Dict:
        """Get last failed workflow run for a service."""
        workflows = self.repo.get_workflows()
        
        for workflow in workflows:
            if service.lower() in workflow.name.lower():
                runs = workflow.get_runs(status="failure")
                if runs.totalCount > 0:
                    run = runs[0]
                    return {
                        "id": str(run.id),
                        "name": run.name,
                        "status": run.status,
                        "conclusion": run.conclusion,
                        "created_at": run.created_at.isoformat(),
                        "html_url": run.html_url,
                        "workflow": workflow.name
                    }
        
        return {"error": f"No failed builds found for service: {service}"}


class GenericCICDAdapter(CICDAdapter):
    """Generic CI/CD adapter using REST API."""
    
    def __init__(self, base_url: str, token: Optional[str] = None):
        import httpx
        self.base_url = base_url
        self.token = token
        self.client = httpx.AsyncClient()
    
    async def list_pipelines(self, limit: int = 50) -> List[Dict]:
        """List pipelines via generic API."""
        headers = {}
        if self.token:
            headers["Authorization"] = f"Bearer {self.token}"
        
        try:
            response = await self.client.get(
                f"{self.base_url}/pipelines",
                headers=headers,
                params={"limit": limit}
            )
            response.raise_for_status()
            return response.json()
        except Exception as e:
            return [{"error": str(e)}]
    
    async def get_pipeline_status(self, pipeline_id: str) -> Dict:
        """Get pipeline status via generic API."""
        headers = {}
        if self.token:
            headers["Authorization"] = f"Bearer {self.token}"
        
        try:
            response = await self.client.get(
                f"{self.base_url}/pipelines/{pipeline_id}",
                headers=headers
            )
            response.raise_for_status()
            return response.json()
        except Exception as e:
            return {"error": str(e)}
    
    async def get_last_failed_build(self, service: str) -> Dict:
        """Get last failed build via generic API."""
        headers = {}
        if self.token:
            headers["Authorization"] = f"Bearer {self.token}"
        
        try:
            response = await self.client.get(
                f"{self.base_url}/services/{service}/builds/last-failed",
                headers=headers
            )
            response.raise_for_status()
            return response.json()
        except Exception as e:
            return {"error": str(e)}


def create_cicd_adapter(adapter_type: str, config: Dict) -> CICDAdapter:
    """Create a CI/CD adapter based on type."""
    if adapter_type == "github_actions":
        return GitHubActionsAdapter(
            token=config.get("token"),
            owner=config.get("owner"),
            repo=config.get("repo")
        )
    elif adapter_type == "generic":
        return GenericCICDAdapter(
            base_url=config.get("base_url"),
            token=config.get("token")
        )
    else:
        raise ValueError(f"Unsupported CI/CD adapter type: {adapter_type}")

