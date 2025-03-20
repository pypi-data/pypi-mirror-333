from abc import abstractmethod

from langchain_core.language_models import BaseChatModel
from langchain_core.prompts import ChatPromptTemplate
from langchain_core.tools import BaseTool
from typing_extensions import List

from core.base.component import InvokeComponentBase
from .schema import ResolverState


class ResolverBase(InvokeComponentBase):
    def __init__(
            self,
            llm: BaseChatModel,
            tools: List[BaseTool],
            prompt_template: ChatPromptTemplate,
            **kwargs
    ):
        super().__init__(llm=llm, tools=tools, prompt_template=prompt_template, **kwargs)

    @abstractmethod
    def invoke(self, state: ResolverState):
        raise NotImplemented
