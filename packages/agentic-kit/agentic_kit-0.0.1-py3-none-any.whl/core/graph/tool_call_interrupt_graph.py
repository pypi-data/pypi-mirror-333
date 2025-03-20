import asyncio
import copy
from typing import List, Any, Dict

from langchain_core.language_models import BaseChatModel
from langchain_core.messages import AIMessage, ToolCall, ToolMessage
from langchain_core.prompts import ChatPromptTemplate
from langchain_core.tools import BaseTool
from langgraph.checkpoint.memory import MemorySaver
from langgraph.constants import END
from langgraph.graph import StateGraph
from langgraph.types import interrupt, Command

from core.base.schema import Breakpoint
from core.pattern.tool_use.schema import ToolCallWithBreakpointState
from core.pattern.tool_use.tool_call_graph import ToolCallGraphBase
from utils.tools import get_tools_desc_for_prompt_zh, find_tool_by_name


# TODO: 如何处理state传递


class ToolCallInterruptGraph(ToolCallGraphBase):
    """interruptible tool call"""

    default_prompt = \
        '''
        # 你是一个工具tool调用助手，通过给出的工具tool调用提示，来调用对应的用具。
        # 调用提示中可能包含一些前置信息或其他工具tool的调用结果，在类似<#E>这样的字段中，表示前置信息或其他工具tool的调用结果。
    
        ## 前置信息或其他工具tool的调用结果是：{ex_info}
    
        # 当前的工具tool调用任务是: {task}，请分析任务，如果包含的多个任务，请分别返回没个任务对应的工具调用
    
        可供调用的工具tool和详细参数结构、描述，分别是：{tools},
    
        # 生成规则：
        1.请使用正确的参数调用工具tool，严格遵守匹配工具tool的参数类型，
        2.可以选择多个最适合的工具tool来完成任务
        3.如果没有合适的工具tool，就不要返回任何信息
        4.请忽略上次调用的任何信息，重新生成回答
        '''

    breakpoints: list[Breakpoint]
    '''断点'''

    def _check_is_interrupt(self):
        """检测当前是否有中断"""
        is_interrupt = False
        for bk in self.breakpoints:
            if bk.status == 0:  # note: 0表示断点执行中
                is_interrupt = True
                break
        return is_interrupt

    def _finish_breakpoint(self, tool_call_id: str, tool_call_response: Any):
        for bk in self.breakpoints:
            if tool_call_id  == bk.id:
                # note: 设置断点的结果
                bk.resume(result=tool_call_response)
                self.tool_call_response_queue.put_nowait(tool_call_response)
                self.graph.update_state(self.thread_config, {'breakpoints': self.breakpoints})
                break

    def _on_tool_call(self, selected_tool: BaseTool, tool_call: ToolCall, task: Any):
        raise NotImplemented

    def tool_call(self, state: ToolCallWithBreakpointState):
        print('########## ToolCallInterruptGraph 开始执行调用tools ##########')
        tools_desc = get_tools_desc_for_prompt_zh(self.tools)
        ex_info = state.get('ex_info', '')
        task = state['task']
        print('上一步执行结果是: [%s]' % ex_info)
        print('执行task是: [%s]' % task)
        print('可供调用的是: %s' % tools_desc)

        response = self.llm_callable_with_tools.invoke({
            'ex_info': ex_info,
            'task': task,
            'tools': tools_desc,
        })

        if isinstance(response, AIMessage) and response.tool_calls:
            print(f'准备调用tool calls: [{len(response.tool_calls)}]个tool call')
            for tool_call in response.tool_calls:
                print(f'执行调用: {tool_call}')
                selected_tool = find_tool_by_name(tool_name=tool_call['name'], tools=self.tools)
                if selected_tool is None:
                    print(f'执行调用失败，找不到tool: {tool_call}')
                    continue
                res = self._on_tool_call(selected_tool=selected_tool, tool_call=tool_call, task=task)

        # return {'call_log': [response]}

    def tool_call_interrupt(self, state):
        """tool call interrupt node"""
        print('@@@@@@@@@检测中断等待输入--------')
        is_interrupt = self._check_is_interrupt()
        if is_interrupt:
            print('@@@@@@@@@中断等待输入--------')
            result = interrupt(state['task'])
            print('@@@@@@@@@获得中断数据: %s' % result)
            return {'results': [result]}
        else:
            print('@@@@@@@@@无中断等待--------')
            if len(self.breakpoints) > 0:
                result = self.breakpoints[-1].result
                return {'results': [result]}

    async def astream(self, initial_state: Dict[str, Any], config: dict = None, stream_mode: str = "updates"):
        """
        Stream the graph execution with interrupt handling.
        """
        self.breakpoints = []
        self.initial_state = initial_state
        self.stream_mode = stream_mode
        if config is None:
            self.thread_id = initial_state['thread_id']
            self.thread_config = {"configurable": {"thread_id": initial_state['thread_id']}}
        else:
            self.thread_config = config

        # Initial run to capture interrupt
        async for event in self.graph.astream(initial_state, self.thread_config, stream_mode=stream_mode):
            print('=================1')
            print(event)
            yield event

        while self._check_is_interrupt():
            # note: 如果有中断，等待消息队列返回中断结果
            interrupt_resp = await self.tool_call_response_queue.get()
            async for resume_event in self.graph.astream(Command(resume=interrupt_resp), self.thread_config, stream_mode=self.stream_mode):
                print('=================2')
                print(event)
                yield resume_event
        print('==================== ok')

    def _init_graph(self):
        """初始化graph： CompiledStateGraph"""
        builder = StateGraph(ToolCallWithBreakpointState)
        builder.add_node('tool_call', self.tool_call)
        builder.add_node('tool_call_interrupt', self.tool_call_interrupt)
        builder.add_edge('tool_call', 'tool_call_interrupt')
        builder.add_edge('tool_call_interrupt', END)
        builder.set_entry_point('tool_call')
        self.graph = builder.compile(checkpointer=self.checkpointer)

    def __init__(
        self,
        llm: BaseChatModel,
        tools: List,
        prompt_template: ChatPromptTemplate,
        **kwargs
    ):
        checkpointer = kwargs.get('checkpointer', None)
        if checkpointer is None:
            checkpointer = MemorySaver()
        self.checkpointer = checkpointer

        super().__init__(llm=llm, tools=tools, prompt_template=prompt_template, **kwargs)

        self.tool_call_response_queue = asyncio.Queue()  # 用于存储中断调用信息
