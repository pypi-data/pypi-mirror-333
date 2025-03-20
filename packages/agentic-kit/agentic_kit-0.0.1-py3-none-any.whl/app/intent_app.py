from typing import Any

from langchain_community.chat_models import ChatTongyi
from langgraph.checkpoint.memory import MemorySaver
from langgraph.types import Command

from infrastructure.rpc.message import RpcChatMessage
from scenario.prebuilt.agent.intent.intent_recognition.intent_recognition_agent import IntentRecognitionGraph
from scenario.prebuilt.interactive.ws_chat_manager import WsInteractiveApp


class IntentApp(WsInteractiveApp):

    @classmethod
    def create(cls, ws_chat_manager: Any=None):
        app_id = 'IntentApp'
        app = cls(app_id=app_id)

        if ws_chat_manager:
            ws_chat_manager.add_app(app)

        return app

    def __init__(self, app_id: str):
        super().__init__(app_id)

        self.llm = ChatTongyi(
            model_name='qwen-max-latest',
            api_key='sk-b66bdec7097847f7af9d9fe63797c7c6',
            top_p=0.1,
        )
        self.checkpointer = MemorySaver()

        self.graph_map = {}

    def on_chat(self, message: RpcChatMessage, connection: Any = None, **kwargs):
        print(f'IntentApp.on_chat: f{message.to_pretty_json()}')

        data = message.message
        thread_id = data['thread_id']
        query = data['query']
        llm_agent = self.graph_map.get(thread_id, None)
        if llm_agent is None:
            llm_agent = IntentRecognitionGraph.create(llm=self.llm, intent_app=self, client_id=message.sender, checkpointer=self.checkpointer)
            self.graph_map[thread_id] = llm_agent
            # thread_id = str(uuid.uuid4())
            config = {"configurable": {"thread_id": thread_id}}
            res = llm_agent.callable.astream({
                "thread_id": thread_id,
                "query": query,
                'loop_counter': 1
            }, stream_mode='updates', config=config)
            for e in res:
                print('-----------------------------')
                print(e)
        else:
            print('IntentApp.on_chat resume graph : %s' % query)
            res = llm_agent.graph.astream(Command(resume=query),
                                          config={"configurable": {"thread_id": thread_id}},
                                          stream_mode='updates')
            for e in res:
                print('-----------------------------')
                print(e)
