import json
import asyncio
from typing import Dict, List, Any
from mcp import ClientSession, StdioServerParameters
from mcp.client.stdio import stdio_client

class McpClient:
    def __init__(self, config_path: str = 'mcp_config.json'):
        self.config_path = config_path
        self.servers = {}  # Store server sessions
        self.all_tools = {}  # Store tool information
        
    def load_mcp_servers_from_config(self) -> List[tuple]:
        with open(self.config_path, 'r') as f:
            config = json.load(f)
        
        servers = []
        for server_name, server_config in config.get('mcpServers', {}).items():
            server_params = StdioServerParameters(
                command=server_config.get('command', 'python'),
                args=server_config.get('args', []),
                env=server_config.get('env', None)
            )
            servers.append((server_name, server_params))
        
        return servers

    @staticmethod
    def _convert_to_openai_functions(tools: Dict) -> List[Dict]:
        functions = []
        for tool_name, tool_details in tools.items():
            function = {
                "type": "function",
                "function": {
                    "name": tool_name,  # Using prefixed name (server-toolname)
                    "description": tool_details['description'],
                    "parameters": tool_details['input_schema']
                }
            }
            functions.append(function)
        return functions

    async def initialize(self):
        """Initialize connections to all MCP servers"""
        servers = self.load_mcp_servers_from_config()
        
        for server_name, server_params in servers:
            # Create client and session
            client = stdio_client(server_params)
            read, write = await client.__aenter__()
            session = ClientSession(read, write)
            await session.__aenter__()
            
            # Store session
            self.servers[server_name] = {
                'client': client,
                'session': session
            }
            
            # Initialize the connection
            await session.initialize()
            
            # Get tools for this server
            server_tools = await session.list_tools()
            
            # Store tools with server prefix
            if hasattr(server_tools, 'tools'):
                for tool in server_tools.tools:
                    prefixed_tool_name = f"{server_name}-{tool.name}"
                    self.all_tools[prefixed_tool_name] = {
                        'description': tool.description,
                        'input_schema': tool.inputSchema,
                        'server': server_name,
                        'name': tool.name
                    }

    async def get_openai_functions(self) -> List[Dict]:
        """Get OpenAI-compatible function descriptions"""
        return self._convert_to_openai_functions(self.all_tools)

    async def call_tool(self, tool_name: str, tool_params: Dict[str, Any]) -> Any:
        """Call a tool using server-toolname format"""
        if tool_name not in self.all_tools:
            raise ValueError(f"Unknown tool: {tool_name}")
        
        tool_info = self.all_tools[tool_name]
        server_name = tool_info['server']
        
        if server_name not in self.servers:
            raise ValueError(f"Server not connected: {server_name}")
        
        session = self.servers[server_name]['session']
        return await session.call_tool(tool_info['name'], arguments=tool_params)

    async def close(self):
        """Close all server connections"""
        for server_info in self.servers.values():
            await server_info['session'].__aexit__(None, None, None)
            await server_info['client'].__aexit__(None, None, None)

async def main():
    # Example usage
    client = McpClient()
    try:
        # Initialize connections
        await client.initialize()
        
        # Get OpenAI functions
        functions = await client.get_openai_functions()
        print("\nAvailable OpenAI Functions:")
        print(json.dumps(functions, indent=2))
        
        # Example tool call (uncomment and modify as needed)
        result = await client.call_tool("everything-add", {"a":1231,"b":464646})
        print("\nTool Result:", result)
        
    finally:
        # Clean up
        await client.close()

if __name__ == "__main__":
    asyncio.run(main())
