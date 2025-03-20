from pydantic import BaseModel
from pydantic.fields import Field

from core.base.schema import BaseState


class IntentSlotSchema(BaseModel):
    slot: str = Field(..., description='用户意图的词槽意义，表示这个词槽代表的是什么信息')

    slot_info: str = Field(..., description='用户意图的词槽具体参数，表示从意图中提取的信息，填充到词槽里')


class IntentSchema(BaseModel):
    query: str = Field(..., description='用户的原始输入，大模型去理解这个原始输入的意图')

    slots: list[IntentSlotSchema] = Field(..., description='从用户的原始输入，提取的词槽信息列表，可能有多个词槽')

    scenario_list: list[str] = Field(..., description='分析用户的意图，得到的与这个意图相关的场景列表，可能有多个，不超过2个')

    result: str = Field(..., description='融合了用户的原始输入和填充词槽后的完整意图信息')

    lost_slots: list[str] = Field(..., description='分析了用户的原始输入意图后，缺失的词槽信息')


class IntentRecognitionState(BaseState):
    """意图识别状态"""

    query: str
    '''用户的原始输入，大模型去理解这个原始输入的意图'''

    intent: IntentSchema
    '''llm分析后的意图信息'''

    ex_info: str

    # lost_info: list[str]

    loop_counter: int

    should_finish: bool
