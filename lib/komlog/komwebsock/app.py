import tornado.web
from komlog.komwebsock import settings, handlers
from komlog.komcass import connection as casscon
from komlog.komimc import bus
from komlog.komfig import logging, config, options

class Application(tornado.web.Application):
    def __init__(self):
        autoreload = config.get(options.WS_AUTORELOAD)
        autoreload = True if autoreload and autoreload.lower() == 'true' else False
        debug = config.get(options.LOG_LEVEL)
        debug = True if debug and debug.lower() == 'debug' else False
        logging.logger.debug('Initializing Application')
        logging.logger.debug(str(settings.SETTINGS))
        logging.logger.debug('Tornado debug_mode: '+str(debug))
        logging.logger.debug('autoreload: '+str(autoreload))
        tornado.web.Application.__init__(self, handlers.HANDLERS, debug=debug, autorelaod=autoreload, **settings.SETTINGS)
