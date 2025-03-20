import asyncio
import json
import sys
import logging
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
    EmbeddedResource,
    GetPromptResult,
    ImageContent,
    ListToolsResult,
    Prompt,
    ResourceTemplate,
    TextContent,
    Tool,
)
from pydantic import BaseModel

# Set up logging for debugging purposes.
logger = logging.getLogger(__name__)
logging.basicConfig(level=logging.INFO)


class MCPServerSettings(BaseModel):
    """
    Basic server configuration settings.
    """
    type: str  # "stdio" or "sse"
    command: str | None = None  # for stdio
    args: list[str] | None = None  # for stdio
    url: str | None = None  # for sse
    env: dict | None = None
    description: str | None = None

    @property
    def transport(self) -> str:
        return self.type

    @transport.setter
    def transport(self, value: str) -> None:
        self.type = value


class ServerRegistry:
    """
    Simple registry for managing server configurations.
    """
    def __init__(self, servers: dict[str, MCPServerSettings]):
        self.registry = servers

    def save_config(self, path: Path | str) -> None:
        path = Path(path)
        path.parent.mkdir(parents=True, exist_ok=True)
        config = {
            "mcpServers": {
                name: settings.model_dump(exclude_none=True)
                for name, settings in self.registry.items()
            }
        }
        with open(path, "w") as f:
            json.dump(config, f, indent=2)

    @classmethod
    def from_config(cls, path: Path | str) -> "ServerRegistry":
        path = Path(path)
        if not path.exists():
            raise FileNotFoundError(f"Config file not found: {path}")
        with open(path) as f:
            config = json.load(f)
        if "mcpServers" not in config:
            raise KeyError("Config file must have a 'mcpServers' section")
        servers = {
            name: MCPServerSettings(**settings)
            for name, settings in config["mcpServers"].items()
        }
        return cls(servers)

    @asynccontextmanager
    async def get_client(self, server_name: str) -> AsyncGenerator[ClientSession, None]:
        if server_name not in self.registry:
            raise ValueError(f"Server '{server_name}' not found in registry")
        config = self.registry[server_name]
        if config.type == "stdio":
            if not config.command or not config.args:
                raise ValueError(f"Command and args required for stdio type: {server_name}")
            params = StdioServerParameters(
                command=config.command,
                args=config.args,
                env={**get_default_environment(), **(config.env or {})},
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
        return list(self.registry.keys())

    def get_server_info(self, server_name: str) -> str:
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
    """
    A tool that is namespaced by server name.
    """
    tool: Tool
    server_name: str
    namespaced_tool_name: str


class MCPAggregator:
    """
    Aggregates multiple MCP servers.
    """
    def __init__(self, registry: ServerRegistry, server_names: list[str] | None = None):
        self.registry = registry
        self.server_names = server_names or registry.list_servers()
        self._namespaced_tool_map: dict[str, NamespacedTool] = {}

    async def load_servers(self):
        """
        Discover and namespace tools from each sub-server.
        """
        logger.info(f"Loading tools from servers: {self.server_names}")
        self._namespaced_tool_map.clear()

        async def load_server_tools(server_name: str):
            try:
                async with asyncio.timeout(10):
                    async with self.registry.get_client(server_name) as client:
                        result: ListToolsResult = await client.list_tools()
                        tools = result.tools or []
                        logger.info(f"Loaded {len(tools)} tools from {server_name}")
                        return server_name, tools
            except Exception as e:
                logger.error(f"Error loading tools from {server_name}: {e}")
                return server_name, []

        results = await gather(*(load_server_tools(name) for name in self.server_names))
        for server_name, tools in results:
            for tool in tools:
                namespaced_name = f"{server_name}__{tool.name}"
                namespaced_tool = tool.model_copy(update={"name": namespaced_name})
                namespaced_tool.description = f"[{server_name}] {tool.description or ''}"
                self._namespaced_tool_map[namespaced_name] = NamespacedTool(
                    tool=namespaced_tool,
                    server_name=server_name,
                    namespaced_tool_name=namespaced_name,
                )

    async def list_tools(self) -> ListToolsResult:
        """
        List all available tools from all sub-servers.
        """
        await self.load_servers()
        tools = [nt.tool for nt in self._namespaced_tool_map.values()]
        return ListToolsResult(tools=tools)

    async def call_tool(
        self,
        tool_name: str,
        arguments: dict | None = None,
        server_name: str | None = None,
    ) -> CallToolResult:
        """
        Call a tool by its namespaced name.
        """
        await self.load_servers()
        # Determine server and tool names from parameters or the namespaced string.
        if server_name:
            actual_server = server_name
            actual_tool = tool_name
        else:
            if "__" not in tool_name:
                err_msg = (
                    f"Tool name '{tool_name}' must be namespaced as 'server__tool'"
                )
                return CallToolResult(
                    isError=True,
                    message=err_msg,
                    content=[TextContent(type="text", text=err_msg)],
                )
            actual_server, actual_tool = tool_name.split("__", 1)

        if actual_server not in self.server_names:
            err_msg = f"Server '{actual_server}' not found or not enabled"
            return CallToolResult(
                isError=True,
                message=err_msg,
                content=[TextContent(type="text", text=err_msg)],
            )

        try:
            async with self.registry.get_client(actual_server) as client:
                try:
                    async with asyncio.timeout(30):
                        result = await client.call_tool(actual_tool, arguments)
                except asyncio.TimeoutError:
                    err_msg = (
                        f"Timeout calling tool '{actual_tool}' on server '{actual_server}'"
                    )
                    return CallToolResult(
                        isError=True,
                        message=err_msg,
                        content=[TextContent(type="text", text=err_msg)],
                    )
                except Exception as e:
                    err_msg = (
                        f"Error calling tool '{actual_tool}' on server '{actual_server}': {e}"
                    )
                    logger.error(err_msg)
                    return CallToolResult(
                        isError=True,
                        message=err_msg,
                        content=[TextContent(type="text", text=err_msg)],
                    )

                # If the call returns an error result, propagate it.
                if getattr(result, "isError", False):
                    err_msg = f"Server '{actual_server}' returned error: {getattr(result, 'message', '')}"
                    return CallToolResult(
                        isError=True,
                        message=err_msg,
                        content=[TextContent(type="text", text=err_msg)],
                    )

                # Process returned content into a proper list of content objects.
                content = []
                extracted = None
                if hasattr(result, "content"):
                    extracted = result.content
                elif isinstance(result, dict) and "content" in result:
                    extracted = result["content"]
                elif hasattr(result, "result"):
                    extracted = [result.result]
                elif isinstance(result, dict) and "result" in result:
                    extracted = [result["result"]]

                if extracted:
                    for item in extracted:
                        if isinstance(item, (TextContent, ImageContent, EmbeddedResource)):
                            content.append(item)
                        elif isinstance(item, dict) and "text" in item and "type" in item:
                            content.append(TextContent(**item))
                        elif isinstance(item, str):
                            content.append(TextContent(type="text", text=item))
                        else:
                            content.append(TextContent(type="text", text=str(item)))
                if not content:
                    content = [TextContent(type="text", text="Tool execution completed.")]
                return CallToolResult(isError=False, message="", content=content)
        except Exception as e:
            err_msg = f"Error in call_tool for '{tool_name}': {e}"
            logger.error(err_msg)
            return CallToolResult(
                isError=True,
                message=err_msg,
                content=[TextContent(type="text", text=err_msg)],
            )


async def run_registry_server(registry: ServerRegistry, server_names: list[str] | None = None):
    """
    Create and run an MCP compound server that aggregates tools from the registry.
    """
    server = Server("MCP Registry Server")
    aggregator = MCPAggregator(registry, server_names)

    @server.list_tools()
    async def handle_list_tools() -> list[Tool]:
        result = await aggregator.list_tools()
        return result.tools

    @server.call_tool()
    async def handle_call_tool(name: str, arguments: dict | None) -> list[TextContent | ImageContent | EmbeddedResource]:
        try:
            result = await aggregator.call_tool(name, arguments)
            if getattr(result, "isError", False):
                raise Exception(getattr(result, "message", "Unknown error"))
            if hasattr(result, "content") and result.content:
                return result.content
            elif hasattr(result, "result"):
                return [TextContent(type="text", text=str(result.result))]
            else:
                return [TextContent(type="text", text="Tool execution completed.")]
        except Exception as e:
            err_msg = f"Error routing tool call for '{name}': {e}"
            logger.error(err_msg)
            return [TextContent(type="text", text=err_msg)]

    @server.list_prompts()
    async def handle_list_prompts() -> list[Prompt]:
        return []

    @server.get_prompt()
    async def handle_get_prompt(name: str, arguments: dict[str, str] | None) -> GetPromptResult:
        return GetPromptResult(
            isError=True,
            message=f"Prompt '{name}' not found - prompts are not supported by the registry server"
        )

    @server.list_resource_templates()
    async def handle_list_resource_templates() -> list[ResourceTemplate]:
        return []

    @server.progress_notification()
    async def handle_progress(progress_token: str | int, progress: float, total: float | None) -> None:
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
                        prompts_changed=False,
                        resources_changed=False,
                        tools_changed=True,
                    ),
                    experimental_capabilities={},
                ),
            ),
        )


def main():
    config_dir = Path.home() / ".config" / "mcp_registry"
    config_file = config_dir / "mcp_registry_config.json"
    registry = ServerRegistry.from_config(config_file)
    asyncio.run(run_registry_server(registry))


if __name__ == "__main__":
    main()
"""
MCP Registry - A simplified MCP server aggregator and compound server implementation.

This module provides tools for managing and aggregating multiple MCP servers,
allowing them to be used either directly or as a compound server.
"""

import asyncio
import json
import sys
import logging
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
    EmbeddedResource,
    GetPromptResult,
    ImageContent,
    ListToolsResult,
    Prompt,
    ResourceTemplate,
    TextContent,
    Tool,
)
from pydantic import BaseModel

logger = logging.getLogger(__name__)
logging.basicConfig(level=logging.INFO)


class MCPServerSettings(BaseModel):
    """
    Basic server configuration settings.
    """
    type: str  # "stdio" or "sse"
    command: str | None = None  # for stdio
    args: list[str] | None = None  # for stdio
    url: str | None = None  # for sse
    env: dict | None = None
    description: str | None = None

    @property
    def transport(self) -> str:
        return self.type

    @transport.setter
    def transport(self, value: str) -> None:
        self.type = value


class ServerRegistry:
    """
    Simple registry for managing server configurations.
    """
    def __init__(self, servers: dict[str, MCPServerSettings]):
        self.registry = servers

    def save_config(self, path: Path | str) -> None:
        """
        Save the current registry configuration to a file.
        """
        path = Path(path)
        path.parent.mkdir(parents=True, exist_ok=True)
        config = {
            "mcpServers": {
                name: settings.model_dump(exclude_none=True)
                for name, settings in self.registry.items()
            }
        }
        with open(path, "w") as f:
            json.dump(config, f, indent=2)

    @classmethod
    def from_config(cls, path: Path | str) -> "ServerRegistry":
        """
        Create a ServerRegistry from a config file.
        """
        path = Path(path)
        if not path.exists():
            raise FileNotFoundError(f"Config file not found: {path}")
        with open(path) as f:
            config = json.load(f)
        if "mcpServers" not in config:
            raise KeyError("Config file must have a 'mcpServers' section")
        servers = {
            name: MCPServerSettings(**settings)
            for name, settings in config["mcpServers"].items()
        }
        return cls(servers)

    @asynccontextmanager
    async def get_client(self, server_name: str) -> AsyncGenerator[ClientSession, None]:
        """
        Create a client session for a given server.
        """
        if server_name not in self.registry:
            raise ValueError(f"Server '{server_name}' not found in registry")
        config = self.registry[server_name]
        if config.type == "stdio":
            if not config.command or not config.args:
                raise ValueError(f"Command and args required for stdio type: {server_name}")
            params = StdioServerParameters(
                command=config.command,
                args=config.args,
                env={**get_default_environment(), **(config.env or {})},
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
        """
        List all registered server names.
        """
        return list(self.registry.keys())

    def get_server_info(self, server_name: str) -> str:
        """
        Get information about a specific server.
        """
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
    """
    A tool that is namespaced by server name.
    """
    tool: Tool
    server_name: str
    namespaced_tool_name: str


class MCPAggregator:
    """
    Aggregates multiple MCP servers.
    """
    def __init__(self, registry: ServerRegistry, server_names: list[str] | None = None):
        """
        Initialize the aggregator.

        Args:
            registry: The server registry to use.
            server_names: Optional list of server names to use. If None, uses all registered servers.
        """
        self.registry = registry
        self.server_names = server_names or registry.list_servers()
        self._namespaced_tool_map: dict[str, NamespacedTool] = {}

    async def load_servers(self):
        """
        Discover and namespace tools from each sub-server.
        """
        logger.info(f"Loading tools from servers: {self.server_names}")
        self._namespaced_tool_map.clear()

        async def load_server_tools(server_name: str):
            try:
                async with asyncio.timeout(10):
                    async with self.registry.get_client(server_name) as client:
                        result: ListToolsResult = await client.list_tools()
                        tools = result.tools or []
                        logger.info(f"Loaded {len(tools)} tools from {server_name}")
                        return server_name, tools
            except Exception as e:
                logger.error(f"Error loading tools from {server_name}: {e}")
                return server_name, []

        results = await gather(*(load_server_tools(name) for name in self.server_names))
        for server_name, tools in results:
            for tool in tools:
                namespaced_name = f"{server_name}__{tool.name}"
                namespaced_tool = tool.model_copy(update={"name": namespaced_name})
                namespaced_tool.description = f"[{server_name}] {tool.description or ''}"
                self._namespaced_tool_map[namespaced_name] = NamespacedTool(
                    tool=namespaced_tool,
                    server_name=server_name,
                    namespaced_tool_name=namespaced_name,
                )

    async def list_tools(self) -> ListToolsResult:
        """
        List all available tools from all sub-servers.
        """
        await self.load_servers()
        tools = [nt.tool for nt in self._namespaced_tool_map.values()]
        return ListToolsResult(tools=tools)

    async def call_tool(
        self,
        tool_name: str,
        arguments: dict | None = None,
        server_name: str | None = None,
    ) -> CallToolResult:
        """
        Call a tool by its namespaced name.

        Args:
            tool_name: The tool name (either provided fully namespaced or with a separate server_name).
            arguments: The arguments to pass to the tool.
            server_name: Optional server name if tool_name is not namespaced.
        """
        await self.load_servers()
        if server_name:
            actual_server = server_name
            actual_tool = tool_name
        else:
            if "__" not in tool_name:
                err_msg = (
                    f"Tool name '{tool_name}' must be namespaced as 'server__tool'"
                )
                return CallToolResult(
                    isError=True,
                    message=err_msg,
                    content=[TextContent(type="text", text=err_msg)],
                )
            actual_server, actual_tool = tool_name.split("__", 1)

        if actual_server not in self.server_names:
            err_msg = f"Server '{actual_server}' not found or not enabled"
            return CallToolResult(
                isError=True,
                message=err_msg,
                content=[TextContent(type="text", text=err_msg)],
            )

        try:
            async with self.registry.get_client(actual_server) as client:
                try:
                    async with asyncio.timeout(30):
                        result = await client.call_tool(actual_tool, arguments)
                except asyncio.TimeoutError:
                    err_msg = (
                        f"Timeout calling tool '{actual_tool}' on server '{actual_server}'"
                    )
                    return CallToolResult(
                        isError=True,
                        message=err_msg,
                        content=[TextContent(type="text", text=err_msg)],
                    )
                except Exception as e:
                    err_msg = (
                        f"Error calling tool '{actual_tool}' on server '{actual_server}': {e}"
                    )
                    logger.error(err_msg)
                    return CallToolResult(
                        isError=True,
                        message=err_msg,
                        content=[TextContent(type="text", text=err_msg)],
                    )

                if getattr(result, "isError", False):
                    err_msg = f"Server '{actual_server}' returned error: {getattr(result, 'message', '')}"
                    return CallToolResult(
                        isError=True,
                        message=err_msg,
                        content=[TextContent(type="text", text=err_msg)],
                    )

                content = []
                extracted = None
                if hasattr(result, "content"):
                    extracted = result.content
                elif isinstance(result, dict) and "content" in result:
                    extracted = result["content"]
                elif hasattr(result, "result"):
                    extracted = [result.result]
                elif isinstance(result, dict) and "result" in result:
                    extracted = [result["result"]]

                if extracted:
                    for item in extracted:
                        if isinstance(item, (TextContent, ImageContent, EmbeddedResource)):
                            content.append(item)
                        elif isinstance(item, dict) and "text" in item and "type" in item:
                            content.append(TextContent(**item))
                        elif isinstance(item, str):
                            content.append(TextContent(type="text", text=item))
                        else:
                            content.append(TextContent(type="text", text=str(item)))
                if not content:
                    content = [TextContent(type="text", text="Tool execution completed.")]
                return CallToolResult(isError=False, message="", content=content)
        except Exception as e:
            err_msg = f"Error in call_tool for '{tool_name}': {e}"
            logger.error(err_msg)
            return CallToolResult(
                isError=True,
                message=err_msg,
                content=[TextContent(type="text", text=err_msg)],
            )


async def run_registry_server(registry: ServerRegistry, server_names: list[str] | None = None):
    """
    Create and run an MCP compound server that aggregates tools from the registry.
    """
    server = Server("MCP Registry Server")
    aggregator = MCPAggregator(registry, server_names)

    @server.list_tools()
    async def handle_list_tools() -> list[Tool]:
        result = await aggregator.list_tools()
        return result.tools

    @server.call_tool()
    async def handle_call_tool(name: str, arguments: dict | None) -> list[TextContent | ImageContent | EmbeddedResource]:
        try:
            result = await aggregator.call_tool(name, arguments)
            if getattr(result, "isError", False):
                raise Exception(getattr(result, "message", "Unknown error"))
            if hasattr(result, "content") and result.content:
                return result.content
            elif hasattr(result, "result"):
                return [TextContent(type="text", text=str(result.result))]
            else:
                return [TextContent(type="text", text="Tool execution completed.")]
        except Exception as e:
            err_msg = f"Error routing tool call for '{name}': {e}"
            logger.error(err_msg)
            return [TextContent(type="text", text=err_msg)]

    @server.list_prompts()
    async def handle_list_prompts() -> list[Prompt]:
        return []

    @server.get_prompt()
    async def handle_get_prompt(name: str, arguments: dict[str, str] | None) -> GetPromptResult:
        return GetPromptResult(
            isError=True,
            message=f"Prompt '{name}' not found - prompts are not supported by the registry server"
        )

    @server.list_resource_templates()
    async def handle_list_resource_templates() -> list[ResourceTemplate]:
        return []

    @server.progress_notification()
    async def handle_progress(progress_token: str | int, progress: float, total: float | None) -> None:
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
                        prompts_changed=False,
                        resources_changed=False,
                        tools_changed=True,
                    ),
                    experimental_capabilities={},
                ),
            ),
        )


def main():
    config_dir = Path.home() / ".config" / "mcp_registry"
    config_file = config_dir / "mcp_registry_config.json"
    registry = ServerRegistry.from_config(config_file)
    asyncio.run(run_registry_server(registry))


if __name__ == "__main__":
    main()
