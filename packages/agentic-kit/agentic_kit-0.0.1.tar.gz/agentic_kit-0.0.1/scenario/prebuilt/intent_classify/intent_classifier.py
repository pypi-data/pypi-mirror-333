from langchain_core.language_models import BaseChatModel
from langchain_core.prompts import ChatPromptTemplate
from tenacity import retry, stop_after_attempt

from core.pattern.llm_call import LlmCallGraphBase
from utils.parser import parse_json_llm_response
from .base import intent_retry_failed_callback
from .retriver import IntentRetrieverBase
from .schema import IntentClassifyState


class IntentClassifierGraph(LlmCallGraphBase):
    default_prompt = '''
    # 你是一个意图分类专家，意图识别专家，主要工作是根据用户输入，来识别用户的意图，进行分类。 

    # 要求：
    1. 请根据前置信息和意图类型，判断<用户输入>的内容，属于哪个意图类型
    2. 只从可选择的意图类型中选择意图返回，不要扩展额外内容。
    3. 返回1个或多个意图
    4. 根据<用户输入>，提取能够表现意图的关键字
    
    # 前置信息：
    {ex_info}
    
    # 可选择的<意图类型>
    {intent_options}
    
    # <用户输入>是：
    {query}
    
    # 输出json结构，必须包含字段：
        'intent': 意图，
        'intent_keywords': 能够表现意图的关键字的list
        
    # 举例：
    
    请开始分析
    '''

    required_field = ['{query}', '{ex_info}', '{intent_options}']

    default_loop_counter = 1

    state_cls = IntentClassifyState

    intent_retriever: IntentRetrieverBase

    def __init__(self, llm: BaseChatModel, prompt_template: ChatPromptTemplate, intent_retriever: IntentRetrieverBase, **kwargs):
        super().__init__(llm=llm, prompt_template=prompt_template, **kwargs)

        assert intent_retriever is not None
        self.intent_retriever = intent_retriever
        self._init_graph()

    @retry(stop=stop_after_attempt(3), retry_error_callback=intent_retry_failed_callback)
    def _llm_call(self, state: IntentClassifyState):
        print('########## IntentClassifierGraph 开始执行 ##########')
        print(state)
        ex_info = state.get('ex_info', '')
        query = state['query']
        print('前置信息是: [%s]' % ex_info)
        print('执行query是: [%s]' % query)

        response = self.llm_callable.invoke({
            'ex_info': ex_info,
            'query': query,
            'intent_options': self.intent_retriever.get_intent_options(query),
        })
        # print(response)
        print('########## IntentClassifierGraph 结束执行 ##########')
        result = parse_json_llm_response(response.content)

        intent = result.get('intent', '')
        intent_keywords = result.get('intent_keywords', [])
        intent_entity = self.intent_retriever.retrieve(query=query, intent=intent, intent_keywords=intent_keywords)

        return {
            'intent': intent,
            'intent_entity': intent_entity,
            'should_finish': True
        }
