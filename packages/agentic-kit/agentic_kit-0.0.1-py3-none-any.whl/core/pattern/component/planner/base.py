from abc import abstractmethod

from langchain_core.language_models import BaseChatModel
from langchain_core.prompts import ChatPromptTemplate
from langchain_core.tools import BaseTool
from typing_extensions import List

from core.base.component import InvokeComponentBase
from .parser import PlanParserBase
from .schema import PlannerState


class PlannerBase(InvokeComponentBase):
    """plan生成的基类"""

    plan_parser: PlanParserBase

    def __init__(
        self,
        llm: BaseChatModel,
        tools: List[BaseTool],
        prompt_template: ChatPromptTemplate,
        plan_parser: PlanParserBase,
        **kwargs
    ):
        super().__init__(llm=llm, tools=tools, prompt_template=prompt_template, **kwargs)
        self.plan_parser = plan_parser # if plan_parser else PlanParserYaml()

    @abstractmethod
    def invoke(self, state: PlannerState):
        raise NotImplemented


def planner_retry_failed_callback(retry_state):
    print('planner_retry_failed_callback: %s' % retry_state)
    return {'steps': [], 'plans': ''}
