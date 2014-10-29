#coding: utf-8
'''
Created on 01/10/2014

@author: komlog crew
'''

class UserAgentPerm:
    ''' This class is used to access User - Agent permission relation '''
    def __init__(self, uid, aid=None, perm=None):
        self.uid=uid
        self.aid=aid
        self.perm=perm

class UserDatasourcePerm:
    ''' This class is used to access User-Datasource permission relation '''
    def __init__(self, uid, did=None, perm=None):
        self.uid=uid
        self.did=did
        self.perm=perm

class UserDatapointPerm:
    ''' This class is used to access User-Datapoint permission relation '''
    def __init__(self, uid, pid=None, perm=None):
        self.uid=uid
        self.pid=pid
        self.perm=perm

class AgentDatasourcePerm:
    ''' This class is used to access Agent-Datasource permission relation '''
    def __init__(self, aid, did=None, perm=None):
        self.aid=aid
        self.did=did
        self.perm=perm

class AgentDatapointPerm:
    ''' This class is used to access Agent-Datapoint permission relation '''
    def __init__(self, aid, pid=None, perm=None ):
        self.aid=aid
        self.pid=pid
        self.perm=perm

class UserWidgetPerm:
    ''' This class is used to access User-Widget permission relation '''
    def __init__(self, uid, wid=None, perm=None):
        self.uid=uid
        self.wid=wid
        self.perm=perm

class UserDashboardPerm:
    ''' This class is used to access User-Dashboard permission relation '''
    def __init__(self, uid, bid=None, perm=None):
        self.uid=uid
        self.bid=bid
        self.perm=perm

