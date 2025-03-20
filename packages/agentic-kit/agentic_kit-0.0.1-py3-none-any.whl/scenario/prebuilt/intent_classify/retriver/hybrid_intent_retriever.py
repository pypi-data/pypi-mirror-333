from typing import Union

from pydantic import BaseModel
from typing_extensions import Any

from .base import IntentRetrieverBase
from ..schema import IntentModel


class VectorIntentRetriever(IntentRetrieverBase, BaseModel):
    """多种的intent集合检索"""

    retrievers: list[IntentRetrieverBase]

    def get_intent_options(self, query: Any, **kwargs) -> list[Any]:
        pass

    def retrieve(self, query: str, intent: list[Any], **kwargs) -> Union[list[IntentModel], IntentModel, None]:
        pass
