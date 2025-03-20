import unittest

from langchain_community.chat_models import ChatTongyi

from core.pattern.react import simple_react_agent
from scenario.prebuilt.tools.remote.http.http_toolkit import HttpToolkit, ApiDefinition
from scenario.prebuilt.tools.samplas.calculator_add import calculator_add_tool
from scenario.prebuilt.tools.samplas.calculator_sub import calculator_sub_tool

llm = ChatTongyi(
    model_name='qwen-max-latest',
    api_key='sk-b66bdec7097847f7af9d9fe63797c7c6',
    top_p=0.1,
)

api_list = [
    ApiDefinition(url='http://221.229.0.177:9981/chat', method='post', name='llm_chat',
                  description='通过大模型[model_uid="deepseek-chat^deepseek-chat^396@deepseek^18"]调用来回答问题', args={
            "model_uid": {
                "type": "string",
                "title": "选择模型id",
                "description": "选择模型id，如果没有提供model_uid，请使用'deepseek-chat^deepseek-chat^396@deepseek^18'"
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
            },
            "type": "object",
            "required": [
                "model_uid", "如果没有提供model_uid，请使用'deepseek-chat^deepseek-chat^396@deepseek^18'"
            ]
        }),
]

tk = HttpToolkit(
    allow_dangerous_requests=True,
    api_list=api_list,
)
tools = [calculator_add_tool, calculator_sub_tool, *tk.get_tools()]


class MyTestCase(unittest.TestCase):
    def test_react_agent(self):
        agent = simple_react_agent(model=llm, tools=tools, debug=True, state_modifier='请全部通过tool调用来解决问题')
        result = agent.invoke({
            # 'messages': ["中国的人口数量加上20亿等于多少?"]
            'messages': ["2010年斯诺克英锦赛的冠军是哪个国家的人?"]
        })
        print(result)


if __name__ == '__main__':
    unittest.main()
