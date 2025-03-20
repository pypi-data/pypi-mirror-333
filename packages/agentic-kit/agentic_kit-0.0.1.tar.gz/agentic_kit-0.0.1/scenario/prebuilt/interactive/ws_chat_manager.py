import asyncio
from abc import ABC, abstractmethod
from typing import Any, Union, Dict

from starlette.websockets import WebSocket

from infrastructure.rpc.fastapi.ws_connection_manager import ConnectionListener
from infrastructure.rpc.message import RpcChatMessage, RpcClientRegisterMessage, RpcClientUnRegisterMessage, \
    RpcMessageTypeEnum, RpcMessageFactory, RpcMessageBase
from infrastructure.rpc.message_handler import RpcClientRegisterHandler, \
    RpcClientUnRegisterHandler, RpcChatMessageHandler
from .schema import WsChatClient


class WsInteractiveApp(ABC):
    """通过ws交互的app的基类"""

    app_id: str

    manager: Any
    '''当挂在到某个manager时，设置'''

    clients: dict[str, WsChatClient]
    '''client_id: WsChatClient'''

    message_send_queue = asyncio.Queue()
    '''发送消息队列'''

    def __init__(self, app_id: str):
        assert app_id is not None
        self.app_id = app_id

        self.clients = {}

        asyncio.create_task(self.message_sender())

    async def message_sender(self):
        """接受消息队列，调用connection实际去发送消息"""
        while True:
            message = await self.message_send_queue.get()
            _client = self.clients.get(message.receiver, None)
            if _client:
                # note: 根据不同message类型，调用不同发送方法
                if isinstance(message, str):
                    await _client.connection.send_text(message)
                elif isinstance(message, bytes):
                    await _client.connection.send_bytes(message)
                elif isinstance(message, dict):
                    await _client.connection.send_json(message)
                elif isinstance(message, RpcMessageBase):
                    await _client.connection.send_json(message.to_send_json())
                else:
                    print(f'unknown message: {message}')

    @abstractmethod
    def on_chat(self, message: RpcChatMessage, connection: Any = None, **kwargs):
        raise NotImplemented

    def send_message(self, message: Union[bytes, str, Dict[str, Any]]):
        """发送消息，将消息发送到队列中，队列消费者进行实际msg发送"""
        print('######WsInteractiveApp.send_message: %s' % message)
        self.message_send_queue.put_nowait(message)

    def send_message_to_client(self, client_id: str, message: Union[bytes, str, Dict[str, Any]]):
        """发送消息，将消息发送到队列中，队列消费者进行实际msg发送"""
        msg = RpcMessageFactory.create({
            'sender': self.app_id,
            'receiver': client_id,
            'type': RpcMessageTypeEnum.CHAT,
            'message': message
        })
        self.send_message(message=msg)

    def broadcast_died(self):
        """停止消息发送给所有client"""
        for client in self.clients.values():
            message = RpcMessageFactory.create({
                'type': RpcMessageTypeEnum.SERVER_DIED,
                'sender': self.app_id,
                'receiver': client.client_id,
            })
            self.send_message(message=message)

    def broadcast_live(self):
        """上线消息发送给所有client"""
        for client in self.clients.values():
            message = RpcMessageFactory.create({
                'type': RpcMessageTypeEnum.CLIENT_REGISTER_OK,
                'sender': self.app_id,
                'receiver': client.client_id,
            })
            self.send_message(message=message)

    def add_client(self, client: WsChatClient, notify: bool=True):
        if self.clients.get(client.client_id, None) is None:
            self.clients[client.client_id] = client
            client.link_app(app=self)

            # note: 通知注册成功
            if notify:
                message = RpcMessageFactory.create({
                    'type': RpcMessageTypeEnum.CLIENT_REGISTER_OK,
                    'sender': self.app_id,
                    'receiver': client.client_id,
                })
                self.send_message(message=message)
        self.dump()

    def remove_client(self, client_id: str, notify: bool=False):
        if self.clients.get(client_id, None) is not None:
            client = self.clients.pop(client_id)

            # note: 通知
            if notify:
                message = RpcMessageFactory.create({
                    'type': RpcMessageTypeEnum.CLIENT_REMOVED,
                    'sender': self.app_id,
                    'receiver': client.client_id,
                })
                self.send_message(message=message)
        self.dump()

    def remove_client_by_connection(self, connection: WebSocket):
        """当connection断开时，移除对应的client"""
        removed_client_ids = []
        for client in self.clients.values():
            if client.connection.uid == connection.uid:
                removed_client_ids.append(client.client_id)
        if len(removed_client_ids) > 0:
            for client_id in removed_client_ids:
                # print('############ remove %s' % client_id)
                self.remove_client(client_id=client_id, notify=False)

    def dump(self):
        print('=======WsInteractiveApp[%s]========' % self.app_id)
        print(self.clients)


class WsChatManager(RpcChatMessageHandler, RpcClientRegisterHandler, RpcClientUnRegisterHandler, ConnectionListener):

    pending_clients: list[WsChatClient]
    '''app没有ready时候，缓存的clients'''

    apps: dict[str, WsInteractiveApp]

    # connection_to_client_map: dict[str, str]
    # '''connect_id与client_id的映射'''

    @classmethod
    def create(cls):
        manager = cls()
        return manager

    def __init__(self):
        self.apps = {}
        self.pending_clients = []
        self.connection_to_client_map = {}

    def on_chat(self, message: RpcChatMessage, connection: Any = None, **kwargs):
        print('########WsChatManager########')
        print(message.to_pretty_json())
        app_id = message.receiver
        app = self.get_app(app_id=app_id)
        if app:
            app.on_chat(message=message, connection=connection, **kwargs)

    def on_client_register(self, message: RpcClientRegisterMessage, connection: Any = None, **kwargs):
        if message.type == RpcMessageTypeEnum.CLIENT_REGISTER:
            client_id = message.sender
            app_id = message.receiver
            if not client_id or not app_id:
                print('illegal client unregister: %s' % message.to_pretty_json())
                return
            description = message.info.get('description', '') if message.info else ''

            app = self.get_app(app_id=app_id)
            client = WsChatClient.create(app_id=app_id, client_id=client_id, client_desc=description, connection=connection, app=app)
            if app is None:
                # note: 如果app没有ready，先缓存起来
                self.pending_clients.append(client)
            else:
                app.add_client(client=client)

    def on_client_unregister(self, message: RpcClientUnRegisterMessage, connection: Any = None, **kwargs):
        if message.type == RpcMessageTypeEnum.CLIENT_UNREGISTER:
            client_id = message.sender
            app_id = message.receiver
            if not client_id or not app_id:
                print('illegal client unregister: %s' % message.to_pretty_json())
                return

            app = self.get_app(app_id=app_id)
            if app:
                app.remove_client(client_id=client_id, notify=True)

    def on_connect(self, connection: Any):
        pass

    def on_disconnect(self, connection: Any):
        for app in self.apps.values():
            app.remove_client_by_connection(connection=connection)

    def get_app(self, app_id):
        return self.apps.get(app_id, None)

    def add_app(self, app: WsInteractiveApp):
        assert app is not None
        app_id = app.app_id
        if self.apps.get(app_id) is None:
            self.apps[app_id] = app
            app.manager = self

            # 关联之前缓存的client，并广播通知
            for client in self.pending_clients:
                client.link_app(app)
            app.broadcast_live()
        self.dump()

    def remove_app(self, app_id: str):
        app = self.apps.get(app_id, None)
        if app:
            self.apps.pop(app_id)
            app.broadcast_died()
        self.dump()

    def dump(self):
        print('=======WsChatManager========')
        print(self.apps)
        for app in self.apps.values():
            app.dump()
