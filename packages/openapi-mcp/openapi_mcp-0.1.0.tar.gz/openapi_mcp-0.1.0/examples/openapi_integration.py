"""
Example of using OpenAPI-MCP with an OpenAPI specification URL.

This example demonstrates how OpenAPI-MCP automatically creates an MCP server from any OpenAPI spec.
"""

from openapi_mcp import create_mcp_server, serve_mcp


def main():
    """Create and serve an MCP server from a public OpenAPI specification."""
    print("Creating an MCP server from the Swagger Petstore OpenAPI spec...")
    print("No configuration needed - just point it at the OpenAPI spec and it works!")
    
    # One line to create the MCP server - that's it!
    # OpenAPI-MCP automatically discovers all endpoints and converts them to MCP tools
    mcp_server = create_mcp_server("https://petstore3.swagger.io/api/v3/openapi.json")
    
    # Start the server
    print("Starting MCP server on http://localhost:8000")
    print("Connect to this MCP server in Claude to access the Petstore API")
    serve_mcp(mcp_server, host="127.0.0.1", port=8000)


if __name__ == "__main__":
    main() 