from typing import Union

from openai import BaseModel
from typing_extensions import Any

from .base import IntentRetrieverBase
from ..schema import IntentModel


class FlatIntentRetriever(IntentRetrieverBase, BaseModel):
    """list结构的intent集合检索"""
    intent_options: list[str]

    def get_intent_options(self, query: str, **kwargs) -> list[Any]:
        return self.intent_options

    def retrieve(self, query: str, intent: list[str], **kwargs) -> Union[list[IntentModel], IntentModel, None]:
        def __convert(it: str):
            _it = it.split('^')
            if len(_it) != 2:
                return None
            metadata = {
                'id': _it[0],
                'intent': _it[1],
                **kwargs
            }
            return IntentModel(query=query, intent=_it[1], metadata=metadata)

        if len(intent) == 0:
            return None
        elif len(intent) == 1:
            return __convert(intent[0])
        else:
            res = []
            for intent_item in intent:
                res.append(__convert(intent_item))
            return res
