from langchain_core.tools import tool, InjectedToolCallId
from typing_extensions import Annotated, Union

from core.tool.asynchronous.async_tool_decorator import set_tool_async
from ..celery.tasks import calculator_add

@set_tool_async()
@tool(
    parse_docstring=True,
    return_direct=False,
)
def async_calculator_add_tool(
    x: Annotated[Union[int, float], '加法计算需要传入的数值，可以是整型或者浮点型'],
    y: Annotated[Union[int, float], '加法计算需要传入的数值，可以是整型或者浮点型'],
    tool_call_id: Annotated[str, InjectedToolCallId],
):
    """
    这个工具是加法计算器，可以计算两个数值的和。

    Args:
        x: 加法计算需要传入的数值，可以是整型或者浮点型.
        y: 加法计算需要传入的数值，可以是整型或者浮点型.

    Returns:
         Union[int, float] 两个数字相加的总和
    """
    print('=====async_calculator_add_tool=======')
    print(f'cal = {x} + {y}')
    print('tool_call_id = %s' % tool_call_id)
    # print(state)
    calculator_add.apply_async(kwargs={
        'x': x,
        'y': y,
        **{'tool_call_id': tool_call_id}
    }, retry=True)
    return ''

    # return {'content': 'success', 'artifact': 'artifact content'}
