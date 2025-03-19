"""MCP Registry - A simplified MCP server aggregator and compound server implementation."""

from .compound import (
    MCPAggregator,
    MCPServerSettings,
    ServerRegistry,
    run_registry_server,
)

__version__ = "0.1.0"
__all__ = [
    "MCPServerSettings",
    "ServerRegistry",
    "MCPAggregator",
    "run_registry_server",
]
