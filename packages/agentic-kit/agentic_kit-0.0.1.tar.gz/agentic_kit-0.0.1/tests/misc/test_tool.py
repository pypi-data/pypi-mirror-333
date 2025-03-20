from langchain_core.tools import tool, InjectedToolCallId
from typing_extensions import Annotated, Union


def add_attributes(**kwargs):
    def decorator(func):
        print('set ------- %s' % kwargs)
        for attr_name, value in kwargs.items():
            setattr(func, attr_name, value)
        return func
    return decorator


def add_metadata(*args, **kwargs):
    def decorator(func):
        # for attr_name, value in kwargs.items():
        print('set ------- ')
        setattr(func, 'metadata', {'is_sync': True})
        return func
    return decorator

# @add_attributes(metadata={'is_async': True})
@add_metadata()
@tool(
    parse_docstring=True,
    return_direct=False,
    # metadata={'is_sync': True}
)
def async_calculator_add_tool(
    x: Annotated[Union[int, float], '加法计算需要传入的数值，可以是整型或者浮点型'],
    y: Annotated[Union[int, float], '加法计算需要传入的数值，可以是整型或者浮点型'],
    tool_call_id: Annotated[str, InjectedToolCallId],
) :
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
    print(tool_call_id)


    # print(state)
    return ''

    # return {'content': 'success', 'artifact': 'artifact content'}

print(async_calculator_add_tool.metadata)
