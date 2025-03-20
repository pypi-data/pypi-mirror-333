from langchain_core.language_models import BaseChatModel
from langchain_core.prompts import ChatPromptTemplate
from langchain_core.tools import BaseTool
from tenacity import stop_after_attempt, retry
from typing_extensions import List

from utils.prompt import check_prompt_required_filed
from utils.tools import get_tools_desc_for_prompt_zh
from .base import PlannerBase, planner_retry_failed_callback
from .parser import PlanParserYaml
from .schema import PlannerState


class CotPlanner(PlannerBase):
    """Chain-of-Thought planner"""

    default_prompt: str = ''

    @retry(stop=stop_after_attempt(3), retry_error_callback=planner_retry_failed_callback)
    def invoke(self, state: PlannerState):
        task = state["task"]
        print(f'########## CotPlanner 开始执行分析 [{state["task"]}] ##########')

        tools_desc = get_tools_desc_for_prompt_zh(self.tools)
        response = self.llm_callable_with_tools.invoke({
            'task': task,
            'tool': tools_desc,
        })

        plans = response.content
        steps = self.plan_parser.parse(content=plans)
        if len(steps) == 0:
            # note: for retry
            raise Exception('empty plans, retry')
        for item in steps:
            print(item.model_dump_json())
        print('########## CotPlanner 执行完毕，已生成详细step ##########\n\n\n')
        return {
            'steps': steps,
            'plans': plans
        }

    @classmethod
    def create(cls, llm: BaseChatModel, tools: List[BaseTool], **kwargs):
        # note: 处理prompt和parser，两者必须成对出现，或者同时为None
        prompt = kwargs.get('prompt', None)
        plan_parser = kwargs.get('plan_parser', None)
        if (prompt and not plan_parser) or (plan_parser and not prompt):
            raise Exception('prompt and plan_parser not match. both None or both not UnNone.')
        if prompt is None:
            prompt = cls.default_prompt
        if plan_parser is None:
            plan_parser = PlanParserYaml()

        # note: prompt中必须包含的字段
        assert check_prompt_required_filed(prompt=prompt, required_field=['{task}', '{tool}']) is True

        prompt_template = ChatPromptTemplate.from_messages(
            [
                (
                    "system", prompt
                )
            ]
        )
        planner = cls(llm=llm, prompt_template=prompt_template, tools=tools, plan_parser=plan_parser, **kwargs)
        return planner
