from mcp.server.fastmcp import FastMCP

mcp = FastMCP("customer-server")

@mcp.tool()
def get_customer(customer_id: str) -> dict:
    """Get customer details by ID."""
    return {"id": customer_id, "name": "Axl", "email": "axl@example.com"}

@mcp.tool()
def create_ticket(title: str, description: str) -> dict:
    """Create a support ticket."""
    return {"ticket_id": "TKT-001", "title": title, "description": description , "status": "open"}

if __name__ == "__main__":
    mcp.run(transport="stdio")