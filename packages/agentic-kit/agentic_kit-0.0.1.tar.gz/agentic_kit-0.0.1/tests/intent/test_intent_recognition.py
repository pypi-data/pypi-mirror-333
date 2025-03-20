import unittest
import uuid

from langchain_community.chat_models import ChatTongyi

from scenario.prebuilt.agent.intent.intent_recognition.intent_recognition_agent import IntentRecognitionGraph
from scenario.prebuilt.intent_classify.intent_classifier import IntentClassifierGraph
from scenario.prebuilt.intent_classify.retriver import FlatIntentRetriever

llm = ChatTongyi(
    model_name='qwen-max-latest',
    api_key='sk-b66bdec7097847f7af9d9fe63797c7c6',
    top_p=0.1,
)


class MyTestCase(unittest.TestCase):
    def test_intent_recognition(self):
        # query = "我弹奏了一首钢琴曲，内容是abc格式，如下: xxyyddaaa，帮我评价一下能够得多少分，然后根据我弹奏的内容再帮我续写一个钢琴曲，23秒，悲伤风格"
        # query = "请帮我订一张火车票"
        query = "请帮我订一张火车票，从北京到常州，时间是3月10号"

        llm_agent = IntentRecognitionGraph.create(llm=llm)

        res = llm_agent.callable.astream({
            "thread_id": str(uuid.uuid4()),
            "query": query,
            'loop_counter': 1
        }, stream_mode='updates', config={})
        print(res)

if __name__ == '__main__':
    unittest.main()
