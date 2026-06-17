import asyncio
from mcp import ClientSession, StdioServerParameters
from mcp.client.stdio import stdio_client

async def main():
    server = StdioServerParameters(
        command="uv",
        args=["run", "python", "phase2_tools/server.py"]
    )

    async with stdio_client(server) as (read, write):
        async with ClientSession(read, write) as session:
            await session.initialize()

            # Step 1 — discover all tools
            tools = await session.list_tools()
            print("\n--- Tools available ---")
            for tool in tools.tools:
                print(f"  {tool.name}: {tool.description}")

            # Step 2 — call get_customer
            print("\n--- Get Customer ---")
            result = await session.call_tool("get_customer", {"customer_id": "123"})
            print(result.content[0].text)

            # Step 3 — call create_ticket
            print("\n--- Create Ticket ---")
            result = await session.call_tool("create_ticket", {
                "title": "Login bug",
                "description": "Users cannot login on mobile"
            })
            print(result.content[0].text)

            # Step 4 — call get_weather
            print("\n--- Get Weather ---")
            result = await session.call_tool("get_weather", {"city": "bangalore"})
            print(result.content[0].text)

asyncio.run(main())