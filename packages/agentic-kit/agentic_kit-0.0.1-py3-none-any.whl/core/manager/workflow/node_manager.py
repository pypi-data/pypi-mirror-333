from typing import Any, Union, Sequence

from langchain_core.tools import BaseTool
from langgraph.prebuilt import ToolNode
from langgraph.types import interrupt, Command

from ...base.schema import BaseStateInterrupt
from ...scheduler.scheduler import Scheduler


class NodeManager:
    @classmethod
    def make_interrupt_node(cls, thread_id: str, breakpoint_id: str, next_node: str, scheduler: Scheduler, input: Any = '', **kwargs):
        """
        生成interrupt节点
        input: 断点需要执行操作的上下文
        """
        def interrupt_node(state: BaseStateInterrupt):
            # print("执行到中断节点，等待外部输入...")
            # _breakpoint = BreakpointManager.set_breakpoint(state=state, breakpoint_id=breakpoint_id, input=input)
            # note: 如果断点status == 0
            # if _breakpoint.status == 0:
            #     # note: 挂起时，保存上下文
            #     scheduler.suspend(thread_id=thread_id, breakpoint=_breakpoint)
            #     _breakpoint.data = interrupt(input)
            #
            #     # note: 设置status = 1，下次进入断点则不会重复执行
            #     _breakpoint.status = 1

            return Command(goto=next_node)

        return interrupt_node

    @classmethod
    def make_injectable_tool(cls, tools: Union[BaseTool, Sequence[BaseTool], ToolNode],
                             messages_key: str = 'messages') -> ToolNode:
        """创建一个ToolNode，ToolNode才可以动态注入state到tool中"""
        if isinstance(tools, ToolNode):
            return tools
        elif isinstance(tools, BaseTool):
            return ToolNode([tools], messages_key=messages_key)
        elif isinstance(tools, list):
            return ToolNode(tools, messages_key=messages_key)
        else:
            return ToolNode(tools, messages_key=messages_key)
