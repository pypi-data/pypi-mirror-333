from langgraph.errors import GraphDelegate
from typing_extensions import TypedDict
from langgraph.graph import StateGraph, START, END
from langgraph.types import interrupt, Command
from langgraph.checkpoint.memory import MemorySaver

class State(TypedDict):
    input: str
    user_feedback: str

def step_1(state: State) -> State:
    print("---Step 1---")
    return state

def human_feedback(state: State) -> State:
    print("---Human Feedback---")
    # 抛出中断异常，等待用户输入
    feedback = interrupt("Please provide feedback:")
    return {"user_feedback": feedback}

def step_3(state: State) -> State:
    print("---Step 3---")
    return state

builder = StateGraph(State)
builder.add_node("step_1", step_1)
builder.add_node("human_feedback", human_feedback)
builder.add_node("step_3", step_3)
builder.add_edge(START, "step_1")
builder.add_edge("step_1", "human_feedback")
builder.add_edge("human_feedback", "step_3")
builder.add_edge("step_3", END)

class CustomGraphDelegate(GraphDelegate):
    def on_interrupt(self, node_name: str, state: State):
        print(f"Interrupted at node: {node_name}")
        return state

# 设置内存检查点
checkpointer = MemorySaver()
graph = builder.compile(checkpointer=checkpointer, delegate=CustomGraphDelegate())

initial_input = {"input": "hello world"}
thread_config = {"configurable": {"thread_id": "1"}}

# 运行图直到第一次中断
for event in graph.stream(initial_input, thread_config, stream_mode="updates"):
    print(event)

# 使用用户输入恢复执行
for event in graph.stream(Command(resume="User feedback here"), thread_config, stream_mode="updates"):
    print(event)
