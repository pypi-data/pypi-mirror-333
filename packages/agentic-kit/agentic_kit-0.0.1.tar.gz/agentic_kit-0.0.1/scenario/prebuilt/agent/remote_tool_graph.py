from core.base.graph import PatternToolGraphBase


class ToolCallGraphBase(PatternToolGraphBase, ABC):
    def __init__(self, llm: BaseChatModel, tools: List, prompt_template: ChatPromptTemplate, **kwargs):
        super().__init__(llm=llm, tools=tools, prompt_template=prompt_template, **kwargs)

        self._init_graph()

    def _init_graph(self):
        """初始化graph： CompiledStateGraph"""
        builder = StateGraph(ToolCallState)
        builder.add_node('tool_call', self.invoke)
        builder.add_edge('tool_call', END)
        builder.set_entry_point('tool_call')
        self.graph = builder.compile()

    @classmethod
    def create(cls, llm: BaseChatModel, tools: List[BaseTool], **kwargs):
        prompt = kwargs.get('prompt', default_prompt)
        assert check_prompt_required_filed(prompt=prompt, required_field=['{ex_info}', '{task}', '{tool}']) is True
        prompt_template = ChatPromptTemplate.from_messages(
            [
                (
                    "system", kwargs.get('prompt', prompt)
                )
            ]
        )

        agent = cls(llm=llm, tools=tools, prompt_template=prompt_template)
        return agent
