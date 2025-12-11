"""Documentation search tools for app-docs server."""

import os
import re
from pathlib import Path
from typing import List, Dict
from mcp.types import Tool, TextContent


def build_search_index(docs_dir: str) -> Dict[str, Dict]:
    """Build a search index of all documentation files."""
    index = {}
    docs_path = Path(docs_dir)
    
    if not docs_path.exists():
        return index
    
    # Index root-level files
    root_files = ["AGENTS.md", "AI.md", "README.md"]
    for filename in root_files:
        file_path = docs_path.parent / filename
        if file_path.exists() and file_path.suffix == ".md":
            content = file_path.read_text(encoding="utf-8")
            name = filename.replace(".md", "").lower()
            index[f"app-docs://docs/{name}"] = {
                "path": str(file_path),
                "name": name,
                "content": content.lower(),
                "original_content": content
            }
    
    # Index files in docs/ directory
    if docs_path.is_dir():
        for file_path in docs_path.rglob("*.md"):
            rel_path = file_path.relative_to(docs_path)
            uri_path = str(rel_path).replace("\\", "/").replace(".md", "")
            uri = f"app-docs://docs/{uri_path}"
            
            content = file_path.read_text(encoding="utf-8")
            index[uri] = {
                "path": str(file_path),
                "name": file_path.stem,
                "content": content.lower(),
                "original_content": content
            }
    
    return index


def search_docs(query: str, docs_dir: str, limit: int = 10) -> List[Dict]:
    """Search documentation files for a query."""
    index = build_search_index(docs_dir)
    query_lower = query.lower()
    query_words = set(query_lower.split())
    
    results = []
    
    for uri, doc_data in index.items():
        content = doc_data["content"]
        score = 0
        
        # Simple scoring: count word matches
        for word in query_words:
            if word in content:
                # Count occurrences
                score += content.count(word)
        
        # Boost score if query appears in title/name
        if query_lower in doc_data["name"].lower():
            score += 10
        
        # Boost score for exact phrase match
        if query_lower in content:
            score += 5
        
        if score > 0:
            # Extract snippet
            snippet = extract_snippet(doc_data["original_content"], query_lower, max_length=200)
            results.append({
                "uri": uri,
                "name": doc_data["name"],
                "score": score,
                "snippet": snippet
            })
    
    # Sort by score (descending)
    results.sort(key=lambda x: x["score"], reverse=True)
    
    return results[:limit]


def extract_snippet(content: str, query: str, max_length: int = 200) -> str:
    """Extract a snippet from content containing the query."""
    query_lower = query.lower()
    content_lower = content.lower()
    
    # Find first occurrence
    idx = content_lower.find(query_lower)
    if idx == -1:
        # Fallback: return first part of content
        return content[:max_length] + "..." if len(content) > max_length else content
    
    # Extract context around the match
    start = max(0, idx - max_length // 2)
    end = min(len(content), idx + len(query) + max_length // 2)
    
    snippet = content[start:end]
    if start > 0:
        snippet = "..." + snippet
    if end < len(content):
        snippet = snippet + "..."
    
    return snippet


search_tools = [
    Tool(
        name="search_docs",
        description="Search across all documentation files for a query string",
        inputSchema={
            "type": "object",
            "properties": {
                "query": {
                    "type": "string",
                    "description": "Search query string"
                },
                "limit": {
                    "type": "integer",
                    "description": "Maximum number of results to return",
                    "default": 10
                }
            },
            "required": ["query"]
        }
    ),
    Tool(
        name="get_diagram",
        description="Retrieve a diagram file by name (SVG, PNG, etc.)",
        inputSchema={
            "type": "object",
            "properties": {
                "name": {
                    "type": "string",
                    "description": "Name or path of the diagram file"
                }
            },
            "required": ["name"]
        }
    ),
]


async def handle_search(name: str, arguments: dict, docs_dir: str) -> List[TextContent]:
    """Handle search tool calls."""
    if name == "search_docs":
        query = arguments.get("query", "")
        limit = arguments.get("limit", 10)
        
        if not query:
            return [TextContent(
                type="text",
                text="Error: Query parameter is required"
            )]
        
        results = search_docs(query, docs_dir, limit)
        
        if not results:
            return [TextContent(
                type="text",
                text=f"No documentation found matching query: {query}"
            )]
        
        # Format results
        result_text = f"Found {len(results)} result(s) for '{query}':\n\n"
        for i, result in enumerate(results, 1):
            result_text += f"{i}. **{result['name']}** (score: {result['score']})\n"
            result_text += f"   URI: {result['uri']}\n"
            result_text += f"   Snippet: {result['snippet']}\n\n"
        
        return [TextContent(type="text", text=result_text)]
    
    elif name == "get_diagram":
        diagram_name = arguments.get("name", "")
        
        if not diagram_name:
            return [TextContent(
                type="text",
                text="Error: Diagram name parameter is required"
            )]
        
        docs_path = Path(docs_dir)
        
        # Try to find the diagram file
        diagram_extensions = [".svg", ".png", ".jpg", ".jpeg", ".gif", ".pdf"]
        found_file = None
        
        # Search in docs directory
        if docs_path.exists() and docs_path.is_dir():
            for ext in diagram_extensions:
                # Try exact match
                candidate = docs_path / f"{diagram_name}{ext}"
                if candidate.exists():
                    found_file = candidate
                    break
                
                # Try with name as path
                candidate = docs_path / f"{diagram_name}"
                if candidate.exists() and candidate.suffix.lower() in diagram_extensions:
                    found_file = candidate
                    break
                
                # Search recursively
                for file_path in docs_path.rglob(f"*{diagram_name}*{ext}"):
                    found_file = file_path
                    break
                
                if found_file:
                    break
        
        if not found_file or not found_file.exists():
            return [TextContent(
                type="text",
                text=f"Diagram not found: {diagram_name}"
            )]
        
        # Get relative path for URI
        rel_path = found_file.relative_to(docs_path)
        uri_path = str(rel_path).replace("\\", "/")
        uri = f"app-docs://diagrams/{uri_path}"
        
        return [TextContent(
            type="text",
            text=f"Diagram found: {found_file.name}\nURI: {uri}\nPath: {found_file}\n\nUse the read_resource tool to retrieve the diagram content."
        )]
    
    else:
        raise ValueError(f"Unknown search tool: {name}")

