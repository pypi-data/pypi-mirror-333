from typing import Literal

from langchain_core.language_models import BaseChatModel
from langchain_core.prompts import ChatPromptTemplate
from langgraph.constants import END
from langgraph.graph import StateGraph
from langgraph.types import interrupt, Command

from core.base.graph import PatternSingleLlmGraphBase
from utils.parser import parse_json_llm_response
from utils.prompt import check_prompt_required_filed
from .schema import IntentRecognitionState, IntentSchema


class IntentRecognitionGraph(PatternSingleLlmGraphBase):
    default_prompt = '''
    # 你是一个意图信息分析专家，意图识别专家，主要工作是根据用户输入，来识别用户的意图，进行分类分析，提取意图中的词槽关键字信息。 

    # 要求：
    1. 请根据前置信息和和<用户输入>的内容，分析并提取用户的意图信息
    2. 根据<用户输入>，提取能够表现意图的词槽关键字

    # 前置信息和用户补充的信息：
    {ex_info}

    # <用户输入>是：
    {query}

    # 输入信息格式要求：必须满足以下结构，请返回BaseModel格式的信息：
    {intent_schema}

    请开始分析
    '''

    required_field = ['{query}', '{ex_info}', '{intent_schema}']

    default_loop_counter = 1

    def __init__(self, llm: BaseChatModel, prompt_template: ChatPromptTemplate, **kwargs):
        super().__init__(llm=llm, prompt_template=prompt_template, **kwargs)

        self.intent_app = kwargs.get('intent_app')
        self.client_id = kwargs.get('client_id')
        self.checkpointer = kwargs.get('checkpointer')

        self._init_graph()

    # @retry(stop=stop_after_attempt(3), retry_error_callback=intent_retry_failed_callback)
    def _llm_call(self, state: IntentRecognitionState):
        print('########## IntentRecognitionGraph 开始执行 ##########')
        print(state)
        ex_info = state.get('ex_info', '')
        query = state['query']
        print('前置信息是: [%s]' % ex_info)
        print('执行query是: [%s]' % query)

        print('提示词: [%s]' % self.prompt_template)
        response = self.llm_callable.invoke({
            'ex_info': ex_info,
            'query': query,
            'intent_schema': IntentSchema.model_json_schema(),
        })
        # print(response)
        print('########## IntentRecognitionGraph 结束执行 ##########')
        result = parse_json_llm_response(response.content)
        print(result)

        should_finish = True if len(result['lost_slots']) == 0 else False
        print(should_finish)

        return {
            'intent': IntentSchema(**result),
            'should_finish': should_finish,
        }

    def _interrupt_node(self, state: IntentRecognitionState):
        print('######IntentRecognitionGraph 进入')
        print(state)
        lost_slots = ','.join(state['intent'].lost_slots)
        msg = f'请补充以下信息:{lost_slots}'
        self.intent_app.send_message_to_client(client_id=self.client_id, message=msg)
        print('########## IntentRecognitionGraph 中断 ##########')
        ex_info = interrupt(msg)
        print('########## IntentRecognitionGraph 恢复 ##########')
        print(f'已补充：f{ex_info}')
        return {'ex_info': ex_info}

    def _should_continue(self, state: IntentRecognitionState) -> Literal['interrupt_node', END]:
        print('######IntentRecognitionGraph._should_continue 进入')
        if state.get('should_finish', False):
            print('######IntentRecognitionGraph._should_continue to end')
            self.intent_app.send_message_to_client(client_id=self.client_id, message=state['intent'].result)
            return END
        else:
            print('######IntentRecognitionGraph._should_continue to interrupt_node')
            return 'interrupt_node'

    def _init_graph(self):
        """初始化graph： CompiledStateGraph"""
        builder = StateGraph(IntentRecognitionState)
        builder.add_node('llm_call', self._llm_call)
        builder.add_node('interrupt_node', self._interrupt_node)
        builder.add_edge('interrupt_node', 'llm_call')
        builder.add_conditional_edges('llm_call', self._should_continue)
        builder.set_entry_point('llm_call')
        self.graph = builder.compile(checkpointer=self.checkpointer)

    @classmethod
    def create(cls, llm: BaseChatModel, **kwargs):
        prompt = kwargs.get('prompt', cls.default_prompt)
        assert check_prompt_required_filed(prompt=prompt, required_field=cls.required_field) is True
        prompt_template = ChatPromptTemplate.from_messages(
            [
                (
                    "system", kwargs.get('prompt', prompt)
                )
            ]
        )

        agent = cls(llm=llm, prompt_template=prompt_template, **kwargs)
        return agent
