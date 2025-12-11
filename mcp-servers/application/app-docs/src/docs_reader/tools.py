"""Documentation reader tools for app-docs server."""

import os
from pathlib import Path
from typing import List, Dict
from mcp.types import Resource, TextContent


def discover_docs(docs_dir: str) -> List[Resource]:
    """Discover all markdown files in the docs directory."""
    resources = []
    docs_path = Path(docs_dir)
    
    if not docs_path.exists():
        return resources
    
    # Common documentation files at root
    root_files = ["AGENTS.md", "AI.md", "README.md"]
    for filename in root_files:
        file_path = docs_path.parent / filename
        if file_path.exists() and file_path.suffix == ".md":
            name = filename.replace(".md", "").lower()
            resources.append(Resource(
                uri=f"app-docs://docs/{name}",
                name=f"{name.title()} Documentation",
                description=f"Documentation from {filename}",
                mimeType="text/markdown"
            ))
    
    # Files in docs/ directory
    if docs_path.is_dir():
        for file_path in docs_path.rglob("*.md"):
            # Get relative path from docs_dir
            rel_path = file_path.relative_to(docs_path)
            # Convert to URI-friendly path
            uri_path = str(rel_path).replace("\\", "/").replace(".md", "")
            name = file_path.stem.replace("-", " ").replace("_", " ").title()
            
            resources.append(Resource(
                uri=f"app-docs://docs/{uri_path}",
                name=name,
                description=f"Documentation from {file_path.name}",
                mimeType="text/markdown"
            ))
    
    # Discover diagram files
    diagram_extensions = [".svg", ".png", ".jpg", ".jpeg", ".gif", ".pdf"]
    if docs_path.is_dir():
        for file_path in docs_path.rglob("*"):
            if file_path.suffix.lower() in diagram_extensions:
                rel_path = file_path.relative_to(docs_path)
                uri_path = str(rel_path).replace("\\", "/")
                name = file_path.stem.replace("-", " ").replace("_", " ").title()
                
                mime_type = {
                    ".svg": "image/svg+xml",
                    ".png": "image/png",
                    ".jpg": "image/jpeg",
                    ".jpeg": "image/jpeg",
                    ".gif": "image/gif",
                    ".pdf": "application/pdf"
                }.get(file_path.suffix.lower(), "application/octet-stream")
                
                resources.append(Resource(
                    uri=f"app-docs://diagrams/{uri_path}",
                    name=name,
                    description=f"Diagram: {file_path.name}",
                    mimeType=mime_type
                ))
    
    return resources


async def read_doc_resource(uri: str, docs_dir: str) -> str:
    """Read a documentation resource."""
    uri_str = str(uri)
    docs_path = Path(docs_dir)
    
    if uri_str.startswith("app-docs://docs/"):
        # Extract the path
        doc_path = uri_str.replace("app-docs://docs/", "")
        
        # Handle root-level files
        root_files = {
            "agents": "AGENTS.md",
            "ai": "AI.md",
            "readme": "README.md"
        }
        
        if doc_path in root_files:
            file_path = docs_path.parent / root_files[doc_path]
        else:
            # File in docs/ directory
            file_path = docs_path / f"{doc_path}.md"
        
        if file_path.exists() and file_path.is_file():
            return file_path.read_text(encoding="utf-8")
        else:
            raise ValueError(f"Document not found: {uri_str}")
    
    elif uri_str.startswith("app-docs://diagrams/"):
        # Extract the path
        diagram_path = uri_str.replace("app-docs://diagrams/", "")
        file_path = docs_path / diagram_path
        
        if file_path.exists() and file_path.is_file():
            # For binary files, return base64 encoded
            import base64
            file_data = file_path.read_bytes()
            return base64.b64encode(file_data).decode("utf-8")
        else:
            raise ValueError(f"Diagram not found: {uri_str}")
    
    else:
        raise ValueError(f"Unknown resource URI: {uri_str}")

