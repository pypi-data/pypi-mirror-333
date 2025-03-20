import unittest

from langchain_community.chat_models import ChatTongyi

from core.pattern.llm_call.llm_call_graph import LlmCallGraphBase

llm = ChatTongyi(
    model_name='qwen-max-latest',
    api_key='sk-b66bdec7097847f7af9d9fe63797c7c6',
    top_p=0.1,
)

class MyTestCase(unittest.TestCase):
    def test_llm_call(self):
        task = "我是一名工人，每个小时的工资是29.9元。上个月我工作了37个小时，这个月我工作了24.5个小时。上个月我购买了一台车花费了291元，请问我现在剩余多少钱?"
        llm_agent = LlmCallGraphBase.create(llm=llm)

        for s in llm_agent.graph.astream({
            "task": task
        }, stream_mode='values'):
            print("---1")
            print(s)
            print("---2")


if __name__ == '__main__':
    unittest.main()
