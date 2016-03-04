import tornado.web
from komwebsock import settings, handlers
from komcass import connection as casscon
from komimc import bus
from komfig import logger

class Application(tornado.web.Application):
    def __init__(self):
        logger.logger.debug('Initializing Application')
        logger.logger.debug(str(settings.SETTINGS))
        tornado.web.Application.__init__(self, handlers.HANDLERS, **settings.SETTINGS)

