import asyncio
import os
from mcp import ClientSession, StdioServerParameters
from mcp.client.stdio import stdio_client
from dotenv import load_dotenv

load_dotenv("phase7_auth/.env")

API_KEY = os.getenv("MCP_API_KEY")

async def main():
    server = StdioServerParameters(
        command="uv",
        args=["run", "python", "phase7_auth/server.py"]
    )

    async with stdio_client(server) as (read, write):
        async with ClientSession(read, write) as session:
            await session.initialize()

            # public data — no token needed
            print("\n--- Public data (no auth) ---")
            result = await session.call_tool("get_public_data", {})
            print(result.content[0].text)

            # protected data — wrong token
            print("\n--- Protected data (wrong token) ---")
            result = await session.call_tool("get_secret_data", {"token": "wrong-token"})
            print(result.content[0].text)

            # protected data — correct token from env
            print("\n--- Protected data (correct token) ---")
            result = await session.call_tool("get_secret_data", {"token": API_KEY})
            print(result.content[0].text)

asyncio.run(main())