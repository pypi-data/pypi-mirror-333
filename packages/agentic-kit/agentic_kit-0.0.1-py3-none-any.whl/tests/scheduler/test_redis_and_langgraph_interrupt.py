from typing import TypedDict

from langgraph.errors import NodeInterrupt
from langgraph.types import interrupt, Command
from langgraph.checkpoint.memory import MemorySaver
from langgraph.graph import StateGraph
from langgraph.constants import START
import uuid
import redis
import threading
import time

class State(TypedDict):
    some_text: str

def human_node(state: State):
    # 使用 interrupt 函数暂停执行，等待人类输入
    print('使用 interrupt 函数暂停执行，等待人类输入')
    value = interrupt({"text_to_revise": state["some_text"]})
    print('-----human_node')
    print('resume value = %s' % value)
    return {"some_text": value}



# 构建 LangGraph
graph_builder = StateGraph(State)
graph_builder.add_node("human_node", human_node)
graph_builder.add_edge(START, "human_node")

# 使用 MemorySaver 作为检查点
checkpointer = MemorySaver()
graph = graph_builder.compile(checkpointer=checkpointer)

# 配置线程 ID
thread_config = {"configurable": {"thread_id": uuid.uuid4()}}

# 连接到 Redis
r = redis.Redis(host='localhost', port=6379, db=0)

# 定义 Redis Pub/Sub 回调函数
def redis_callback(message):
    print(f"Received Redis message: {message['data'].decode()}")
    # 假设 Redis 消息包含人类输入
    human_input = message['data'].decode()
    # 通过 LangGraph 的 Command 恢复执行
    print('-----通过 LangGraph 的 Command 恢复执行')
    graph.invoke(Command(resume=human_input), config=thread_config)

# 启动 Redis 订阅者线程
def start_redis_subscriber():
    pubsub = r.pubsub()
    pubsub.subscribe("langgraph_events")
    for message in pubsub.listen():
        if message['type'] == 'message':
            redis_callback(message)

# 在后台启动 Redis 订阅者
t = threading.Thread(target=start_redis_subscriber, daemon=True)
t.start()

# 运行 LangGraph 直到中断
graph.invoke({"some_text": "Original text"}, config=thread_config)

# 模拟 Redis 发布消息
print('####sleep2')
time.sleep(2)  # 等待 LangGraph 挂起
print('####sleep ok')
print('publish event')

print(graph.get_state(config=thread_config))
print(';;;;state')

r.publish("langgraph_events", "Edited textxxx")
t.join()
