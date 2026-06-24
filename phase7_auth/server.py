import os
from mcp.server.fastmcp import FastMCP
from dotenv import load_dotenv

load_dotenv("phase7_auth/.env")

API_KEY = os.getenv("MCP_API_KEY")

mcp = FastMCP("auth-server")

def verify_token(token: str) -> bool:
    """Check if the provided token matches our API key."""
    return token == API_KEY

@mcp.tool()
def get_secret_data(token: str) -> dict:
    """Get protected data — requires a valid token."""
    if not verify_token(token):
        return {"error": "Unauthorized — invalid token"}
    return {
        "data": "This is protected data",
        "user": "authenticated",
        "records": {1: "will of the D", 2: "poneglyph", 3: "one piece"}
    }

@mcp.tool()
def get_public_data() -> dict:
    """Get public data — no token needed."""
    return {"data": "This is public data", "status": "ok"}

if __name__ == "__main__":
    mcp.run(transport="stdio")