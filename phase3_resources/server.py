from mcp.server.fastmcp import FastMCP
from pathlib import Path

mcp = FastMCP("resources-server")

# --- Tools (actions) ---
@mcp.tool()
def create_ticket(title: str, description: str) -> dict:
    """Create a support ticket."""
    return {
        "ticket_id": "TKT-001",
        "title": title,
        "description": description,
        "status": "open"
    }

# --- Resources (knowledge) ---
@mcp.resource("policy://company")
def get_company_policy() -> str:
    """Read the company policy document."""
    path = Path(__file__).parent / "company_policy.md"
    return path.read_text()

@mcp.resource("policy://leave")
def get_leave_policy() -> str:
    """Read just the leave policy."""
    return """
## Leave Policy
- Employees get 20 days of paid leave per year.
- Leave must be applied 2 days in advance.
"""

if __name__ == "__main__":
    mcp.run(transport="stdio")