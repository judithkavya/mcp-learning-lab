from mcp.server.fastmcp import FastMCP

mcp = FastMCP("tools-server")

@mcp.tool()
def get_customer(customer_id: str) -> dict:
    """Get customer details by ID."""
    mock_customers = {
        "123": {"id": "123", "name": "Naruto", "email": "naruto@example.com"},
        "456": {"id": "456", "name": "Sasuke", "email": "sasuke@example.com"},
    }
    return mock_customers.get(customer_id, {"error": "Customer not found"})

@mcp.tool()
def create_ticket(title: str, description: str) -> dict:
    """Create a support ticket."""
    return {
        "ticket_id": "TKT-001",
        "title": title,
        "description": description,
        "status": "open"
    }

@mcp.tool()
def get_weather(city: str) -> dict:
    """Get weather for a city."""
    mock_weather = {
        "bangalore": {"city": "Bangalore", "temp": "24C", "condition": "Cloudy"},
        "mumbai": {"city": "Mumbai", "temp": "31C", "condition": "Humid"},
    }
    return mock_weather.get(city.lower(), {"error": "City not found"})

if __name__ == "__main__":
    mcp.run(transport="stdio")