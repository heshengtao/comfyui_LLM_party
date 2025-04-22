import json
import asyncio
import locale
import os
from typing import Dict, List, Any
from mcp import ClientSession, StdioServerParameters
from mcp.client.stdio import stdio_client
import json
from typing import Any, Dict, List, Tuple
import nest_asyncio
import shutil

def get_command_path(command_name, default_command='python'):
    """Find the full path of a command on the system PATH."""
    command_path = shutil.which(command_name)
    if command_path is None:
        print(f"Command '{command_name}' not found in PATH. Using default: {default_command}")
        command_path = shutil.which(default_command)
        if command_path is None:
            raise FileNotFoundError(f"Neither '{command_name}' nor '{default_command}' were found in PATH.")
    return command_path

# 当前脚本目录的上级目录
current_dir = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
config_path = os.path.join(current_dir, "config.ini")
mcp_config_path = os.path.join(current_dir, "mcp_config.json")
nest_asyncio.apply()
class McpClient:
    def __init__(self, config_path: str = mcp_config_path):
        self.config_path = config_path
        self.servers = {}  # Store server sessions
        self.all_tools = {}  # Store tool information
        self.is_initialized = False
        
    def load_mcp_servers_from_config(self) -> List[tuple]:
        with open(self.config_path, 'r') as f:
            config = json.load(f)
        
        servers = []
        for server_name, server_config in config.get('mcpServers', {}).items():
            command = server_config.get('command', 'python')
            server_params = StdioServerParameters(
                command = get_command_path(command),
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
        self.is_initialized = True
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

mcp_client = McpClient()
class Mcp_tool:
    def __init__(self):
        global mcp_client
        self.client = mcp_client
    @classmethod
    def INPUT_TYPES(s):
        return {
            "required": {
                "is_enable": ("BOOLEAN", {"default": True}),
            },
        }

    RETURN_TYPES = ("STRING",)
    RETURN_NAMES = ("tool",)

    FUNCTION = "Mcp_call"

    CATEGORY = "大模型派对（llm_party）/工具（tools）/自动化（Automation）"


    def Mcp_call(self, is_enable=True):
        if not is_enable:
            return (None,)
        
        async def run_client():
            
            try:
                # 如果已经初始化，则跳过
                if self.client.is_initialized is False:
                    await self.client.initialize()

                # Get OpenAI functions
                functions = await self.client.get_openai_functions()
                output = functions
            except Exception as e:
                output = str(e)
                print(f"An error occurred: {e}")
            out = json.dumps(output, ensure_ascii=False)
            return (out,)
        
        # Run the async function using asyncio.run
        try:
            result = asyncio.run(run_client())
            return result
        except asyncio.CancelledError:
            print("The entire async execution was cancelled")
            return ("The async execution was cancelled",)
        except Exception as e:
            print(f"An error occurred during async execution: {e}")
            return (str(e),)

NODE_CLASS_MAPPINGS = {
    "Mcp_tool": Mcp_tool,
}
lang = locale.getlocale()[0]
if 'Chinese' in lang:
   lang = 'zh_CN'
else:
   lang = 'en_US'
import configparser
config = configparser.ConfigParser()
config.read(config_path)
try:
    language = config.get("API_KEYS", "language")
except:
    language = ""
if language == "zh_CN" or language=="en_US":
    lang=language
if lang == "zh_CN":
    NODE_DISPLAY_NAME_MAPPINGS = {
        "Mcp_tool": "MCP工具"
    }
else:
    NODE_DISPLAY_NAME_MAPPINGS = {
        "Mcp_tool": "MCP tool"
    }