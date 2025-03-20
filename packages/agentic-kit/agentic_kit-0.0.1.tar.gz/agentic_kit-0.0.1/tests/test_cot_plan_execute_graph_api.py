import unittest

from langchain_community.chat_models import ChatTongyi

from core.pattern.plan_execute import CotPlanExecuteGraph
from core.tool.rpc.http import ApiDef, HttpToolkit


class MyTestCase(unittest.TestCase):
    def test_cot_plan_execute_graph_api(self):
        llm = ChatTongyi(
            model_name='qwen-max-latest',
            api_key='sk-b66bdec7097847f7af9d9fe63797c7c6',
            top_p=0.1,
        )

        api_list = [
            ApiDef(url='http://221.229.0.177:9981/ping', method='get', name='ping', is_async=False,
                          description='测试api服务是否正常', args=[
                ]),
            ApiDef(url='http://221.229.0.177:9981/v1/models', method='get', name='v1_models',
                          description='查询所有可以支持的模型列表', is_async=False, args=[
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
                          description='通过模型ID查询某个模型的详细信息', is_async=False, args=[
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
                          description='通过大模型调用来回答问题', is_async=False, args={
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
            name='api tool',
            description='test api tool'
        )
        tools = tk.get_tools()

        # tool = [calculator_add_tool, calculator_sub_tool, calculator_multiply_tool]
        # tool = [abc_music_tool, eval_tool]

        pe_graph = CotPlanExecuteGraph.create(llm=llm, tools=tools)
        task = "请问api是通路是否可用？如果可用的话帮我通过api问答回答我的问题，请问\"你是谁\""

        print('########## 通过CotPlanExecuteGraph执行任务 ##########')
        print(task)
        print('\n\n\n')
        res = pe_graph.graph.invoke({
            "task": task,
        })
        print(f"通过CotPlanExecuteGraph获得最终结果: \n{task}\n{res['final_result']}")

        # for s in g.graph.stream({
        #     "task": task,
        # }, stream_mode='updates'):
        #     print("---1")
        #     print(s)
        #     print("---2")


if __name__ == '__main__':
    unittest.main()
