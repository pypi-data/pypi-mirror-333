# MCP Registry

A tool for managing and interacting with multiple MCP servers. It serves two main purposes:

1. **As a CLI Tool**: Manages server configurations and runs a compound server that aggregates multiple servers into one

This is useful when you have multiple MCP clients (Claude Desktop, Cursor, Claude Code (each directory has its own config)) and you want to have a synchronized settings across all of them.
So you can add a new server once and use it across all clients.

2. **As a Library**: Provides a simple way to load and interact with multiple MCP servers directly in your code

The core functionality is very simple, you might want to copy it into your project if you don't want to depend on this package. In fact, the code was derived from [mcp-agent](https://github.com/lastmile-ai/mcp-agent).

## Installation

```bash
pip install mcp-registry
```

## Usage

### 1. As a CLI Tool

Use the command-line interface to manage servers and run them as a compound server: (The syntax follows Claude Code)

```bash
# Initialize config
mcp-registry init

# Add servers
mcp-registry add memory npx -y @modelcontextprotocol/server-memory
mcp-registry add filesystem npx -y @modelcontextprotocol/server-filesystem

# Advanced: Add commands that contain flags
# Method 1: Use -- to separate mcp-registry options from the command's own flags
mcp-registry add myserver -- node server.js --port 3000 --verbose

# Method 2: Use quotes around the command with its arguments
mcp-registry add myserver "npm run server --port 8080"

# Method 3: Use the interactive mode for complex commands
mcp-registry add
# Then enter details when prompted

# List configured servers
mcp-registry list

# Edit configuration directly with your preferred editor
# (validates JSON when saving and keeps a backup)
mcp-registry edit

# Run as a compound server (tools will be available as "server_name__tool_name")
mcp-registry serve

# Run as a compound server with specific servers
mcp-registry serve memory filesystem

# Test it with the inspect tool
npx -y @modelcontextprotocol/inspector mcp-registry serve

# Add this to your client's config file, using claude code as an example:
claude mcp add servers mcp-registry serve

# If you only want certain client to have a few servers, you can add them to the client's config file:
claude mcp add servers mcp-registry serve memory
```

### Configuration

Config file format is the same as Claude Desktop / Claude Code.

```json
{
  "servers": {
    "memory": {
      "type": "stdio", 
      "command": "npx",
      "args": ["-y", "@modelcontextprotocol/server-memory"]
    },
    "remote": {
      "type": "sse",
      "url": "http://localhost:8000/sse"
    }
  }
}
```

#### Connection Management

By default, the MCP Registry creates and destroys connections for each tool call. This is simple and ensures clean resource management, but can be inefficient if you're making multiple calls to the same server, especially for servers with costly initialization.

To optimize performance, you can use persistent connections when using the library (see the library usage section below).

By default, config file is located in `~/.config/mcp_registry/mcp_registry_config.json`:

You can use the environment variable `MCP_REGISTRY_CONFIG` to set a different config file location.
For example, to use Claude Desktop's config file:

```bash
export MCP_REGISTRY_CONFIG=$HOME/'Library/Application Support/Claude/claude_desktop_config.json'
```

You can also use the `mcp-registry show-config-path` command to see the current config file location.


### 2. As a Library

Use MCP Registry in your code to load and interact with multiple servers:

You might want to copy the code into your project if you don't want to depend on this package. In fact, the part of the code was derived from [mcp-agent](https://github.com/lastmile-ai/mcp-agent) by [@lastmile-ai](https://github.com/lastmile-ai).

```python
from mcp_registry import ServerRegistry, MCPAggregator, get_config_path
import asyncio

async def main():
    # Load servers from config (using the current config path)
    registry = ServerRegistry.from_config(get_config_path())

    # Method 1: Temporary connections (default)
    # Each tool call creates and destroys a new connection
    aggregator = MCPAggregator(registry)
    tools = await aggregator.list_tools()
    result = await aggregator.call_tool(
        tool_name="memory__set",  # Format: "server_name__tool_name"
        arguments={"key": "test", "value": "Hello"}
    )
    
    # Method 2: Persistent connections using context manager
    # Maintains connections for the duration of the context
    async with MCPAggregator(registry) as persistent_aggregator:
        # Connections established when entering context
        tools = await persistent_aggregator.list_tools()
        
        # Multiple tool calls use the same connections
        result1 = await persistent_aggregator.call_tool(
            tool_name="memory__set",
            arguments={"key": "test", "value": "Hello"}
        )
        
        result2 = await persistent_aggregator.call_tool(
            tool_name="memory__get",
            arguments={"key": "test"}
        )
        
        # Can also specify server and tool separately
        result3 = await persistent_aggregator.call_tool(
            tool_name="get",
            server_name="memory",
            arguments={"key": "test"}
        )
        # Connections closed automatically when exiting context

asyncio.run(main())
```

For more examples, see the [persistent connections example](examples/persistent_connections_example.py).

For an in-depth explanation of the async connection management patterns used in this project, see [Async Connection Management Patterns](docs/async-connection-management.md).

## Development

```bash
# Install dev dependencies
pip install -e ".[dev]"

# Run tests
pytest

# Format code
ruff format .

# Check code style and lint
ruff check .
```

## License

Apache 2.0