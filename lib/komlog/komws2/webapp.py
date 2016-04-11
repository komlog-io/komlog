#!/usr/bin/env python
#coding: utf-8

import tornado.web
from komlog.komws2 import settings, handlers
from komlog.komcass import connection as casscon
from komlog.komimc import bus
from komlog.komfig import logging, config, options

class Application(tornado.web.Application):
    def __init__(self):
        self.dest_dir=config.get(options.SAMPLES_RECEIVED_PATH)
        debug = config.get(options.TORNADO_DEBUG)
        debug = True if debug else False
        logging.logger.debug('Initializing Application')
        logging.logger.debug('dest path: '+str(self.dest_dir))
        logging.logger.debug(str(settings.SETTINGS))
        logging.logger.debug('Tornado debug_mode: '+str(debug))
        tornado.web.Application.__init__(self, handlers.HANDLERS, debug=debug, **settings.SETTINGS)

