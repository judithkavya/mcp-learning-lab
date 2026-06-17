import asyncio
from mcp import ClientSession, StdioServerParameters
from mcp.client.stdio import stdio_client

async def main():
    customer_server = StdioServerParameters(
        command="uv",
        args=["run", "python", "phase5_gateway/server_customer.py"]
    )
    weather_server = StdioServerParameters(
        command="uv",
        args=["run", "python", "phase5_gateway/server_weather.py"]
    )

    # connect to BOTH servers simultaneously
    async with stdio_client(customer_server) as (cr, cw):
        async with ClientSession(cr, cw) as customer_session:
            await customer_session.initialize()

            async with stdio_client(weather_server) as (wr, ww):
                async with ClientSession(wr, ww) as weather_session:
                    await weather_session.initialize()

                    # discover tools from both servers
                    customer_tools = await customer_session.list_tools()
                    weather_tools = await weather_session.list_tools()

                    print("\n--- Customer Server Tools ---")
                    for tool in customer_tools.tools:
                        print(f"  {tool.name}: {tool.description}")

                    print("\n--- Weather Server Tools ---")
                    for tool in weather_tools.tools:
                        print(f"  {tool.name}: {tool.description}")

                    # call tools from different servers
                    print("\n--- Get Customer (from customer server) ---")
                    result = await customer_session.call_tool("get_customer", {"customer_id": "123"})
                    print(result.content[0].text)

                    print("\n--- Get Weather (from weather server) ---")
                    result = await weather_session.call_tool("get_weather", {"city": "bangalore"})
                    print(result.content[0].text)

                    print("\n--- Create Ticket (from customer server) ---")
                    result = await customer_session.call_tool("create_ticket", {
                        "title": "Weather widget broken",
                        "description": "Weather data not loading on dashboard"
                    })
                    print(result.content[0].text)

asyncio.run(main())