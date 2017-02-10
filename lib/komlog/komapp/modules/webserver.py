import signal
import asyncio
import functools
from komlog.komws2 import webapp
from komlog.komcass import connection as casscon
from komlog.komapp.modules import modules
from komlog.komfig import logging, config, options
from komlog.komimc import bus as msgbus
from tornado.httpserver import HTTPServer
from tornado.platform.asyncio import AsyncIOMainLoop


loop = asyncio.get_event_loop()

class Webserver(modules.Module):
    def __init__(self, instance):
        super().__init__(
            self.__class__.__name__,
            instance,
            needs_db=True,
            needs_msgbus=True,
            needs_mailer=False,
            needs_payment=True,
            tasks=[self._web_server]
        )
        self.params={}
        self.params['http_listen_port']=int(config.get(options.HTTP_LISTEN_PORT))+self.instance if config.get(options.HTTP_LISTEN_PORT) else None
        self.params['http_listen_address']=config.get(options.HTTP_LISTEN_ADDRESS) if config.get(options.HTTP_LISTEN_ADDRESS) else ""

    async def _web_server(self, start=True):
        if start:
            AsyncIOMainLoop().install()
            self.app = webapp.Application()
            self.http_server = HTTPServer(self.app)
            self.http_server.listen(self.params['http_listen_port'], address=self.params['http_listen_address'])
        else:
            self.http_server.stop()
            logging.logger.info('Web server stopped')

def get_module(instance):
    mod = Webserver(instance=instance)
    return mod

