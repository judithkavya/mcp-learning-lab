from mcp.server.fastmcp import FastMCP

mcp = FastMCP("prompts-server")

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

@mcp.prompt()
def customer_support_template(customer_name: str, issue: str) -> str:
    """Reusable prompt template for customer support responses."""
    return f"""You are a helpful customer support agent.

Customer name: {customer_name}
Issue reported: {issue}

Respond professionally and empathetically. 
Suggest a solution and create a ticket if needed."""

@mcp.prompt()
def bug_report_template(feature: str, steps: str) -> str:
    """Reusable prompt template for bug reports."""
    return f"""You are a QA engineer writing a bug report.

Feature affected: {feature}
Steps to reproduce: {steps}

Write a clear, structured bug report with:
- Summary
- Steps to reproduce
- Expected vs actual behavior
- Priority suggestion"""

if __name__ == "__main__":
    mcp.run(transport="stdio")