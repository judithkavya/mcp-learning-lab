"""
Phase 10 — Google Calendar MCP Host
Connects Ollama (llama3.2) to the Google Calendar MCP server via stdio.
"""

import asyncio
import json
import ollama

from mcp import ClientSession, StdioServerParameters
from mcp.client.stdio import stdio_client


# ── Config ───────────────────────────────────────────────────────────────────

SERVER_PARAMS = StdioServerParameters(
    command="uv",
    args=["run", "python", "server.py"],
)

OLLAMA_MODEL = "llama3.2"

SYSTEM_PROMPT = """You are a helpful calendar assistant with access to the user's Google Calendar.

You have these tools available:
- list_events: List events in a date range (use YYYY-MM-DD for dates)
- create_event: Create a new event (use ISO format for datetimes e.g. 2025-07-15T10:00:00)
- update_event: Update an existing event by event_id
- delete_event: Delete an event by event_id

When the user asks about their schedule, always use list_events first to check what exists.
When creating events, confirm the details back to the user after creation.
Today's date context: use it to interpret relative dates like "tomorrow" or "next Monday".
"""


# ── Tool call handler ─────────────────────────────────────────────────────────

async def call_tool(session: ClientSession, tool_name: str, tool_args: dict) -> str:
    """Execute a tool via MCP and return the result as a string."""
    print(f"\n  [tool call] {tool_name}({json.dumps(tool_args, indent=2)})")
    result = await session.call_tool(tool_name, tool_args)
    output = result.content[0].text if result.content else "No result returned."
    print(f"  [tool result] {output[:300]}{'...' if len(output) > 300 else ''}")
    return output


# ── Main agent loop ───────────────────────────────────────────────────────────

async def run():
    async with stdio_client(SERVER_PARAMS) as (read, write):
        async with ClientSession(read, write) as session:
            await session.initialize()

            # Discover tools from the server
            tools_result = await session.list_tools()
            tools = tools_result.tools
            print(f"Connected to Google Calendar MCP server.")
            print(f"Available tools: {[t.name for t in tools]}\n")

            # Convert MCP tool schemas to Ollama tool format
            ollama_tools = []
            for tool in tools:
                schema = tool.inputSchema or {}
                # Remove additionalProperties — Ollama doesn't support it
                schema.pop("additionalProperties", None)
                ollama_tools.append({
                    "type": "function",
                    "function": {
                        "name": tool.name,
                        "description": tool.description or "",
                        "parameters": schema,
                    },
                })

            # Conversation history
            messages = [{"role": "system", "content": SYSTEM_PROMPT}]

            print("Google Calendar Assistant ready. Type 'quit' to exit.\n")
            print("-" * 50)

            while True:
                user_input = input("\nYou: ").strip()
                if user_input.lower() in ("quit", "exit", "q"):
                    print("Goodbye!")
                    break
                if not user_input:
                    continue

                messages.append({"role": "user", "content": user_input})

                # Agentic loop — keep going until no more tool calls
                while True:
                    response = ollama.chat(
                        model=OLLAMA_MODEL,
                        messages=messages,
                        tools=ollama_tools,
                    )

                    assistant_msg = response["message"]
                    tool_calls = assistant_msg.get("tool_calls") or []

                    if not tool_calls:
                        # Final text response — print and break inner loop
                        print(f"\nAssistant: {assistant_msg['content']}")
                        messages.append({
                            "role": "assistant",
                            "content": assistant_msg["content"],
                        })
                        break

                    # Process each tool call
                    messages.append({
                        "role": "assistant",
                        "content": assistant_msg.get("content", ""),
                        "tool_calls": tool_calls,
                    })

                    for tc in tool_calls:
                        fn = tc["function"]
                        tool_name = fn["name"]
                        tool_args = fn.get("arguments", {})

                        tool_result = await call_tool(session, tool_name, tool_args)

                        messages.append({
                            "role": "tool",
                            "content": tool_result,
                        })


# ── Entry point ───────────────────────────────────────────────────────────────

if __name__ == "__main__":
    asyncio.run(run())