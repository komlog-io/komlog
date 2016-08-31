#coding: utf-8
'''
Created on 01/10/2014

@author: komlog crew
'''

class UserQuo:
    def __init__(self,uid, quote, value):
        self.uid=uid
        self.quote=quote
        self.value=value

class AgentQuo:
    def __init__(self,aid, quote, value):
        self.aid=aid
        self.quote=quote
        self.value=value

class DatasourceQuo:
    def __init__(self,did, quote, value):
        self.did=did
        self.quote=quote
        self.value=value

class DatapointQuo:
    def __init__(self,pid, quote, value):
        self.pid=pid
        self.quote=quote
        self.value=value

class WidgetQuo:
    def __init__(self,wid, quote, value):
        self.wid=wid
        self.quote=quote
        self.value=value

class DashboardQuo:
    def __init__(self,bid, quote, value):
        self.bid=bid
        self.quote=quote
        self.value=value

class CircleQuo:
    def __init__(self,cid, quote, value):
        self.cid=cid
        self.quote=quote
        self.value=value

class UserTsQuo:
    def __init__(self,uid, quote, ts, value):
        self.uid=uid
        self.quote=quote
        self.ts=ts
        self.value=value

class DatasourceTsQuo:
    def __init__(self,did, quote, ts, value):
        self.did=did
        self.quote=quote
        self.ts=ts
        self.value=value

class DatapointTsQuo:
    def __init__(self, pid, quote, ts, value):
        self.pid=pid
        self.quote=quote
        self.ts=ts
        self.value=value

