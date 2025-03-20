from openai_agents import Tool, Agent
from mcp import MCPClient  # 假设这是 MCP 的 Python SDK

class MCPTool(Tool):
    def __init__(self, server_name: str, auth_token: str = None):
        self.client = MCPClient(server_name)
        if auth_token:
            self.client.authenticate(auth_token)

    def query_resource(self, query_params: dict) -> dict:
        try:
            response = self.client.query_resource(query_params)
            return response
        except Exception as e:
            return {"error": str(e)}

    def call_tool(self, tool_name: str, tool_params: dict) -> dict:
        try:
            response = self.client.call_tool(tool_name, tool_params)
            return response
        except Exception as e:
            return {"error": str(e)}

    def get_schema(self):
        return {
            "query_resource": {
                "type": "object",
                "properties": {
                    "query_params": {"type": "object", "description": "资源查询参数"}
                },
                "required": ["query_params"]
            },
            "call_tool": {
                "type": "object",
                "properties": {
                    "tool_name": {"type": "string", "description": "要调用的工具名称"},
                    "tool_params": {"type": "object", "description": "工具参数"}
                },
                "required": ["tool_name", "tool_params"]
            }
        }

