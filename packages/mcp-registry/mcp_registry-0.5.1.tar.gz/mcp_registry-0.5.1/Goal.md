read the codebase. 

I want to make mcp-registry a cli tool.

it should support the same config file format as claude desktop
so on first invocation
first it should check if there's existing claude desktop config and if user want to copy from it as a starting point

Mac: ~/Library/Application Support/Claude/claude_desktop_config.json
Windows: %APPDATA%\Claude\claude_desktop_config.json
------

then copy it to some appropriate place like ~/.config/claude_registry/claude_registry_config.json

based on this format. it should support commands that let's you add / remove mcp server in the registry using Claude Code's syntax


mcp-registry add mcp-server-name command args 
mcp-registry remove mcp-server-name
mcp-registry list

-----------

this is just a registry feature

I want it to be a thin wrapper for aggegrating multiple servers 

like suppose user have the following servers registered : memory, github, weather, filesystem

and user wants to expose a few select servers to a mcp client
instead of registring all the select servers again to the client,
user should be able to run

mcp-registry serve memory filesystem

to launch these 2 with a single command, and aggegrate / expose all the tools of these servers

------

besides this quality of life features, mcp-registry should also expose the core logic as library for client developers to build apps that talks to mcp servers individually without using MCPCompoundServer
