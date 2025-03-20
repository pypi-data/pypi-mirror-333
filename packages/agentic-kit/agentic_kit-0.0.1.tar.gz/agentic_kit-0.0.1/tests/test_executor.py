import unittest

from langchain_community.chat_models import ChatTongyi

from core.pattern.component.executor.sequence_executor import SequenceExecutor
from core.pattern.component.planner import SequenceCotPlanner
from scenario.prebuilt.tools.samplas.calculator_add import calculator_add_tool
from scenario.prebuilt.tools.samplas.calculator_multiply import calculator_multiply_tool
from scenario.prebuilt.tools.samplas.calculator_sub import calculator_sub_tool

llm = ChatTongyi(
    model_name='qwen-max-latest',
    api_key='sk-b66bdec7097847f7af9d9fe63797c7c6',
    top_p=0.1,
)

tools = [calculator_add_tool, calculator_sub_tool, calculator_multiply_tool]


class MyTestCase(unittest.TestCase):
    def test_sequence_executor(self):
        task = "我是一名工人，每个小时的工资是29.9元。上个月我工作了37个小时，这个月我工作了24.5个小时。上个月我购买了一台车花费了291元，请问我现在剩余多少钱?"
        planner = SequenceCotPlanner.create(llm=llm, tools=tools)
        result = planner.invoke({
            'task': task
        })
        # print(result)
        for item in result['steps']:
            print(item)
        # print(result['plans'])

        executor = SequenceExecutor.create(llm=llm, tools=tools)
        exe_result = executor.invoke({
            'steps': result['steps']
        })
        print('exe result ============ ')
        for item in exe_result['step_results']:
            print(item)
        print('--------')
        for item in exe_result['results']:
            print(item)
        print('--------')
        for item in exe_result['call_log']:
            print(item)

if __name__ == '__main__':
    unittest.main()
