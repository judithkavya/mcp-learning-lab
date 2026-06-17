from mcp.server.fastmcp import FastMCP

mcp = FastMCP("ticket-server")

# in-memory store to simulate a real DB
tickets = {}
counter = 1

@mcp.tool()
def create_ticket(title: str, description: str, priority: str, customer_id: str) -> dict:
    """Create a support ticket for a customer."""
    global counter
    ticket_id = f"TKT-{counter:03d}"
    tickets[ticket_id] = {
        "id": ticket_id,
        "title": title,
        "description": description,
        "priority": priority,
        "customer_id": customer_id,
        "status": "open"
    }
    counter += 1
    return tickets[ticket_id]

@mcp.tool()
def get_ticket(ticket_id: str) -> dict:
    """Get a ticket by ID."""
    return tickets.get(ticket_id, {"error": "Ticket not found"})

@mcp.tool()
def list_tickets() -> list:
    """List all tickets."""
    return list(tickets.values())

@mcp.tool()
def close_ticket(ticket_id: str) -> dict:
    """Close a ticket."""
    if ticket_id in tickets:
        tickets[ticket_id]["status"] = "closed"
        return tickets[ticket_id]
    return {"error": "Ticket not found"}

if __name__ == "__main__":
    mcp.run(transport="stdio")