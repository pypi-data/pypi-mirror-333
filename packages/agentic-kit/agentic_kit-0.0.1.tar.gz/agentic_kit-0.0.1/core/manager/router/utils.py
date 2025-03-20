from typing import Union

from langchain_core.language_models import BaseChatModel

from utils.prompt import generate_system_prompt
from .schema import default_router_prompt


def route(llm: BaseChatModel, query: str, router_desc: str, router_options: Union[str, list], prompt: str=None, **kwargs):
    if prompt is None:
        prompt = default_router_prompt

    if isinstance(router_options, list):
        _router_options = [option for option in router_options]
        router_options = ','.join(_router_options)

    messages = generate_system_prompt(prompt=prompt, router_desc=router_desc, router_options=router_options, query=query)

    response = llm.invoke(messages)
    print(response)
    return response
