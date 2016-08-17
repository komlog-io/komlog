'''
Created on 01/10/2014

@author: komlog crew
'''

class UserIfaceDeny:
    ''' This class is used to register interfaces whose access is denied to user requests'''
    def __init__(self, uid, interface, content=None):
        self.uid=uid
        self.interface=interface
        self.content=content

class UserIfaceTsDeny:
    ''' This class is used to register interfaces whose access is denied to user requests in different time intervals '''
    def __init__(self, uid, interface, ts, content=None):
        self.uid=uid
        self.interface=interface
        self.ts=ts
        self.content=content

