import signal
import time
from komlog.komws2 import webapp
from komlog.komcass import connection as casscon
from komlog.komapp.modules import modules
from komlog.komfig import logger, config, options
from komlog.komimc import bus as msgbus
from tornado.httpserver import HTTPServer
from tornado.ioloop import IOLoop


class Webserver(modules.Module):
    def __init__(self, instance_number):
        super(Webserver,self).__init__(self.__class__.__name__, instance_number)
        self.params={}
        self.params['http_listen_port']=int(config.get(options.HTTP_LISTEN_PORT))+self.instance_number if config.get(options.HTTP_LISTEN_PORT) else None

    def signal_handler(self, signum, frame):
        if signum == signal.SIGTERM:
            logger.logger.info('SIGTERM received, terminating')
            now=time.time()
            self.ioloop.add_timeout(now+2,self.shutdown_ioloop)
        else:
            logger.logger.info('signal '+str(signum)+' received, ignoring')

    def start(self):
        signal.signal(signal.SIGTERM,self.signal_handler)
        if not logger.initialize_logger(self.name+'_'+str(self.instance_number)):
            exit()
        logger.logger.info('Module started')
        if not casscon.initialize_session():
            logger.logger.error('Error initializing cassandra session')
            exit()
        if not msgbus.initialize_msgbus(self.name, self.instance_number, self.hostname):
            logger.logger.error('Error initializing broker session')
            exit()
        if not self.params['http_listen_port']:
            logger.logger.error('Key '+options.HTTP_LISTEN_PORT+' not found')
            exit()
        self.loop()
        self.terminate()
 
    def loop(self):
        self.app = webapp.Application()
        self.http_server = HTTPServer(self.app)
        self.http_server.listen(self.params['http_listen_port'])
        self.ioloop = IOLoop.instance()
        self.ioloop.start()

    def shutdown_ioloop(self):
        logger.logger.info('Stopping HTTP server')
        self.http_server.stop()
        deadline = time.time() + 60
        def stop_loop():
            now = time.time()
            logger.logger.info('waiting for ioloop finishing requests')
            if now < deadline and self.ioloop._callbacks:
                self.ioloop.add_timeout(now+1, stop_loop)
            elif not self.ioloop._callbacks:
                self.ioloop.stop()
                logger.logger.info('ioloop stopped')
            elif now > deadline:
                logger.logger.info('Timeout expired waiting for ioloop shutdown, forcing it')
                self.ioloop.stop()
                logger.logger.info('ioloop stopped')
        stop_loop()

