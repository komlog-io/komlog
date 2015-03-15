#coding: utf-8
'''
Created on 01/10/2014

@author: komlog crew
'''

class Quote(object):
    def __init__(self, quotes=None):
        self.quotes=quotes if quotes else {}

    def get_quote(self, quote):
        if quote and quote in self.quotes:
            return self.quotes[quote]
        else:
            return None

class UserQuo(Quote):
    def __init__(self,uid, quotes=None):
        self.uid=uid
        super(UserQuo,self).__init__(quotes)

class AgentQuo(Quote):
    def __init__(self,aid, quotes=None):
        self.aid=aid
        super(AgentQuo,self).__init__(quotes)

class DatasourceQuo(Quote):
    def __init__(self,did, quotes=None):
        self.did=did
        super(DatasourceQuo,self).__init__(quotes)

class DatapointQuo(Quote):
    def __init__(self,pid, quotes=None):
        self.pid=pid
        super(DatapointQuo,self).__init__(quotes)

class WidgetQuo(Quote):
    def __init__(self,wid, quotes=None):
        self.wid=wid
        super(WidgetQuo,self).__init__(quotes)

class DashboardQuo(Quote):
    def __init__(self,bid, quotes=None):
        self.bid=bid
        super(DashboardQuo,self).__init__(quotes)

class CircleQuo(Quote):
    def __init__(self,cid, quotes=None):
        self.cid=cid
        super(CircleQuo,self).__init__(quotes)

