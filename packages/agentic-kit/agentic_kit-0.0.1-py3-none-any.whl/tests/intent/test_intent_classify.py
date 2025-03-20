import unittest

from langchain_community.chat_models import ChatTongyi

from scenario.prebuilt.intent_classify.intent_classifier import IntentClassifierGraph
from scenario.prebuilt.intent_classify.retriver import FlatIntentRetriever

llm = ChatTongyi(
    model_name='qwen-max-latest',
    api_key='sk-b66bdec7097847f7af9d9fe63797c7c6',
    top_p=0.1,
)

intent_options = [
            '1^天气相关', '2^购物相关', '3^数学计算问题', '4^其他', '5^音乐测评', '6^音乐创作生成'
        ]

class MyTestCase(unittest.TestCase):
    def test_flat_intent_classify(self):
        # query = "我是一名工人，每个小时的工资是29.9元。上个月我工作了37个小时，这个月我工作了24.5个小时。上个月我购买了一台车花费了291元，请问我现在剩余多少钱?"
        # query = "怎么弹钢琴"
        # query = "怎么学习计算机编程"
        query = "我弹奏了一首钢琴曲，内容是abc格式，如下: xxyyddaaa，帮我评价一下能够得多少分，然后根据我弹奏的内容再帮我续写一个钢琴曲，23秒，悲伤风格"

        llm_agent = IntentClassifierGraph.create(llm=llm, intent_retriever=FlatIntentRetriever(intent_options=intent_options))

        res = llm_agent.callable.invoke({
            "query": query,
            'intent_options': intent_options
        })
        print(res)

if __name__ == '__main__':
    unittest.main()
