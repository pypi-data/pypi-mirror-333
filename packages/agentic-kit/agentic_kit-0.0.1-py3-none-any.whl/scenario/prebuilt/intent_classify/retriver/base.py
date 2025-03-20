from abc import ABC, abstractmethod
from typing import Union

from typing_extensions import Any

from ..schema import IntentModel


class IntentRetrieverBase(ABC):
    """意图检索"""
    @abstractmethod
    def get_intent_options(self, query: str, **kwargs) -> list[Any]:
        """获取可以选择的意图的选项，返回值需要与retrieve流程中的解析转化对应"""
        raise NotImplemented

    @abstractmethod
    def retrieve(self, query: str, intent: list[Any], **kwargs) -> Union[list[IntentModel], IntentModel, None]:
        """根据llm判断的意图，解析后返回一个完整的IntentModel"""
        raise NotImplemented
