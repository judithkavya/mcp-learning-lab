import asyncio
from mcp import ClientSession, StdioServerParameters
from mcp.client.stdio import stdio_client

async def main():
    server = StdioServerParameters(
        command="uv",
        args=["run", "python", "phase3_resources/server.py"]
    )

    async with stdio_client(server) as (read, write):
        async with ClientSession(read, write) as session:
            await session.initialize()

            # Step 1 — discover tools
            tools = await session.list_tools()
            print("\n--- Tools available ---")
            for tool in tools.tools:
                print(f"  {tool.name}: {tool.description}")

            # Step 2 — discover resources
            resources = await session.list_resources()
            print("\n--- Resources available ---")
            for resource in resources.resources:
                print(f"  {resource.uri}: {resource.description}")

            # Step 3 — read a resource
            print("\n--- Reading company policy ---")
            content = await session.read_resource("policy://company")
            print(content.contents[0].text)

            # Step 4 — call a tool
            print("\n--- Creating a ticket ---")
            result = await session.call_tool("create_ticket", {
                "title": "Fix login bug",
                "description": "Users cannot login on mobile"
            })
            print(result.content[0].text)

asyncio.run(main())