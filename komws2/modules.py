#coding: utf-8

import sections, options
import webapp
from komcass import connection as casscon
from komapp import modules
from komfig import logger, config
from komimc import bus as msgbus
import tornado.httpserver
import tornado.ioloop


class Webserver(modules.Module):
    def __init__(self, instance_number):
        super(Webserver,self).__init__(self.__class__.__name__, instance_number)
        self.params={}
        self.params['cassandra_keyspace']=config.config.safe_get(sections.WEBSERVER,options.CASSANDRA_KEYSPACE)
        self.params['cassandra_cluster']=config.config.safe_get(sections.WEBSERVER, options.CASSANDRA_CLUSTER).split(',')[:-1]
        self.params['broker']=config.config.safe_get(sections.WEBSERVER, options.MESSAGE_BROKER)
        if not self.params['broker']:
            self.params['broker']=config.config.safe_get(sections.MAIN, options.MESSAGE_BROKER)
        if config.config.safe_get(sections.WEBSERVER, options.HTTP_LISTEN_PORT):
            self.params['http_listen_port']=int(config.config.safe_get(sections.WEBSERVER, options.HTTP_LISTEN_PORT))+self.instance_number
        else:
            exit()

    def start(self):
        if logger.initialize_logger(self.name+'_'+str(self.instance_number)):
            logger.logger.info('Webserver module started')
        if not self.params['cassandra_keyspace'] or not self.params['cassandra_cluster']:
            logger.logger.error('Cassandra connection configuration keys not found')
        elif not self.params['broker']:
            logger.logger.error('Key '+options.MESSAGE_BROKER+' not found')
        else:
            logger.logger.info('Cassandra params: '+str(self.params['cassandra_cluster'])+' '+self.params['cassandra_keyspace'])
            casscon.initialize_session(self.params['cassandra_cluster'],self.params['cassandra_keyspace'])
            msgbus.initialize_msgbus(self.params['broker'], self.name, self.instance_number, self.hostname)
            self.__loop()
        logger.logger.info('Webserver module exiting')
 
    def __loop(self):
        http_server = tornado.httpserver.HTTPServer(webapp.Application())
        http_server.listen(self.params['http_listen_port'])
        tornado.ioloop.IOLoop.instance().start()

