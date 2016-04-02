import tornado.web
from komlog.komwebsock import settings, handlers
from komlog.komcass import connection as casscon
from komlog.komimc import bus
from komlog.komfig import logger

class Application(tornado.web.Application):
    def __init__(self):
        logger.logger.debug('Initializing Application')
        logger.logger.debug(str(settings.SETTINGS))
        tornado.web.Application.__init__(self, handlers.HANDLERS, **settings.SETTINGS)

