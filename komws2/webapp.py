#!/usr/bin/env python
#coding: utf-8

import tornado.web
from komws2 import settings, handlers
from komcass import connection as casscon
from komimc import bus
from komfig import logger, config, options

class Application(tornado.web.Application):
    def __init__(self):
        self.dest_dir=config.get(options.SAMPLES_RECEIVED_PATH)
        logger.logger.debug('Initializing Application')
        logger.logger.debug('dest path: '+str(self.dest_dir))
        logger.logger.debug(str(settings.SETTINGS))
        tornado.web.Application.__init__(self, handlers.HANDLERS, **settings.SETTINGS)

