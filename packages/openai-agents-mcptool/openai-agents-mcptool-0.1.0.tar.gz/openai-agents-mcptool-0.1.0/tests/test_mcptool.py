import unittest
from mcptool import MCPTool

class TestMCPTool(unittest.TestCase):
    def test_query_resource(self):
        tool = MCPTool('server_name')
        # 添加测试逻辑
        self.assertTrue(True)  # 示例断言

if __name__ == '__main__':
    unittest.main()