#!/usr/bin/env python
#coding: utf-8

import os.path
import tornado.httpserver
import tornado.ioloop
import tornado.options
import tornado.web
import settings
import handlers
import modules
import logging
from komcass import connection as casscon
from komimc import bus

from tornado.options import define, options
define("port", default=8000, help="run on the given port", type=int)

static_path = '/home/komlog/komlog/komws2/static/'
#favicon_path = '/home/komlog/komlog/komws2/static/favicon.ico'

UUID4_REGEX='[0-9a-f]{8}-[0-9a-f]{4}-[0-9a-f]{4}-[0-9a-f]{4}-[0-9a-f]{12}'
class Application(tornado.web.Application):
    def __init__(self):
        handler_list = [(r"/login/?", handlers.LoginHandler),
                    (r"/logout/?", handlers.LogoutHandler),
                    (r"/etc/agent/("+UUID4_REGEX+")", handlers.AgentConfigHandler),
                    (r"/etc/agent/?", handlers.AgentCreationHandler),
                    (r"/etc/ds/?", handlers.DatasourceCreationHandler),
                    (r"/etc/ds/("+UUID4_REGEX+")", handlers.DatasourceConfigHandler),
                    (r"/etc/dp/?", handlers.DatapointCreationHandler),
                    (r"/etc/dp/("+UUID4_REGEX+")", handlers.DatapointConfigHandler),
                    (r"/etc/graph/?", handlers.GraphCreationHandler),
                    (r"/etc/graph/("+UUID4_REGEX+")", handlers.GraphConfigHandler),
                    (r"/etc/usr/confirm/", handlers.UserConfirmationHandler),
                    (r"/etc/usr/?", handlers.UserCreationHandler),
                    (r"/var/ds/("+UUID4_REGEX+")", handlers.DatasourceDataHandler),
                    (r"/var/dp/("+UUID4_REGEX+")", handlers.DatapointDataHandler),
                    (r"/var/static/plot/("+UUID4_REGEX+")", handlers.PlotDataHandler),
#                     (r"/home/(\w+)/config", handlers.UserConfigHandler),
#                     (r"/home/(\w+)", handlers.UserHomeHandler)]
                    (r"/home/config", handlers.UserConfigHandler),
                    (r"/home", handlers.UserHomeHandler)]
                # Listado de modulos de interfaz
        modules_list = {
              "UserHeader" : modules.UserHeaderModule,
              "NavMenu" : modules.NavMenuModule,
              "AgentMenu" : modules.AgentMenuModule,
              "AgentMenuConf" : modules.AgentMenuConfModule,
              "ErrorHelper" : modules.ErrorHelperModule,
              "CardsHome" : modules.CardsHomeModule
              }
        # Defino la variable settings para manejar mejor las variables de la aplicacion
        settings_vars = {
                        "template_path" : settings.TEMPLATE_PATH,
                        "static_path" : settings.STATIC_PATH,
                        "cookie_secret" : settings.COOKIE_SECRET,
                        "xsrf_cookies" : settings.XSRF_COOKIES,
                        "login_url" : settings.LOGIN_URL,
                        "ui_modules" : modules_list,
                        "debug" : settings.DEBUG
                    }

        keyspace='komlog'
        server_list=('csbe1',)
        pool=casscon.Pool(keyspace,server_list,5)
        self.cf=casscon.CF(pool)
        self.dest_dir='/var/local/komlog/data/received'
        #BUS vars
        broker='localhost'
        name='komws2'
        instance_number='8000'
        hostname='komserver1'
        logger=logging.Logger(name)
        self.mb=bus.MessageBus(broker,name,instance_number,hostname,logger)
        tornado.web.Application.__init__(self, handler_list, **settings_vars)

if __name__ == "__main__":
    tornado.options.parse_command_line()
    http_server = tornado.httpserver.HTTPServer(Application())
    http_server.listen(options.port)
    tornado.ioloop.IOLoop.instance().start()

