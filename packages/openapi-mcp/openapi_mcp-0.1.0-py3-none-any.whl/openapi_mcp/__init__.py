"""
OpenAPI-MCP: Automatic MCP server generator for OpenAPI applications.

Created by Tadata Inc. (https://github.com/tadata-org)
"""

__version__ = "0.1.0"

from .server import add_mcp_server, create_mcp_server, mount_mcp_server, serve_mcp
from .http_tools import create_mcp_tools_from_openapi

__all__ = [
    "add_mcp_server",
    "create_mcp_server",
    "mount_mcp_server",
    "create_mcp_tools_from_openapi",
    "serve_mcp",
]
