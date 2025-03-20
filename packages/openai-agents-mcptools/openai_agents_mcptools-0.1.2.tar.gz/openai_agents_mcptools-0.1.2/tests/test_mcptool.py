import unittest
from openai_agents_mcptools import MCPTool

class TestMCPTool(unittest.TestCase):
    def setUp(self):
        self.tool = MCPTool('Demo')

    def test_add_tool(self):
        # 测试加法工具
        result = self.tool.call('add', a=5, b=3)
        self.assertEqual(result, 8)

    def test_query_resource(self):
        # 测试 greeting 资源
        result = self.tool.query('greeting://Alice')
        self.assertEqual(result, "Hello, Alice!")

        # 测试另一个名字
        result = self.tool.query('greeting://Bob')
        self.assertEqual(result, "Hello, Bob!")

if __name__ == '__main__':
    unittest.main()