from langchain_core.tools import tool
from typing_extensions import Annotated


@tool(parse_docstring=True)
def eval_tool(
    music: Annotated[str, '用户弹奏的音乐内容'],
) -> str:
    """
    这个工具评估用户的弹奏水平，给予打分，得分范围是从1分到10分，数字越小代表弹奏越差，数字越大代表弹奏越好。这个工具只做打分操作，不做其他任何操作。

    Args:
        music: 用户弹奏的音乐内容.

    Returns:
         str 用户弹奏得分以及简单的描述
    """
    print('=====eval_tool=======')
    print(f'music = {music}')
    return f'经过分析，你的得分是{5}分'

# @tool(
#     parse_docstring=True,
#     return_direct=True
# )
# def eval_tool(
#     music: Annotated[str, 'The content of the music played by the user'],
# ) -> str:
#     """
#     This tool evaluates the user's playing level and gives a score, with the score range being from 1 to 10. A lower number indicates poorer playing, while a higher number indicates better playing. This tool only performs the scoring operation and does not perform any other operations.
#
#     Args:
#         music: The content of the music played by the user.
#
#     Returns:
#          str The user's playing score and a brief description.
#
#     """
#     print('=====eval_tool=======')
#     print(f'music = {music}')
#     return f'After analysis, your score is {5}'
