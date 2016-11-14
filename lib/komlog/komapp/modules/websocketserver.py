'''
    this module implements a websocket server

'''


import signal
import asyncio
import functools
from komlog.komapp.modules import modules
from komlog.komcass import connection as casscon
from komlog.komfig import logging, config, options
from komlog.komimc import bus as msgbus
from komlog.komimc import api as msgapi
from komlog.komwebsock import app
from tornado.httpserver import HTTPServer
from tornado.platform.asyncio import AsyncIOMainLoop


loop = asyncio.get_event_loop()

class Websocketserver(modules.Module):
    def __init__(self, instance):
        super().__init__(
            self.__class__.__name__,
            instance,
            needs_db=True,
            needs_msgbus=True,
            needs_mailer=False,
            tasks=[self._websocket_server, self._messages_listener]
        )
        self.params={}
        self.params['ws_listen_port']=int(config.get(options.WS_LISTEN_PORT))+self.instance if config.get(options.WS_LISTEN_PORT) else None

    async def _websocket_server(self, start=True):
        if start:
            AsyncIOMainLoop().install()
            self.app = app.Application()
            self.http_server = HTTPServer(self.app)
            self.http_server.listen(self.params['ws_listen_port'])
        else:
            self.http_server.stop()

def get_module(instance):
    mod = Websocketserver(instance=instance)
    return mod

