import tornado.web
from komlog.komwebsock import settings, handlers
from komlog.komcass import connection as casscon
from komlog.komimc import bus
from komlog.komfig import logging

class Application(tornado.web.Application):
    def __init__(self):
        logging.logger.debug('Initializing Application')
        logging.logger.debug(str(settings.SETTINGS))
        tornado.web.Application.__init__(self, handlers.HANDLERS, **settings.SETTINGS)

