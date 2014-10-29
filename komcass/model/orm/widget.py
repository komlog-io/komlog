#coding: utf-8
'''
Created on 01/10/2014

@author: komlog crew
'''

from komcass.model.parametrization.widget import types

class Widget(object):
    def __init__(self,wid,uid,type):
        self.wid=wid
        self.uid=uid
        self.type=type

class WidgetDs(Widget):
    def __init__(self,wid,uid,creation_date,did):
        self.creation_date=creation_date
        self.did=did
        super(WidgetDs,self).__init__(wid,uid,types.WIDGET_DS)

class WidgetDp(Widget):
    def __init__(self,wid,uid,creation_date,pid):
        self.creation_date=creation_date
        self.pid=pid
        super(WidgetDp,self).__init__(wid,uid,types.WIDGET_DP)


