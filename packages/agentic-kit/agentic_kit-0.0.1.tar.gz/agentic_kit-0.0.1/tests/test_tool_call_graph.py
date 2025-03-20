import unittest

from langchain_community.chat_models import ChatTongyi

from core.pattern.tool_use.tool_call_graph import ToolCallMultiTasksGraph, ToolCallSingleTaskGraph
from core.tool.rpc.http import ApiDef, HttpToolkit
from scenario.prebuilt.tools.samplas.calculator_add import calculator_add_tool
from scenario.prebuilt.tools.samplas.calculator_sub import calculator_sub_tool

llm = ChatTongyi(
    model_name='qwen-max-latest',
    api_key='sk-b66bdec7097847f7af9d9fe63797c7c6',
    top_p=0.1,
)

api_list = [
    ApiDef(url='http://221.229.0.177:9981/ping', method='get', name='ping',
                  description='测试api服务是否正常', args=[
        ]),
    ApiDef(url='http://221.229.0.177:9981/v1/models', method='get', name='v1_models',
                  description='查询所有可以支持的模型列表', args=[
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
    ApiDef(url='http://221.229.0.177:9981/v1/models/{model}', method='get', name='v1_models_detail',
                  description='通过模型ID查询某个模型的详细信息', args=[
            {
                "name": "model",
                "in": "path",
                "required": True,
                "schema": {
                    "type": "string",
                    "title": "模型id",
                    "description": "模型id"
                },
                "description": "模型id"
            }
        ]),
    ApiDef(url='http://221.229.0.177:9981/chat', method='post', name='llm_chat',
                  description='通过大模型调用来回答问题', args={
            "properties": {
                "model_uid": {
                    "type": "string",
                    "title": "选择模型id",
                    "description": "选择模型id，默认选择deepseek-chat^deepseek-chat^396@deepseek^18"
                },
                "q": {
                    "type": "string",
                    "title": "提问的问题描述",
                    "description": "提问的问题描述",
                    "default": ""
                },
                "prompt": {
                    "type": "string",
                    "title": "前置提示词",
                    "description": "前置提示词",
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
                    "description": "temperature",
                    "default": 0.130
                },
                "top_p": {
                    "type": "number",
                    "title": "top_p",
                    "description": "top_p",
                    "default": 0.111
                }
            },
            "type": "object",
            "required": [
                "model_uid"
            ]
        }),
]

tk = HttpToolkit.create(
    api_list=api_list,
    name='test tk',
    description='test tk'
)
tools = [calculator_add_tool, calculator_sub_tool, *tk.get_tools()]


class MyTestCase(unittest.TestCase):
    def test_tool_call_graph_single_task(self):
        tool_call_graph = ToolCallSingleTaskGraph.create(llm=llm, tools=[calculator_add_tool, calculator_sub_tool])
        res = tool_call_graph.graph.invoke({
            # 'task': '帮我通过api问答回答我的问题，请问"你是谁"',
            # 'task': '如果正常帮我通过api问答回答我的问题，使用的模型是："qwen-max^qwen-max^377@shubiaobiao^15"，请问"你是谁"',
            # 'task': '请帮我查看一下目前都支持哪些模型调用？',
            # 'task': '请查询一下"claude-3-opus^claude-3-opus^413@online^15"这个模型的详细信息？'
            # 'task': '请测试一下api服务是否正常'
            'task': '请计算100+200=?'
        })
        print('dump res --------')
        print(res)

        self.assertEqual(True, True)  # add assertion here

    def test_tool_call_graph_multi_tasks(self):
        tool_call_graph = ToolCallMultiTasksGraph.create(llm=llm, tools=tools)
        res = tool_call_graph.invoke({
            'task': [
                '请计算1+2=?',
                '5-3等于几？'
            ],
        })
        print('dump res --------')
        print(res)

        self.assertEqual(True, True)  # add assertion here


if __name__ == '__main__':
    unittest.main()
