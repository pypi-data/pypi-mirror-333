from langchain_core.tools import tool
from typing_extensions import Annotated


@tool(parse_docstring=True)
def abc_music_tool(
    style: Annotated[str, '用户想要生成的音乐风格'],
    length: Annotated[int, '用户想要生成的音乐文件的长度'],
) -> str:
    """
    这个工具是可以生成abc格式的音乐文件，输入一些生成音乐的提示，比如风格，长度等等，返回abc格式的文件，以字符串形式返回. 这个工具只做音乐生成操作，不做其他任何操作。

    Args:
        style: 用户想要生成的音乐风格
        length: 用户想要生成的音乐文件的长度

    Returns:
         str 返回abc格式的文件，以字符串形式返回
    """
    print('=====abc_music_tool=======')
    print(f'style = {style}')
    print(f'length = {length}')
    return '经过分析，已生成abc格式的曲谱，如下： X:1\n abcd|efg'
#
#
# @tool(parse_docstring=True)
# def abc_music_tool(
#     style: Annotated[str, 'The music style the user wants to generate'],
#     length: Annotated[int, 'The desired length of the music file the user wants to generate'],
# ) -> str:
#     """
#     This tool is capable of generating music files in abc format. It takes inputs such as prompts for music generation, like style, length, etc., and returns the file in abc format as a string. This tool only performs the operation of music generation and does not perform any other operations.
#
#     Args:
#         style: The music style the user wants to generate
#         length: The desired length of the music file the user wants to generate
#
#     Returns:
#          str Returns a file in abc format, returned as a string.
#     """
#     print('=====abc_music_tool=======')
#     print(f'style = {style}')
#     print(f'length = {length}')
#     return 'After analysis, an abc format score has been generated, as follows: X:1\n abcd|efg'
