import asyncio
from mcp import ClientSession, StdioServerParameters
from mcp.client.stdio import stdio_client

async def main():
    customer_params = StdioServerParameters(
        command="uv",
        args=["run", "python", "phase6_multi_server/server_customer.py"]
    )
    weather_params = StdioServerParameters(
        command="uv",
        args=["run", "python", "phase6_multi_server/server_weather.py"]
    )
    ticket_params = StdioServerParameters(
        command="uv",
        args=["run", "python", "phase6_multi_server/server_ticket.py"]
    )

    async with stdio_client(customer_params) as (cr, cw):
        async with ClientSession(cr, cw) as customer:
            await customer.initialize()

            async with stdio_client(weather_params) as (wr, ww):
                async with ClientSession(wr, ww) as weather:
                    await weather.initialize()

                    async with stdio_client(ticket_params) as (tr, tw):
                        async with ClientSession(tr, tw) as ticket:
                            await ticket.initialize()

                            # discover all tools from all 3 servers
                            print("\n=== TOOL DISCOVERY ACROSS ALL SERVERS ===")
                            for name, session in [("Customer", customer), ("Weather", weather), ("Ticket", ticket)]:
                                tools = await session.list_tools()
                                print(f"\n{name} Server tools:")
                                for tool in tools.tools:
                                    print(f"  {tool.name}: {tool.description}")

                            # simulate a real workflow
                            # 1. get customer
                            print("\n=== WORKFLOW ===")
                            print("\n1. Get customer 123")
                            result = await customer.call_tool("get_customer", {"customer_id": "123"})
                            print(result.content[0].text)

                            # 2. check weather for their city
                            print("\n2. Check weather in Bangalore")
                            result = await weather.call_tool("get_weather", {"city": "bangalore"})
                            print(result.content[0].text)

                            # 3. create a ticket for them
                            print("\n3. Create ticket for customer 123")
                            result = await ticket.call_tool("create_ticket", {
                                "title": "Login issue on mobile",
                                "description": "Cannot login after app update",
                                "priority": "high",
                                "customer_id": "123"
                            })
                            print(result.content[0].text)

                            # 4. list all tickets
                            print("\n4. List all tickets")
                            result = await ticket.call_tool("list_tickets", {})
                            print(result.content[0].text)

                            # 5. close the ticket
                            print("\n5. Close ticket TKT-001")
                            result = await ticket.call_tool("close_ticket", {"ticket_id": "TKT-001"})
                            print(result.content[0].text)

asyncio.run(main())