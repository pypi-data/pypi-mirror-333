import sys

sys.path.append('/Users/manson/ai/app/agentic_kit/')

from scenario.prebuilt.tools.remote.ws.ws_toolkit_manager import WsToolkitManager

# app = WsTornadoServer(tk_manager=WsToolkitManager(), handlers=[(r"/websocket", WsHandler)])

if __name__ == "__main__":
    # app.listen(8888)
    # tornado.ioloop.IOLoop.current().start()
    tk_manager = WsToolkitManager()
    tk_manager.start()
