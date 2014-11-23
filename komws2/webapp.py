#!/usr/bin/env python
#coding: utf-8

import tornado.web
from komws2 import settings, handlers
from komcass import connection as casscon
from komimc import bus
from komfig import logger

class Application(tornado.web.Application):
    def __init__(self):
        self.dest_dir='/var/local/komlog/data/received'
        logger.logger.debug('Initializing Application')
        logger.logger.debug(str(settings.SETTINGS))
        tornado.web.Application.__init__(self, handlers.HANDLERS, **settings.SETTINGS)

