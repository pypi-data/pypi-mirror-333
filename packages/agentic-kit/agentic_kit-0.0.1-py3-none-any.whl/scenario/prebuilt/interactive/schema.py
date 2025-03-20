from typing import Any

from starlette.websockets import WebSocket


class WsChatClient:
    app_id: str

    client_id: str

    client_desc: str = ''

    connection: WebSocket

    app: Any
    '''关联的app'''

    @classmethod
    def create(cls, app_id: str, client_id: str, connection: WebSocket, client_desc: str, app: Any=None):
        client = cls(app_id=app_id, client_id=client_id, client_desc=client_desc, connection=connection, app=app)
        return client

    def __init__(self, app_id: str, client_id: str, connection: WebSocket, client_desc: str, app: Any=None):
        self.app_id = app_id
        self.client_id = client_id
        self.connection = connection
        self.client_desc = client_desc
        self.app = app

    def link_app(self, app: Any):
        if self.app is None:
            self.app = app
