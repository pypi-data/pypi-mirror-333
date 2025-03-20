import operator

from langchain_core.messages import AnyMessage
from typing_extensions import Union, Annotated

from core.base.schema import BaseState


class LlmCallState(BaseState):
    task: Union[str, list[str]]

    ex_info: str

    results: Annotated[list[str], operator.add]

    messages: Annotated[list[AnyMessage], operator.add]

    should_finish: bool

    loop_counter: int
