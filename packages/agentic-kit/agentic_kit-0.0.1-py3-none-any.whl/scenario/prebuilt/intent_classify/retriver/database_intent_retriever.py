from typing import Union

from typing_extensions import Any

from .base import IntentRetrieverBase
from ..schema import IntentModel


class DatabaseIntentRetriever(IntentRetrieverBase):
    """数据库的intent集合检索"""

    def get_intent_options(self, query: str, **kwargs) -> list[Any]:
        pass

    def retrieve(self, query: str, intent: list[str], **kwargs) -> Union[list[IntentModel], IntentModel, None]:
        pass
