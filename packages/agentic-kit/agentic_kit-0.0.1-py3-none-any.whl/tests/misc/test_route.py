import unittest

from langchain_community.chat_models import ChatTongyi

from core.manager.router.utils import route


class MyTestCase(unittest.TestCase):
    def test_cot_plan_execute_graph(self):
        llm = ChatTongyi(
            model_name='qwen-max-latest',
            api_key='sk-b66bdec7097847f7af9d9fe63797c7c6',
            top_p=0.1,
        )
        res = route(llm=llm, query='计算', router_desc='请分类', router_options='计算题,电脑，文化，家居')

if __name__ == '__main__':
    unittest.main()
