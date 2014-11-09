#coding: utf-8

import webapp
from komcass import connection as casscon
from komapp import modules
from komfig import logger, config, options
from komimc import bus as msgbus
import tornado.httpserver
import tornado.ioloop


class Webserver(modules.Module):
    def __init__(self, instance_number):
        super(Webserver,self).__init__(self.__class__.__name__, instance_number)
        self.params={}
        self.params['http_listen_port']=int(config.get(options.HTTP_LISTEN_PORT))+self.instance_number if config.get(options.HTTP_LISTEN_PORT) else None

    def start(self):
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
        self.__loop()
        logger.logger.info('Webserver module exiting')
 
    def __loop(self):
        http_server = tornado.httpserver.HTTPServer(webapp.Application())
        http_server.listen(self.params['http_listen_port'])
        tornado.ioloop.IOLoop.instance().start()

