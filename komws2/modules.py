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
    
class NavMenuModule(tornado.web.UIModule):
    def render(self,navitem):
        # Defino la variable con el par nombre-urls
        items = [ {"itemname" : "Home", "itemurl" : "/home"},
                 {"itemname" : "Config", "itemurl" : "/home/config"} 
                ] 
        return self.render_string('modules/navbar.html',items=items,navitem=navitem)

class AgentMenuModule(tornado.web.UIModule):
    def render(self,userdata):
        return self.render_string('modules/agentmenu.html',userdata=userdata)
    
    def embedded_javascript(self):
        return "initTree(\"tree_menu\")"
    
class AgentMenuConfModule(tornado.web.UIModule):
    def render(self,userdata):
        return self.render_string('modules/agentconfmenu.html',userdata=userdata)
    
    def embedded_javascript(self):
        return "initTree(\"tree_menu\")"    
    
class ErrorHelperModule(tornado.web.UIModule):
    def render(self,errorcode):
        return self.render_string('modules/errorhelper.html',errorcode=errorcode)    