from typing_extensions import Union

from core.base.schema import BaseState
from ...schema import PlanModel


class PlannerState(BaseState):
    task: Union[str, list[str]]

    steps: list[PlanModel]

    plans: str


class RePlannerState(PlannerState):
    # inh from PlannerState
    # task: Union[str, list[str]]
    # steps: list[PlanModel]
    # plans: str

    init_steps: list[PlanModel]
    '''原始任务列表'''

    past_step_results: str
    '''已完成步骤的结果'''
