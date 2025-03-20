"""
Command-line interface for OpenAPI-MCP.

Magically create MCP servers from any OpenAPI specification with zero configuration.
"""

import sys
import typer
from rich import print
from typing import Optional
from .server import create_mcp_server, serve_mcp


app = typer.Typer(
    name="openapi-mcp",
    help="✨ Magical MCP servers from any OpenAPI specification",
    add_completion=False,
)


@app.command("serve")
def serve(
    openapi_url: str = typer.Argument(
        ..., help="URL to your OpenAPI specification"
    ),
    host: str = typer.Option(
        "127.0.0.1", "--host", "-h", help="Host to bind the server to"
    ),
    port: int = typer.Option(
        8000, "--port", "-p", help="Port to bind the server to"
    ),
):
    """
    ✨ Magically create and serve an MCP server from any OpenAPI specification.
    
    Just point it at your OpenAPI URL and it does everything automatically!
    """
    try:
        print(f"[bold green]✨ Creating MCP server from:[/bold green] {openapi_url}")
        print("[bold]No configuration needed - it's magic![/bold]")
        
        # Create the MCP server - one line, no configuration!
        mcp_server = create_mcp_server(openapi_url)
        
        # Print server info
        print(f"[bold green]✨ Starting MCP server on:[/bold green] http://{host}:{port}")
        print("[bold]Connect to this MCP server in Claude to access all API endpoints automatically[/bold]")
        
        # Serve the MCP server
        serve_mcp(mcp_server, host=host, port=port)
        
    except Exception as e:
        print(f"[bold red]Error:[/bold red] {str(e)}")
        sys.exit(1)


@app.command("version")
def version():
    """
    Show the version of OpenAPI-MCP.
    """
    from . import __version__
    print(f"✨ OpenAPI-MCP version: {__version__}")


if __name__ == "__main__":
    app() 