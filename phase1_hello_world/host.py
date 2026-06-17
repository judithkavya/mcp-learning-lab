import asyncio
from mcp import ClientSession, StdioServerParameters
from mcp.client.stdio import stdio_client

async def main():
    server = StdioServerParameters(
        command="uv",
        args=["run", "python", "phase1_hello_world/server.py"]
    )

    async with stdio_client(server) as (read, write):
        async with ClientSession(read, write) as session:
            await session.initialize()

            # Step 1 — discover tools
            tools = await session.list_tools()
            print("\n--- Tools available ---")
            for tool in tools.tools:
                print(f"  {tool.name}: {tool.description}")

            # Step 2 — call the tool
            result = await session.call_tool("hello_world", {"name": "Judith"})
            print("\n--- Result ---")
            print(result.content[0].text)

asyncio.run(main())