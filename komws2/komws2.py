#!/usr/bin/env python
#coding: utf-8

import os.path
import tornado.httpserver
import tornado.ioloop
import tornado.options
import tornado.web
from komcass import connection as casscon
import handlers

from tornado.options import define, options
define("port", default=8000, help="run on the given port", type=int)

static_path = '/home/komlog/komlog/komws2/static/'
#favicon_path = '/home/komlog/komlog/komws2/static/favicon.ico'

UUID4_REGEX='[0-9a-f]{8}-[0-9a-f]{4}-[0-9a-f]{4}-[0-9a-f]{4}-[0-9a-f]{12}'
class Application(tornado.web.Application):
    def __init__(self):
        handler_list = [(r"/etc/agent/("+UUID4_REGEX+")", handlers.AgentConfigHandler),
                    (r"/etc/agent/", handlers.AgentCreationHandler),
                    (r"/etc/ds/("+UUID4_REGEX+")", handlers.DatasourceConfigHandler),
                    (r"/home/(\w+)/config", handlers.UserConfigHandler),
                    (r"/home/(\w+)", handlers.UserHomeHandler),
                    (r'/static/(.*)', tornado.web.StaticFileHandler),
                    (r"/var/ds/("+UUID4_REGEX+")", handlers.DatasourceDataHandler)]
        template_path=os.path.join(os.path.dirname(__file__), "templates")
        keyspace='komlog'
        server_list=('csbe1',)
        pool=casscon.Pool(keyspace,server_list,5)
        self.cf=casscon.CF(pool)
        self.dest_dir='/home/komlog/data/received'
        tornado.web.Application.__init__(self, handler_list, static_path=static_path,template_path=template_path,debug=True)

if __name__ == "__main__":
    tornado.options.parse_command_line()
    http_server = tornado.httpserver.HTTPServer(Application())
    http_server.listen(options.port)
    tornado.ioloop.IOLoop.instance().start()

