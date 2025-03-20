import uuid

from langchain_community.chat_models import ChatTongyi
from langchain_core.messages import ToolCall, AIMessage
from langgraph.constants import END
from langgraph.graph import StateGraph
from pydantic import Field

from app.middleware import checkpointer, connection_manager, ws_message_handler_manager, \
    ws_toolkit_manager
from app.tools.async_calculator_add import async_calculator_add_tool
from core.graph.tool_call_async_interrupt_graph import ToolCallAsyncInterruptGraph
from core.graph.tool_call_ws_interrupt_graph import ToolCallWsInterruptGraph
from core.manager.workflow.node_manager import NodeManager
from core.pattern.tool_use.schema import ToolCallState, ToolCallWithBreakpointState
from core.tool.rpc.http import ApiDef
from core.tool.rpc.http.http_tool_async import PostToolAsync
from core.tool.rpc.http.schema import ApiDefArgsScheme
from infrastructure.rpc.fastapi.ws_server import create_ws_server

# todo:
# 1. on startup ,初始化中间件,
# redis subscriber


app = create_ws_server(
    connection_manager=connection_manager,
    ws_message_handler_manager=ws_message_handler_manager,
)


@app.post("/test/async_task", summary="测试异步任务", include_in_schema=True)
async def async_task():
    # tollcall = ToolCall(name='async_calculator_add_tool', args={'x': 1, 'y': 2}, id='task_id_1234')
    # call_adabb8393ed34748a8cfdd
    tollcall =  ToolCall(**{'name': 'async_calculator_add_tool', 'args': {'x': 100, 'y': 200}, 'id': str(uuid.uuid4()), 'type': 'tool_call'})
    # async_calculator_add_tool.invoke(tollcall)

    tool_node = NodeManager.make_injectable_tool(async_calculator_add_tool, messages_key='place_holder')

    def toolcall_node(state):
        resp = tool_node.invoke(state)
        print('toolcall_node=======')
        print(resp)
        print(resp['place_holder'][0])
        print(resp['place_holder'][0].status)

    builder = StateGraph(ToolCallState)
    builder.add_node('tool_call', toolcall_node)
    builder.add_edge('tool_call', END)
    builder.set_entry_point('tool_call')
    _graph = builder.compile()

    state = {
        "place_holder": [AIMessage("", tool_calls=[tollcall])],
    }

    _graph.invoke(state)


@app.post("/test/interrupt_graph", summary="测试可中断graph", include_in_schema=True)
async def dist_interrupt_graph():
    llm = ChatTongyi(
        model_name='qwen-max-latest',
        api_key='sk-b66bdec7097847f7af9d9fe63797c7c6',
        top_p=0.1,
    )

    # 配置线程 ID
    thread_id = str(uuid.uuid4())
    print(f'thread_id = {thread_id}')
    thread_config = {"configurable": {"thread_id": thread_id}}
    state = {
        'thread_id': thread_id,
        'task': '请计算1+2=？',
        # 'task': '服务正常吗？',
        # 'task': '你是什么大模型？',
    }

    class LLmChatInput(ApiDefArgsScheme):
        model_uid: str = Field(..., description="选择模型id，默认选择deepseek-chat^deepseek-chat^396@deepseek^18", title='选择模型id')
        q: str = Field(..., description="提问的问题描述", title='提问的问题描述')

    http_async = PostToolAsync(tool_def=ApiDef(url='http://221.229.0.177:9981/chat', method='post', name='llm_chat', description='通过大模型调用来回答问题', is_async=True, args_schema=LLmChatInput))

    g = ToolCallAsyncInterruptGraph.create(llm=llm, tools=[async_calculator_add_tool])
    # g = ToolCallAsyncInterruptGraph.create(llm=llm, tools=[http_async])
    async for res in g.astream(state, config=thread_config, stream_mode='values'):
        print("---1")
        print(res)
        print("---2")

@app.post("/test/interrupt_ws_graph", summary="测试可中断graph", include_in_schema=True)
async def dist_ws_interrupt_graph():
    llm = ChatTongyi(
        model_name='qwen-max-latest',
        api_key='sk-b66bdec7097847f7af9d9fe63797c7c6',
        top_p=0.01,
    )

    # 配置线程 ID
    thread_id = str(uuid.uuid4())
    print(f'thread_id = {thread_id}')
    thread_config = {"configurable": {"thread_id": thread_id}}
    state = {
        'thread_id': thread_id,
        'task': '请计算1+2=？',
        # 'breakpoints': []
    }

    tools = ws_toolkit_manager.get_tools()
    print(tools)
    g = ToolCallWsInterruptGraph.create(llm=llm, tools=tools, ws_message_handler_manager=ws_message_handler_manager, checkpointer=checkpointer)

    # job = Job(thread_id=thread_id, context=state, init_state=copy.deepcopy(state), runnable=g.graph,
    #           thread_config=thread_config, stream_mode='values', is_stream=True, start_time=datetime.datetime.now())
    # scheduler.enqueue(thread_id=thread_id, job=job, auto_start=False)
    # scheduler.start(thread_id=thread_id)
    #

    async for res in g.astream(state, config=thread_config, stream_mode='values'):
        print("---1")
        print(res)
        print("---2")

    # for s in res:
    #     print("---1")
    #     print(s)
    #     print("---2")


@app.post("/test/interrupt_mix_graph", summary="测试可中断graph", include_in_schema=True)
async def dist_mix_interrupt_graph():
    llm = ChatTongyi(
        model_name='qwen-max-latest',
        api_key='sk-b66bdec7097847f7af9d9fe63797c7c6',
        top_p=0.01,
    )
    # 配置线程 ID
    thread_id = str(uuid.uuid4())
    print(f'thread_id = {thread_id}')
    thread_config = {"configurable": {"thread_id": thread_id}}
    state = {'thread_id': thread_id, 'task': '请计算1+2=？'}

    async def tool_call1(state: ToolCallWithBreakpointState):
        g = ToolCallAsyncInterruptGraph.create(llm=llm, tools=[async_calculator_add_tool])
        async for res in g.astream(state, config=thread_config, stream_mode='updates'):
            print("@@@@@@@@@@@@@@@tool_call1---1")
            print(res)
            print("@@@@@@@@@@@@@@@tool_call1---2")
            # yield res

    async def tool_call2(state: ToolCallWithBreakpointState):
        tools = ws_toolkit_manager.get_tools()
        print(tools)
        g = ToolCallWsInterruptGraph.create(llm=llm, tools=tools, ws_message_handler_manager=ws_message_handler_manager,
                                            checkpointer=checkpointer)
        async for res in g.astream(state, config=thread_config, stream_mode='updates'):
            print("@@@@@@@@@@@@@@@tool_call2---1")
            print(res)
            print("@@@@@@@@@@@@@@@tool_call2---2")
            # yield res

    builder = StateGraph(ToolCallWithBreakpointState)
    builder.add_node('tool_call1', tool_call1)
    builder.add_node('tool_call2', tool_call2)
    builder.add_edge('tool_call1', 'tool_call2')
    builder.add_edge('tool_call2', END)
    builder.set_entry_point('tool_call1')
    graph = builder.compile(checkpointer=checkpointer)

    async for res in graph.astream(state, config=thread_config, stream_mode='updates'):
        print("---------------------------------------------1")
        print(res)
        print("---------------------------------------------2")


@app.get("/", summary="swagger 文档", include_in_schema=False)
async def document():
    from starlette.responses import RedirectResponse
    return RedirectResponse(url="/docs")

#
# """
# celery相关
# """
#
# celery_config = CeleryConfig()
# celery_app = create_celery_app(celery_config=CeleryConfig(include=['app.tools.async_calculator_add']))
#
# class CeleryTaskSubscriberMessageHandlerFake(CeleryTaskSubscriberMessageHandler):
#     def on_subscribed(self, data: dict):
#         print('CeleryTaskSubscriberMessageHandlerFake: %s' % data)
# subscriber = CeleryTaskSubscriber.create(config=CeleryTaskSubscriberConfig(), handler=CeleryTaskSubscriberMessageHandlerFake(), auto_start=True)
