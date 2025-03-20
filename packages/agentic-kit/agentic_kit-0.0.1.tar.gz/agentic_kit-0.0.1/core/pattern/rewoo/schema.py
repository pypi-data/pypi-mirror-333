from core.base.schema import BaseState


class ReWooState(BaseState):
    task: str

    steps: list

    step_results: list

    final_result: str
