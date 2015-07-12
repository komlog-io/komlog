#coding: utf-8
'''
Created on 01/10/2014

@author: komlog crew
'''

class UserEvent:
    def __init__(self, uid, date, active, priority, type, parameters=None):
        self.uid=uid
        self.date=date
        self.active=active
        self.priority=priority
        self.type=type
        self.parameters=parameters if parameters else dict()

