import unittest

from core.tools.base import RpcToolDefinition
from core.pattern.component import WsSession
from core.tools.rpc.ws.ws_toolkit import WebsocketToolkit


class MyTestCase(unittest.TestCase):
    def test_ws_tool(self):
        tool_list = [
            RpcToolDefinition(name='api1', description='d1', args=[
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
            RpcToolDefinition(name='api2', description='d2', args={
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

        fake_session = WsSession(connection=None, id='1234', connection_metadata={})

        tk = WebsocketToolkit.create(tool_def_list=tool_list, name='ws tool', description='test ws tool', session=fake_session)
        tk.dump()

        # t1 = tk.get_tools()[0]
        # print('------')
        # print(t1.name)
        # res = t1.invoke({
        # })
        # print(res)
        # print(type(res))

        # t2 = tk.get_tools()[1]
        # print('------')
        # print(t2.name)
        # res = t2.invoke({
        #     'model_uid': 'deepseek-chat^deepseek-chat^396@deepseek^18',
        #     'q': '你好',
        # })
        # print(res)
        # print(type(res))


if __name__ == '__main__':
    unittest.main()
