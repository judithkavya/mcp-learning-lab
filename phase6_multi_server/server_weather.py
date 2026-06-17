from mcp.server.fastmcp import FastMCP

mcp = FastMCP("weather-server")

@mcp.tool()
def get_weather(city: str) -> dict:
    """Get current weather for a city."""
    mock = {
        "bangalore": {"temp": "24C", "condition": "Cloudy"},
        "mumbai": {"temp": "31C", "condition": "Humid"},
        "delhi": {"temp": "38C", "condition": "Sunny"},
    }
    return mock.get(city.lower(), {"error": "City not found"})

@mcp.tool()
def get_forecast(city: str, days: int) -> dict:
    """Get weather forecast for N days."""
    return {
        "city": city,
        "days": days,
        "forecast": f"Mostly cloudy for {days} days with occasional rain"
    }

if __name__ == "__main__":
    mcp.run(transport="stdio")