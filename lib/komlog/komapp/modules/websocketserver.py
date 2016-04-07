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
from komlog.komwebsock import app
from tornado.httpserver import HTTPServer
from tornado.platform.asyncio import AsyncIOMainLoop


loop = asyncio.get_event_loop()

class Websocketserver(modules.Module):
    def __init__(self, instance_number):
        super(Websocketserver,self).__init__(self.__class__.__name__, instance_number)
        self.params={}
        self.params['ws_listen_port']=int(config.get(options.WS_LISTEN_PORT))+self.instance_number if config.get(options.WS_LISTEN_PORT) else None

    def signal_handler(self, signum):
        if signum == signal.SIGTERM:
            logging.logger.info('SIGTERM received, terminating')
            self.shutdown()
        else:
            logging.logger.info('signal '+str(signum)+' received, ignoring')

    def start(self):
        loop.add_signal_handler(signal.SIGTERM,\
            functools.partial(self.signal_handler, signal.SIGTERM))
        if not logging.initialize_logging(self.name+'_'+str(self.instance_number)):
            exit()
        logging.logger.info('Module started')
        if not casscon.initialize_session():
            logging.logger.error('Error initializing cassandra session')
            exit()
        if not msgbus.initialize_msgbus(self.name, self.instance_number, self.hostname):
            logging.logger.error('Error initializing broker session')
            exit()
        if not self.params['ws_listen_port']:
            logging.logger.error('Key '+options.WS_LISTEN_PORT+' not found')
            exit()
        self.loop()
        self.terminate()
 
    def loop(self):
        AsyncIOMainLoop().install()
        self.app = app.Application()
        self.http_server = HTTPServer(self.app)
        self.http_server.listen(self.params['ws_listen_port'])
        try:
            loop.run_forever()
        finally:
            loop.close()

    def shutdown(self):
        logging.logger.info('Stopping Webagent HTTP server')
        self.http_server.stop()
        deadline = loop.time() + 15
        def stop_loop():
            now = loop.time()
            logging.logger.info('waiting for loop finishing requests')
            if now < deadline and len(asyncio.Task.all_tasks())>0:
                loop.call_later(1, stop_loop)
            elif len(asyncio.Task.all_tasks())==0:
                loop.stop()
                logging.logger.info('loop stopped')
            elif now > deadline:
                logging.logger.info('Timeout expired waiting for loop shutdown, forcing it')
                loop.stop()
                logging.logger.info('loop stopped')
        stop_loop()

