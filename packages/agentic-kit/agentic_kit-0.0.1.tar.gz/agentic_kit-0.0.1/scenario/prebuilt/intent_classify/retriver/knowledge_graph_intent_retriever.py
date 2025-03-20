from typing import Union

from typing_extensions import Any

from .base import IntentRetrieverBase
from ..schema import IntentModel


class KnowledgeGraphIntentRetriever(IntentRetrieverBase):
    """知识图谱的intent集合检索"""

    def get_intent_options(self, query: Any, **kwargs) -> list[Any]:
        pass

    def retrieve(self, query: str, intent: list[Any], **kwargs) -> Union[list[IntentModel], IntentModel, None]:
        pass
