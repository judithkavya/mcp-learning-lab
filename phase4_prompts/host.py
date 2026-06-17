import asyncio
from mcp import ClientSession, StdioServerParameters
from mcp.client.stdio import stdio_client

async def main():
    server = StdioServerParameters(
        command="uv",
        args=["run", "python", "phase4_prompts/server.py"]
    )

    async with stdio_client(server) as (read, write):
        async with ClientSession(read, write) as session:
            await session.initialize()

            # Step 1 — discover tools
            tools = await session.list_tools()
            print("\n--- Tools available ---")
            for tool in tools.tools:
                print(f"  {tool.name}: {tool.description}")

            # Step 2 — discover prompts
            prompts = await session.list_prompts()
            print("\n--- Prompts available ---")
            for prompt in prompts.prompts:
                print(f"  {prompt.name}: {prompt.description}")

            # Step 3 — get a prompt and print it
            print("\n--- Customer Support Prompt ---")
            result = await session.get_prompt("customer_support_template", {
                "customer_name": "Judith",
                "issue": "Cannot login on mobile app"
            })
            print(result.messages[0].content.text)

            # Step 4 — get bug report prompt
            print("\n--- Bug Report Prompt ---")
            result = await session.get_prompt("bug_report_template", {
                "feature": "Login",
                "steps": "1. Open app 2. Enter credentials 3. Tap login 4. Nothing happens"
            })
            print(result.messages[0].content.text)

asyncio.run(main())