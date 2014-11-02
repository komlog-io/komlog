#!/usr/bin/env python
#coding: utf-8

import tornado.web
import settings
import handlers
from komcass import connection as casscon
from komimc import bus

class Application(tornado.web.Application):
    def __init__(self):
        self.dest_dir='/var/local/komlog/data/received'
        tornado.web.Application.__init__(self, handlers.HANDLERS, **settings.SETTINGS)

