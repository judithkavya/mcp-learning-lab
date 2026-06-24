import asyncio
from mcp.client.streamable_http import streamable_http_client
from mcp import ClientSession

SERVER_URL = "http://127.0.0.1:8000/mcp"

async def main():
    async with streamable_http_client(SERVER_URL) as (read, write, _):
        async with ClientSession(read, write) as session:
            await session.initialize()

            print("\n--- Tools available ---")
            tools = await session.list_tools()
            for tool in tools.tools:
                print(f"  {tool.name}: {tool.description}")

            print("\n--- Get Customer ---")
            result = await session.call_tool("get_customer", {"customer_id": "123"})
            print(result.content[0].text)

            print("\n--- Create Ticket ---")
            result = await session.call_tool("create_ticket", {
                "title": "Login bug",
                "description": "Cannot login on mobile",
                "priority": "high"
            })
            print(result.content[0].text)

            print("\n--- Read Resource ---")
            content = await session.read_resource("docs://readme")
            print(content.contents[0].text)

asyncio.run(main())