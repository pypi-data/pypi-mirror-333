from abc import abstractmethod, ABC
from typing import Any

from langchain_core.tools import BaseTool


# class BaseToolAsyncArgsSchema(args_schema_cls):
#     tool_call_id: Annotated[str, InjectedToolCallId]


# todo:
# 1. 设置args_schema，参考rpt tool
# 2. 封装异步tool调用

class BaseToolAsync(BaseTool, ABC):
    """异步tool的基类"""

    is_async: bool = True

    def __init__(self, **kwargs):
        super().__init__(**kwargs)

    # @celery_app.task(name='celery_app.tasks.calculator_add')
    # @tool_call_publish_wrapper(publisher=tool_call_publisher)
    @abstractmethod
    def _tool_do_async(self, **kwargs):
        raise NotImplemented

    def _run(self, *args: Any, **kwargs: Any) -> Any:
        pass
