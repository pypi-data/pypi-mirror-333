# %%

from mcp_registry import ServerRegistry, MCPAggregator
from mcp_registry.cli import get_default_config_path

# Load the registry using the default config path
registry = ServerRegistry.from_config(get_default_config_path())
aggregator = MCPAggregator(registry)
# List all available tools from all servers
result = await aggregator.list_tools()
# %%
result
# %%
for tool in result.tools:
    if 'exa' in tool.name:
        print(f"{tool.name}: {tool.description}")
        break
tool.inputSchema
"""
{'type': 'object',
 'properties': {'query': {'type': 'string', 'description': 'Search query'},
  'numResults': {'type': 'number',
   'description': 'Number of results to return (default: 10)',
   'minimum': 1,
   'maximum': 50}},
 'required': ['query']}

"""

# %%
# Call a tool (two ways)
# Method 1: Specify tool and server separately
await aggregator.call_tool(
    tool_name="search",
    server_name="exa",
    arguments={"query": "a book about cats"}
)
# %%
# Method 2: Use combined name format: server_name__tool_name
result = await aggregator.call_tool(
    tool_name="exa__search",
    arguments={"query": "a book about cats"},
)
print(result)
# %%
