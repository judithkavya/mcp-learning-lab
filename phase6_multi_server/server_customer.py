from mcp.server.fastmcp import FastMCP

mcp = FastMCP("customer-server")

@mcp.tool()
def get_customer(customer_id: str) -> dict:
    """Get customer details by ID."""
    customers = {
        "123": {"id": "123", "name": "Nico", "email": "nico@example.com", "plan": "premium"},
        "456": {"id": "456", "name": "Robin", "email": "robin@example.com", "plan": "basic"},
    }
    return customers.get(customer_id, {"error": "Customer not found"})

@mcp.tool()
def list_customers() -> list:
    """List all customers."""
    return [
        {"id": "123", "name": "Nico", "plan": "premium"},
        {"id": "456", "name": "Robin", "plan": "basic"},
    ]

if __name__ == "__main__":
    mcp.run(transport="stdio")