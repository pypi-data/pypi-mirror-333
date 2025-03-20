from langgraph.checkpoint.memory import MemorySaver

from app.intent_app import IntentApp
from core.manager.tool.ws_toolkit_manager import WsToolkitManager
from core.scheduler.scheduler import Scheduler
from infrastructure.event_driven.ws.ws_message_handler_manager import WsMessageHandlerManager
from infrastructure.rpc.fastapi.ws_connection_manager import WsConnectionManager
from infrastructure.rpc.message import RpcMessageTypeEnum
from infrastructure.rpc.session_mananger import SessionManager
from scenario.prebuilt.interactive.ws_chat_manager import WsChatManager

"""全局的中间件"""

session_manager = SessionManager.create()

# websocket相关全局对象
ws_toolkit_manager = WsToolkitManager.create(session_manager=session_manager)
'''mixin（SessionManager, ToolkitManager）全局的session管理和ws tool管理'''

connection_manager = WsConnectionManager.create()
connection_manager.add_connection_listener(session_manager)
connection_manager.add_connection_listener(ws_toolkit_manager)
'''全局的ws连接管理器'''

ws_message_handler_manager = WsMessageHandlerManager.create()
ws_message_handler_manager.add_message_handler(RpcMessageTypeEnum.TOOL_REGISTER, ws_toolkit_manager)
ws_message_handler_manager.add_message_handler(RpcMessageTypeEnum.TOOL_UNREGISTER, ws_toolkit_manager)
'''全局的ws消息管理器'''

checkpointer = MemorySaver()
'''全局checkpointer'''

scheduler = Scheduler.create()
'''全局任务调度器'''

ws_chat_manager = WsChatManager.create()
ws_message_handler_manager.add_message_handler(RpcMessageTypeEnum.CHAT, ws_chat_manager)
ws_message_handler_manager.add_message_handler(RpcMessageTypeEnum.CLIENT_REGISTER, ws_chat_manager)
ws_message_handler_manager.add_message_handler(RpcMessageTypeEnum.CLIENT_UNREGISTER, ws_chat_manager)
connection_manager.add_connection_listener(ws_chat_manager)
'''全局chat manager'''

intent_app = IntentApp.create(ws_chat_manager=ws_chat_manager)
'''全局意图识别'''
