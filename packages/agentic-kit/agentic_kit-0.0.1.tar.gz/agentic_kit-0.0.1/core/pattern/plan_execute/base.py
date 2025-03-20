from abc import ABC

from core.base.graph import PatternGraphBase
from core.pattern.component.executor import ExecutorBase
from core.pattern.component.planner import PlannerBase
from core.pattern.component.resolver import ResolverBase


class PlanExecuteBase(PatternGraphBase, ABC):
    planner: PlannerBase

    replanner: PlannerBase

    executor: ExecutorBase

    resolver: ResolverBase

    def __init__(self,
                 planner: PlannerBase,
                 replanner: PlannerBase,
                 executor: ExecutorBase,
                 resolver: ResolverBase,
                 **kwargs
                 ):
        assert planner is not None
        assert replanner is not None
        assert executor is not None
        assert resolver is not None

        super().__init__(**kwargs)

        self.planner = planner
        self.replanner = replanner
        self.executor = executor
        self.resolver = resolver

        self._init_graph()

    # @abstractmethod
    # def _init_graph(self):
    #     raise NotImplemented
