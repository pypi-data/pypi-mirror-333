import unittest

from core.pattern.component import HttpToolkit
from core.pattern.component import ApiDefinition
from core.manager.tool.flat_toolkit_manager import FlatToolkitManager


class MyTestCase(unittest.TestCase):
    def test_rpc_toolkit_manager(self):
        api_list = [
            ApiDefinition(url='http://221.229.0.177:9981/v1/models', method='get', name='api1', description='d1', args=[
                {
                    "name": "name",
                    "in": "query",
                    "required": False,
                    "schema": {
                        "type": "string",
                        "title": "模型id",
                        "description": "模型id"
                    },
                    "description": "模型id"
                }
            ]),
            ApiDefinition(url='http://221.229.0.177:9981/chat', method='post', name='api2', description='d2', args={
                "properties": {
                    "model_uid": {
                        "type": "string",
                        "title": "选择模型ID",
                        "description": "选择模型ID"
                    },
                    "q": {
                        "type": "string",
                        "title": "提问",
                        "description": "提问",
                        "default": ""
                    },
                    "prompt": {
                        "type": "string",
                        "title": "提问",
                        "description": "提问",
                        "default": ""
                    },
                    "stream": {
                        "type": "boolean",
                        "title": "stream模式",
                        "description": "stream模式, true or false",
                        "default": False
                    },
                    "history": {
                        "items": {

                        },
                        "type": "array",
                        "title": "历史记录",
                        "description": "历史记录",
                        "default": []
                    },
                    "temperature": {
                        "type": "number",
                        "title": "temperature",
                        "description": "temperature，默认0.2",
                        "default": 0.2
                    },
                    "top_p": {
                        "type": "number",
                        "title": "top_p",
                        "description": "top_p",
                        "default": 0.8
                    }
                },
                "type": "object",
                "required": [
                    "model_uid"
                ],
                "title": "Body_chat_chat_post"
            }),
        ]

        tk = HttpToolkit.create(api_list=api_list, name='tk_test', description='test api tool')

        tk_manager = FlatToolkitManager()
        tk_manager.register(tk)
        _tk = tk_manager.get_toolkit(toolkit_name='tk_test')
        print('######get_toolkit')
        print(_tk)

        tool = tk_manager.get_tool(tool_name='api1')
        print('######get_tool')
        print(tool)

        tool = tk_manager.get_tool(tool_name='api1', toolkit_name='tk_test')
        print('######get_tool')
        print(tool)

        print('######get_tools')
        tools = tk_manager.get_tools()
        print(tools)

        tk_manager.unregister(tk_name_or_obj=_tk)
        _tk = tk_manager.get_toolkit(toolkit_name='tk_test')
        print('######get_toolkit')
        print(_tk)


if __name__ == '__main__':
    unittest.main()
