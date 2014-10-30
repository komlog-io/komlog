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


UUID4_REGEX='[0-9a-f]{8}-[0-9a-f]{4}-[0-9a-f]{4}-[0-9a-f]{4}-[0-9a-f]{12}'
class Application(tornado.web.Application):
    def __init__(self):
        handler_list = [(r"/login/?", handlers.LoginHandler),
                    (r"/logout/?", handlers.LogoutHandler),
                    (r"/etc/ag/?", handlers.AgentsHandler),
                    (r"/etc/ag/("+UUID4_REGEX+")", handlers.AgentConfigHandler),
                    (r"/etc/ds/?", handlers.DatasourcesHandler),
                    (r"/etc/ds/("+UUID4_REGEX+")", handlers.DatasourceConfigHandler),
                    (r"/etc/dp/?", handlers.DatapointsHandler),
                    (r"/etc/dp/("+UUID4_REGEX+")", handlers.DatapointConfigHandler),
                    (r"/etc/graph/?", handlers.GraphsHandler),
                    (r"/etc/graph/("+UUID4_REGEX+")", handlers.GraphConfigHandler),
                    (r"/etc/wg/?", handlers.WidgetsHandler),
                    (r"/etc/wg/("+UUID4_REGEX+")", handlers.WidgetConfigHandler),
                    (r"/etc/db/?", handlers.DashboardsHandler),
                    (r"/etc/db/("+UUID4_REGEX+")", handlers.DashboardConfigHandler),
                    (r"/etc/usr/confirm/", handlers.UserConfirmationHandler),
                    (r"/etc/usr/?", handlers.UsersHandler),
                    (r"/var/ds/("+UUID4_REGEX+")", handlers.DatasourceDataHandler),
                    (r"/var/dp/("+UUID4_REGEX+")", handlers.DatapointDataHandler),
                    (r"/var/static/plot/("+UUID4_REGEX+")", handlers.PlotDataHandler),
                    (r"/home/config", handlers.UserConfigHandler),
                    (r"/home/profile", handlers.UserProfileHandler),
                    (r"/home", handlers.UserHomeHandler)]
                # Listado de modulos de interfaz
        modules_list = {
              "UserHeader" : modules.UserHeaderModule,
              "ErrorHelper" : modules.ErrorHelperModule,
              "UserProfile" : modules.UserProfileModule
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
        server_list=('localhost',)
        casscon.initialize_session(server_list,keyspace)
        self.dest_dir='/var/local/komlog/data/received'
        #BUS vars
        broker='localhost'
        name='komws2'
        instance_number='8000'
        hostname='localhost'
        logger=logging.Logger(name)
        self.mb=bus.MessageBus(broker,name,instance_number,hostname,logger)
        tornado.web.Application.__init__(self, handler_list, **settings_vars)

if __name__ == "__main__":
    tornado.options.parse_command_line()
    http_server = tornado.httpserver.HTTPServer(Application())
    http_server.listen(options.port)
    tornado.ioloop.IOLoop.instance().start()

