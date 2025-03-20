import json
from typing import List, Any
from typing import Union

from langchain_core.language_models import BaseChatModel
from langchain_core.messages import ToolCall, ToolMessage
from langchain_core.prompts import ChatPromptTemplate
from langchain_core.tools import BaseTool, StructuredTool

from core.base.schema import Breakpoint
from infrastructure.event_driven.pub_sub.redis_pubsub_manager import tool_call_subscriber
from infrastructure.event_driven.pub_sub.redis_subscriber import RedisSubscriberHandler
from utils.prompt import check_prompt_required_filed
from .tool_call_interrupt_graph import ToolCallInterruptGraph
from ..tool.rpc.http.base import HttpTool


class ToolCallAsyncInterruptGraph(ToolCallInterruptGraph, RedisSubscriberHandler):
    """interruptible local&http tool call"""

    def on_subscribed(self, data: Union[str, dict]):
        """
        RedisSubscriberHandler，向asyncio.Queue() 发送消息，通知graph的interrupt继续执行
        """
        print('###### ToolCallAsyncInterruptGraph on_subscribed: %s' % data)
        if isinstance(data, str):
            data = json.loads(data)
        if 'tool_call_id' in data:
            self._finish_breakpoint(tool_call_id=data.get('tool_call_id'), tool_call_response=ToolMessage(**data))

    def _on_tool_call(self, selected_tool: BaseTool, tool_call: ToolCall, task: Any):
        # note: 如果是异步tool，就配置断点等
        if (isinstance(selected_tool, StructuredTool) and 'is_async' in selected_tool.metadata and
            selected_tool.metadata['is_async']) or \
                (isinstance(selected_tool, HttpTool) and selected_tool.tool_def.is_async):
            tool_call_id = tool_call['id']
            breakpoint = Breakpoint.create(status=0, task=task, id=tool_call_id, thread_id=self.thread_id)
            self.breakpoints.append(breakpoint)

            tool_call_subscriber.add_handler(
                channel_name=tool_call_id,
                handler=self
            )
            res = selected_tool.invoke(tool_call)
            return res

    def __init__(
        self,
        llm: BaseChatModel,
        tools: List,
        prompt_template: ChatPromptTemplate,
        **kwargs
    ):
        super().__init__(llm=llm, tools=tools, prompt_template=prompt_template, **kwargs)

    @classmethod
    def create(cls, llm: BaseChatModel, tools: List[BaseTool], **kwargs):
        prompt = kwargs.get('prompt', cls.default_prompt)
        assert prompt is not None
        assert check_prompt_required_filed(prompt=prompt, required_field=['{ex_info}', '{task}', '{tools}']) is True

        prompt_template = ChatPromptTemplate.from_messages(
            [
                (
                    "system", kwargs.get('prompt', prompt)
                )
            ]
        )
        agent = cls(llm=llm, tools=tools, prompt_template=prompt_template, **kwargs)
        return agent
