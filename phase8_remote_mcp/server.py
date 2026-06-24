from mcp.server.fastmcp import FastMCP

mcp = FastMCP("remote-server")

@mcp.tool()
def get_customer(customer_id: str) -> dict:
    """Get customer details by ID."""
    customers = {
        "123": {"id": "123", "name": "Romero", "email": "romero@example.com"},
        "456": {"id": "456", "name": "Romano", "email": "romano@example.com"},
    }
    return customers.get(customer_id, {"error": "Customer not found"})

@mcp.tool()
def create_ticket(title: str, description: str, priority: str) -> dict:
    """Create a support ticket."""
    return {
        "ticket_id": "TKT-001",
        "title": title,
        "description": description,
        "priority": priority,
        "status": "open"
    }

@mcp.resource("docs://readme")
def get_readme() -> str:
    """Get the readme document."""
    return "This is a remote MCP server running over HTTP/SSE."

if __name__ == "__main__":
    # runs on http://localhost:8000 instead of stdio
    mcp.run(transport="streamable-http")