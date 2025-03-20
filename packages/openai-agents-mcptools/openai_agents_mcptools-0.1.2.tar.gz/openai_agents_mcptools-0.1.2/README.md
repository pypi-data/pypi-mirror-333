安装方法：pip install mcptool。

使用示例：
from openai_agents import Agent

# 创建 MCPTool 实例
mcp_tool = MCPTool(server_name="database_server", auth_token="your_auth_token")

# 创建代理并注册工具
agent = Agent(tools=[mcp_tool])

# 为代理设置指令
agent.set_instructions(
    "如果用户请求数据库中的数据，使用 MCPTool 的 query_resource 方法；"
    "如果用户需要执行特定操作，使用 MCPTool 的 call_tool 方法。"
)



运行测试：
安装 pip install mcp

python -m unittest discover


