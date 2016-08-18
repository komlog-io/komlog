'''
Created on 01/10/2014

@author: komlog crew
'''

class UserSegment:
    def __init__(self, sid, description=None):
        self.sid=sid
        self.description=description

class UserSegmentQuo:
    def __init__(self, sid, quote, value):
        self.sid=sid
        self.quote=quote
        self.value=value

