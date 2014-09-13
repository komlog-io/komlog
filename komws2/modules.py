#!/usr/bin/env python
#coding: utf-8

import tornado.web
from tornado.template import Template
from tornado.escape import json_encode,json_decode,xhtml_escape
import os
import datetime
import dateutil.parser

class UserHeaderModule(tornado.web.UIModule):
    def render(self):
        return self.render_string('modules/header.html',date=datetime.datetime.now().strftime("%d %B %Y"))
    
class ErrorHelperModule(tornado.web.UIModule):
    def render(self,errorcode):
        return self.render_string('modules/errorhelper.html',errorcode=errorcode)    

class UserProfileModule(tornado.web.UIModule):
    def render(self,data):
        return self.render_string('modules/userprofile.html',data=data)

