# Persistent Connections Feature

This branch implements persistent connections for MCP Registry to improve performance when making multiple tool calls.

## Overview

The standard behavior in MCP Registry creates and destroys connections for each tool call. While this is simple and ensures clean resource management, it can be inefficient when making multiple calls to the same server, especially for servers with expensive initialization.

This feature adds support for persistent connections using the context manager pattern, allowing connections to be maintained across multiple tool calls.

## Changes

1. **New Connection Management System**
   - Added `MCPConnectionManager` to manage persistent connections
   - Added `ServerConnection` to represent individual server connections
   - Added `ConnectionState` enum to track connection states

2. **Context Manager Support**
   - Modified `MCPAggregator` to support the async context manager pattern
   - Implemented `__aenter__` and `__aexit__` methods

3. **Optimizations**
   - Improved temporary connection mode to only load specific servers
   - Added selective tool caching

4. **Documentation**
   - Added detailed documentation on async connection patterns
   - Updated README with examples of both connection modes
   - Created example script demonstrating both approaches

## How It Works

### Temporary Connections (Default)

```python
# Default behavior - temporary connections
aggregator = MCPAggregator(registry)
result = await aggregator.call_tool("memory__get", {"key": "test"})
```

This creates a new connection for each tool call, optimized to only load the specific server needed.

### Persistent Connections

```python
# Persistent connections with context manager
async with MCPAggregator(registry) as aggregator:
    # Connections established when entering context
    result1 = await aggregator.call_tool("memory__get", {"key": "test"})
    result2 = await aggregator.call_tool("memory__set", {"key": "test2", "value": "hello"})
    # Connections closed automatically when exiting context
```

This maintains connections for the duration of the context, significantly improving performance for multiple calls.

## Implementation Notes

- **Backward Compatibility**: Original behavior with temporary connections is preserved
- **Error Handling**: Robust error handling for connection failures
- **Resource Management**: Proper cleanup of resources when context is exited
- **Concurrency**: Thread-safe using asyncio locks
- **Fallback**: Persistent connections fall back to temporary when needed

## Examples

See [examples/persistent_connections_example.py](examples/persistent_connections_example.py) for a detailed example demonstrating both connection modes.

## Documentation

For an in-depth explanation of the async connection management patterns used, see [docs/async-connection-management.md](docs/async-connection-management.md).