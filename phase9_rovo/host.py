import asyncio
import os
import base64
import json
import httpx
import ollama
from mcp.client.streamable_http import streamable_http_client
from mcp import ClientSession
from dotenv import load_dotenv

load_dotenv("phase9_rovo/.env")

JIRA_EMAIL     = os.getenv("JIRA_EMAIL")
JIRA_API_TOKEN = os.getenv("JIRA_API_TOKEN")
JIRA_PROJECT   = os.getenv("JIRA_DEFAULT_PROJECT")

ROVO_MCP_URL = "https://mcp.atlassian.com/v1/mcp"

credentials = base64.b64encode(f"{JIRA_EMAIL}:{JIRA_API_TOKEN}".encode()).decode()
headers = {"Authorization": f"Basic {credentials}"}

def convert_tools_for_ollama(tools):
    """Convert MCP tools to Ollama function format."""
    result = []
    for tool in tools:
        schema = dict(tool.inputSchema) if tool.inputSchema else {}
        schema.pop("additionalProperties", None)
        result.append({
            "type": "function",
            "function": {
                "name": tool.name,
                "description": tool.description,
                "parameters": schema
            }
        })
    return result

async def main():
    print("Connecting to Atlassian MCP server...")

    async with streamable_http_client(
        ROVO_MCP_URL,
        http_client=httpx.AsyncClient(headers=headers)
    ) as (read, write, _):
        async with ClientSession(read, write) as session:
            await session.initialize()

            # step 1 — discover tools
            print("\n--- Tools from Atlassian MCP ---")
            tools_result = await session.list_tools()
            tools = tools_result.tools
            for tool in tools[:10]:
                print(f"  {tool.name}: {tool.description[:80]}")
            print(f"  ... {len(tools)} tools total")

            # step 2 — convert tools for Ollama
            ollama_tools = convert_tools_for_ollama(tools)

            # step 3 — chat loop
            print("\n--- Chat (type 'exit' to quit) ---")
            messages = [
                {
                    "role": "system",
                    "content": f"You are a helpful assistant with access to Jira. Default project is {JIRA_PROJECT}. Use tools to answer requests."
                }
            ]

            while True:
                user_input = input("\nYou: ").strip()
                if user_input.lower() == "exit":
                    break

                messages.append({"role": "user", "content": user_input})

                response = ollama.chat(
                    model="llama3.2",
                    messages=messages,
                    tools=ollama_tools
                )

                # step 4 — handle tool calls
                while response.message.tool_calls:
                    tool_results = []

                    for tool_call in response.message.tool_calls:
                        tool_name = tool_call.function.name
                        tool_args = dict(tool_call.function.arguments)

                        print(f"\n  → Calling tool: {tool_name}")
                        print(f"    Args: {json.dumps(tool_args, indent=2)}")

                        mcp_result = await session.call_tool(tool_name, tool_args)
                        result_text = mcp_result.content[0].text
                        print(f"    Result: {result_text[:200]}")

                        tool_results.append({
                            "role": "tool",
                            "content": result_text
                        })

                    messages.append(response.message)
                    messages.extend(tool_results)

                    response = ollama.chat(
                        model="llama3.2",
                        messages=messages,
                        tools=ollama_tools
                    )

                # step 5 — print final response
                final = response.message.content or ""
                messages.append({"role": "assistant", "content": final})
                print(f"\nAssistant: {final}")

asyncio.run(main())