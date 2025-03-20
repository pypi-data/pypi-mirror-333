from typing import Union

from pydantic import BaseModel

from core.base.schema import BaseState


class IntentModel(BaseModel):
    query: Union[str, list[str]]

    intent: str

    metadata: dict


class IntentClassifyState(BaseState):
    query: Union[str, list[str]]

    ex_info: str

    intent: Union[str, list[str]]

    intent_keywords: list[str]

    intent_entity: Union[list[IntentModel], IntentModel]
