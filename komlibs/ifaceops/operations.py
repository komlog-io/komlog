#coding:utf-8
'''
 operations.py

 This file contains classes and functions related with web interface operations (operation=requests done)
 We associate user operations with qoutes, so that we can
 update user resource utilization and control access based on this
 We also associate operations to resources, so the authorization schema can be generated.

 author: jcazor
 date: 2013/09/29
'''

import json
import uuid
from komlibs.general.validation import arguments

OPID={'NewAgentOperation':0,
      'NewGraphOperation':1,
      'NewDatasourceOperation':2,
      'NewDatapointOperation':3,
      'NewWidgetOperation':4,
      'NewDashboardOperation':5
      }

OPIDQUOTES={0:('quo_static_user_total_agents',),
            1:('quo_static_user_total_graphs',),
            2:('quo_static_agent_total_datasources','quo_static_user_total_datasources'),
            3:('quo_static_datasource_total_datapoints','quo_static_agent_total_datapoints','quo_static_user_total_datapoints'),
            4:('quo_static_user_total_widgets',),
            5:('quo_static_user_total_dashboars',),
            }

OPIDAUTHS={0:('user_agent_perms',),
           1:('user_graph_perms',),
           2:('user_datasource_perms','agent_datasource_perms'),
           3:('user_datapoint_perms',),
           4:('user_widget_perms',),
           5:('user_dashboard_perms',),
           }



class WIFaceOperation:
    def __init__(self):
        pass

    def get_operationid(self):
        return self.oid 
    
    def get_quotes_to_update(self):
        return OPIDQUOTES[self.oid]

    def get_auths_to_update(self):
        return OPIDAUTHS[self.oid]

    def get_params(self):
        return self.params

    def get_json_serialization(self):
        params=self.params
        params['opclass']=self.opclass
        for key,value in params.items():
            if not type(value) in ('str','unicode'):
                params[key]=str(value)
        return json.dumps(params)

class NewAgentOperation(WIFaceOperation):
    def __init__(self, uid, aid):
        self.oid=OPID[self.__class__.__name__]
        self.opclass=self.__class__.__name__
        self.params={}
        self.params['uid']=uid if arguments.is_valid_uuid(uid) else uuid.UUID(uid)
        self.params['aid']=aid if arguments.is_valid_uuid(aid) else uuid.UUID(aid)

class NewDatasourceOperation(WIFaceOperation):
    def __init__(self, uid, aid, did):
        self.oid=OPID[self.__class__.__name__]
        self.opclass=self.__class__.__name__
        self.params={}
        self.params['uid']=uid if arguments.is_valid_uuid(uid) else uuid.UUID(uid)
        self.params['aid']=aid if arguments.is_valid_uuid(aid) else uuid.UUID(aid)
        self.params['did']=did if arguments.is_valid_uuid(did) else uuid.UUID(did)

class NewDatapointOperation(WIFaceOperation):
    def __init__(self, uid, aid, did, pid):
        self.oid=OPID[self.__class__.__name__]
        self.opclass=self.__class__.__name__
        self.params={}
        self.params['uid']=uid if arguments.is_valid_uuid(uid) else uuid.UUID(uid)
        self.params['aid']=aid if arguments.is_valid_uuid(aid) else uuid.UUID(aid)
        self.params['did']=did if arguments.is_valid_uuid(did) else uuid.UUID(did)
        self.params['pid']=pid if arguments.is_valid_uuid(pid) else uuid.UUID(pid)

class NewWidgetOperation(WIFaceOperation):
    def __init__(self, uid, wid):
        self.oid=OPID[self.__class__.__name__]
        self.opclass=self.__class__.__name__
        self.params={}
        self.params['uid']=uid if arguments.is_valid_uuid(uid) else uuid.UUID(uid)
        self.params['wid']=uid if arguments.is_valid_uuid(wid) else uuid.UUID(wid)

class NewDashboardOperation(WIFaceOperation):
    def __init__(self, uid, bid):
        self.oid=OPID[self.__class__.__name__]
        self.opclass=self.__class__.__name__
        self.params={}
        self.params['uid']=uid if arguments.is_valid_uuid(uid) else uuid.UUID(uid)
        self.params['bid']=uid if arguments.is_valid_uuid(bid) else uuid.UUID(bid)

