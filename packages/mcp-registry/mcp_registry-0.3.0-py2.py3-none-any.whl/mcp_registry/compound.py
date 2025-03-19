"""
MCP Registry - A simplified MCP server aggregator and compound server implementation.

This module provides tools for managing and aggregating multiple MCP servers,
allowing them to be used either directly or as a compound server.
"""

import asyncio
import json
import sys
from asyncio import gather
from collections.abc import AsyncGenerator
from contextlib import asynccontextmanager
from pathlib import Path

from mcp.client.session import ClientSession
from mcp.client.sse import sse_client
from mcp.client.stdio import (
    StdioServerParameters,
    get_default_environment,
    stdio_client,
)
from mcp.server.lowlevel.server import NotificationOptions, Server
from mcp.server.models import InitializationOptions
from mcp.server.stdio import stdio_server
from mcp.types import (
    CallToolResult,
    GetPromptResult,
    ListToolsResult,
    Prompt,
    ResourceTemplate,
    Tool,
)
from pydantic import BaseModel


class MCPServerSettings(BaseModel):
    """Basic server configuration settings."""

    type: str  # "stdio" or "sse"
    command: str | None = None  # for stdio
    args: list[str] | None = None  # for stdio
    url: str | None = None  # for sse
    env: dict | None = None
    description: str | None = None  # optional description of the server

    @property
    def transport(self) -> str:
        """Alias for type field - represents the transport mechanism (stdio or sse)."""
        return self.type

    @transport.setter
    def transport(self, value: str) -> None:
        """Set the type field through the transport property."""
        self.type = value


class ServerRegistry:
    """Simple registry for managing server configurations."""

    def __init__(self, servers: dict[str, MCPServerSettings]):
        self.registry = servers

    def save_config(self, path: Path | str) -> None:
        """Save the current registry configuration to a file.

        Args:
            path: Path where to save the config file (either string or Path object)

        Raises:
            OSError: If there's an error creating directories or writing the file
        """
        path = Path(path)
        path.parent.mkdir(parents=True, exist_ok=True)

        config = {"mcpServers": {name: settings.model_dump(exclude_none=True) for name, settings in self.registry.items()}}

        with open(path, "w") as f:
            json.dump(config, f, indent=2)

    @classmethod
    def from_config(cls, path: Path | str) -> "ServerRegistry":
        """Create a ServerRegistry from a config file.

        Args:
            path: Path to the config file (either string or Path object)

        Returns:
            A new ServerRegistry instance

        Raises:
            FileNotFoundError: If the config file doesn't exist
            json.JSONDecodeError: If the config file is not valid JSON
            KeyError: If the config file doesn't have the expected structure
        """
        path = Path(path)
        if not path.exists():
            raise FileNotFoundError(f"Config file not found: {path}")

        with open(path) as f:
            config = json.load(f)

        if "mcpServers" not in config:
            raise KeyError("Config file must have a 'mcpServers' section")

        servers = {name: MCPServerSettings(**settings) for name, settings in config["mcpServers"].items()}
        return cls(servers)

    @asynccontextmanager
    async def get_client(self, server_name: str) -> AsyncGenerator[ClientSession, None]:
        """Create a client session for a server."""
        if server_name not in self.registry:
            raise ValueError(f"Server '{server_name}' not found in registry")

        config = self.registry[server_name]

        if config.type == "stdio":
            if not config.command or not config.args:
                raise ValueError(f"Command and args required for stdio type: {server_name}")

            command = config.command

            params = StdioServerParameters(
                command=command,
                args=config.args,
                env={
                    **get_default_environment(),  # includes things like PATH, SHELL, etc.
                    **(config.env or {}),
                },
            )

            async with stdio_client(params) as (read_stream, write_stream):
                session = ClientSession(read_stream, write_stream)
                async with session:
                    await session.initialize()
                    yield session

        elif config.type == "sse":
            if not config.url:
                raise ValueError(f"URL required for SSE type: {server_name}")

            async with sse_client(config.url) as (read_stream, write_stream):
                session = ClientSession(read_stream, write_stream)
                async with session:
                    await session.initialize()
                    yield session
        else:
            raise ValueError(f"Unsupported type: {config.type}")

    def list_servers(self) -> list[str]:
        """List all registered server names."""
        return list(self.registry.keys())

    def get_server_info(self, server_name: str) -> str:
        """Get information about a specific server."""
        if server_name not in self.registry:
            return f"Server '{server_name}' not found"

        config = self.registry[server_name]
        desc = f" - {config.description}" if config.description else ""
        type_info = (
            f"stdio: {config.command} {' '.join(config.args or [])}"
            if config.type == "stdio"
            else f"sse: {config.url}"
        )
        return f"{server_name}: {type_info}{desc}"


class NamespacedTool(BaseModel):
    """A tool that is namespaced by server name."""

    tool: Tool
    server_name: str
    namespaced_tool_name: str


class MCPAggregator:
    """Aggregates multiple MCP servers."""

    def __init__(self, registry: ServerRegistry, server_names: list[str] | None = None):
        """
        Initialize the aggregator.

        Args:
            registry: The server registry to use
            server_names: Optional list of server names to use. If None, uses all registered servers.
        """
        self.registry = registry
        self.server_names = server_names or registry.list_servers()
        self._namespaced_tool_map: dict[str, NamespacedTool] = {}

    async def load_servers(self):
        """Discover tools from each server."""

        async def load_server_tools(server_name: str):
            try:
                async with asyncio.timeout(10):  # 10 second timeout per server
                    async with self.registry.get_client(server_name) as client:
                        result: ListToolsResult = await client.list_tools()
                        return server_name, result.tools or []
            except TimeoutError:
                print(f"Timeout loading tools from {server_name}", file=sys.stderr)
                return server_name, []
            except Exception as e:
                print(f"Error loading tools from {server_name}: {e}", file=sys.stderr)
                return server_name, []

        # Clear existing tools
        self._namespaced_tool_map.clear()

        # Gather tools from all servers concurrently with timeout protection
        results = await gather(
            *(load_server_tools(server_name) for server_name in self.server_names),
            return_exceptions=False,  # We handle exceptions in load_server_tools
        )

        # Build tool map
        for server_name, tools in results:
            for tool in tools:
                namespaced_name = f"{server_name}__{tool.name}"  # Using double underscore
                # Create a copy of the tool with the namespaced name
                namespaced_tool = tool.model_copy(update={"name": namespaced_name})
                # Update the description to include the server name
                namespaced_tool.description = f"[{server_name}] {tool.description}"

                self._namespaced_tool_map[namespaced_name] = NamespacedTool(
                    tool=namespaced_tool, server_name=server_name, namespaced_tool_name=namespaced_name
                )

    async def list_tools(self) -> ListToolsResult:
        """List all available tools."""
        # Always reload tools to ensure we have the latest
        await self.load_servers()
        return ListToolsResult(tools=[tool.tool for tool in self._namespaced_tool_map.values()])

    async def call_tool(
        self,
        tool_name: str,
        arguments: dict | None = None,
        server_name: str | None = None,
    ) -> CallToolResult:
        """Call a tool by name.

        Args:
            tool_name: Name of the tool. Can be either:
                - A tool name (if server_name is provided)
                - A combined name in format "server_name__tool_name"
            arguments: Arguments to pass to the tool
            server_name: Optional server name. If not provided, tool_name must be in format "server_name__tool_name"

        Returns:
            The result of the tool call
        """
        # Always reload tools to ensure we have the latest
        await self.load_servers()

        # Parse server name and actual tool name
        actual_server_name: str
        actual_tool_name: str

        if server_name is not None:
            # Use provided server name and tool name as is
            actual_server_name = server_name
            actual_tool_name = tool_name
        else:
            # Parse from combined format
            if "__" not in tool_name:
                return CallToolResult(
                    isError=True,
                    message=(
                        f"Tool name '{tool_name}' not found - "
                        "when server_name is not provided, tool_name must be in format 'server_name__tool_name'"
                    ),
                    content=[],
                )
            actual_server_name, actual_tool_name = tool_name.split("__", 1)

        # Verify server exists
        if actual_server_name not in self.server_names:
            return CallToolResult(
                isError=True,
                message=f"Server '{actual_server_name}' not found or not enabled",
                content=[],
            )

        try:
            async with self.registry.get_client(actual_server_name) as client:
                return await client.call_tool(name=actual_tool_name, arguments=arguments)
        except Exception as e:
            return CallToolResult(
                isError=True,
                message=f"Error calling tool '{actual_tool_name}' on server '{actual_server_name}': {str(e)}",
                content=[],
            )


async def run_registry_server(registry: ServerRegistry, server_names: list[str] | None = None):
    """Create and run an MCP compound server that aggregates tools from the registry.
    Follows the doc in site-packages/mcp/server/lowlevel/server.py

    Args:
        registry: The ServerRegistry containing server configurations
        server_names: Optional list of server names to use. If None, uses all registered servers.

    Returns:
        A configured Server instance ready to run
    """
    server = Server("MCP Registry Server")
    aggregator = MCPAggregator(registry, server_names)

    @server.list_tools()
    async def handle_list_tools() -> list[Tool]:
        """List all tools from all registered servers."""
        result = await aggregator.list_tools()
        return result.tools

    @server.call_tool()
    async def handle_call_tool(name: str, arguments: dict | None) -> CallToolResult:
        """Route tool calls to the appropriate server."""
        return await aggregator.call_tool(name=name, arguments=arguments)

    @server.list_prompts()
    async def handle_list_prompts() -> list[Prompt]:
        """List available prompts (empty for now)."""
        return []

    @server.get_prompt()
    async def handle_get_prompt(name: str, arguments: dict[str, str] | None) -> GetPromptResult:
        """Handle prompt requests (not implemented)."""
        return GetPromptResult(
            isError=True, message=f"Prompt '{name}' not found - prompts are not supported by the registry server"
        )

    @server.list_resource_templates()
    async def handle_list_resource_templates() -> list[ResourceTemplate]:
        """List available resource templates (empty for now)."""
        return []

    @server.progress_notification()
    async def handle_progress(progress_token: str | int, progress: float, total: float | None) -> None:
        """Handle progress notifications."""
        # For now, we just print progress to stderr
        print(f"Progress {progress:.1f}" + (f"/{total:.1f}" if total else ""), file=sys.stderr)

    async with stdio_server() as (read_stream, write_stream):
        await server.run(
            read_stream=read_stream,
            write_stream=write_stream,
            initialization_options=InitializationOptions(
                server_name=server.name,
                server_version="0.1.0",
                capabilities=server.get_capabilities(
                    notification_options=NotificationOptions(
                        prompts_changed=False, resources_changed=False, tools_changed=True
                    ),
                    experimental_capabilities={},
                ),
            ),
        )


def main():
    """Main entry point for the registry server."""
    # Load registry configuration
    config_dir = Path.home() / ".config" / "mcp_registry"
    config_file = config_dir / "mcp_registry_config.json"

    # Create registry from config
    registry = ServerRegistry.from_config(config_file)
    asyncio.run(run_registry_server(registry))


if __name__ == "__main__":
    main()
