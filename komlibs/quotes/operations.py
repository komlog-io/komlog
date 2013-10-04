#coding:utf-8
'''
 operations.py

 This file contains classes and functions related with qoute operations
 We associate user operations with qoutes, so that we can
 update user resource utilization and control access based on this

 author: jcazor
 date: 2013/09/29
'''

import json
import uuid

OPID={'NewAgentQuoteOperation':0,
      'NewGraphQuoteOperation':1,
      'NewDatasourceQuoteOperation':2,
      'NewDatapointQuoteOperation':3}

OPIDQUOTES={0:('quo_static_user_total_agents',),
            1:('quo_static_user_total_graphs',),
            2:('quo_static_agent_total_datasources','quo_static_user_total_datasources'),
            3:('quo_static_ds_total_datapoints','quo_static_agent_total_datapoints','quo_static_user_total_datapoints')}


class QuoteOperation:
    def __init__(self):
        pass

    def get_operationid(self):
        return self.oid 
    
    def get_quotes_to_update(self):
        return OPIDQUOTES[self.oid]

    def get_params(self):
        return self.params

    def get_json_serialization(self):
        params=self.params
        params['opclass']=self.opclass
        for key,value in params.iteritems():
            if not type(value) in ('str','unicode'):
                params[key]=str(value)
        return json.dumps(params)

class NewAgentQuoteOperation(QuoteOperation):
    def __init__(self, uid):
        self.oid=OPID[self.__class__.__name__]
        self.opclass=self.__class__.__name__
        self.params={}
        if type(uid)==uuid.UUID:
            self.params['uid']=uid
        else:
            self.params['uid']=uuid.UUID(uid)

class NewGraphQuoteOperation(QuoteOperation):
    def __init__(self, uid):
        self.oid=OPID[self.__class__.__name__]
        self.opclass=self.__class__.__name__
        self.params={}
        if type(uid)==uuid.UUID:
            self.params['uid']=uid
        else:
            self.params['uid']=uuid.UUID(uid)

class NewDatasourceQuoteOperation(QuoteOperation):
    def __init__(self, uid, aid):
        self.oid=OPID[self.__class__.__name__]
        self.opclass=self.__class__.__name__
        self.params={}
        self.params['uid']=uid if type(uid)==uuid.UUID else uuid.UUID(uid)
        self.params['aid']=aid if type(aid)==uuid.UUID else uuid.UUID(aid)

class NewDatapointQuoteOperation(QuoteOperation):
    def __init__(self, uid, aid, did):
        self.oid=OPID[self.__class__.__name__]
        self.opclass=self.__class__.__name__
        self.params={}
        self.params['uid']=uid if type(uid)==uuid.UUID else uuid.UUID(uid)
        self.params['aid']=aid if type(aid)==uuid.UUID else uuid.UUID(aid)
        self.params['did']=did if type(did)==uuid.UUID else uuid.UUID(did)

