"""Example usage of MCP Registry."""

import asyncio
from pathlib import Path

from mcp_registry import MCPAggregator, ServerRegistry, run_registry_server


async def example_direct_interaction():
    """Example of directly interacting with servers."""
    # Load registry from config
    config_path = Path.home() / ".config" / "mcp_registry" / "mcp_registry_config.json"
    registry = ServerRegistry.from_config(config_path)

    # Create an aggregator to interact with servers
    aggregator = MCPAggregator(registry)

    # List all available tools
    print("\nAvailable tools:")
    result = await aggregator.list_tools()
    for tool in result.tools:
        print(f"  {tool.name}: {tool.description}")

    # Example: Use the memory server if available
    try:
        # Method 1: Using separate server name
        await aggregator.call_tool(
            tool_name="set", server_name="memory", arguments={"key": "greeting", "value": "Hello from MCP Registry!"}
        )

        # Method 2: Using combined name
        result = await aggregator.call_tool(
            tool_name="memory__get",  # Format: server_name__tool_name
            arguments={"key": "greeting"},
        )
        print(f"\nRetrieved value: {result.result}")

    except Exception as e:
        print(f"Error interacting with memory server: {e}")


async def example_compound_server():
    """Example of running as a compound server.

    When running as a compound server, tools will be available with the format:
    server_name__tool_name (e.g., memory__set, filesystem__read)
    """
    # Load registry from config
    config_path = Path.home() / ".config" / "mcp_registry" / "mcp_registry_config.json"
    registry = ServerRegistry.from_config(config_path)

    print("\nStarting compound server with the following servers:")
    for name in registry.list_servers():
        print(registry.get_server_info(name))

    # Run the registry server
    await run_registry_server(registry)


if __name__ == "__main__":
    # Choose which example to run
    USE_COMPOUND_SERVER = False  # Set to True to run as compound server

    if USE_COMPOUND_SERVER:
        asyncio.run(example_compound_server())
    else:
        asyncio.run(example_direct_interaction())
