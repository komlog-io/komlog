#coding: utf-8
'''
Created on 01/10/2014

@author: komlog crew
'''

class UserSegment:
    def __init__(self,sid, segmentname, params=None):
        self.sid=sid
        self.segmentname=segmentname
        self.params=params if params else {}

    def get_param(self, param):
        if param and param in self.params:
            return self.params[param]
        else:
            return None



