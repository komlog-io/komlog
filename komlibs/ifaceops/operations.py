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
            3:('quo_static_ds_total_datapoints','quo_static_agent_total_datapoints','quo_static_user_total_datapoints'),
            4:('quo_static_user_total_widgets',),
            5:('quo_static_user_total_dashboards',),
            }

OPIDAUTHS={0:('user_agent_perms',),
           1:('user_graph_perms',),
           2:('user_ds_perms','agent_ds_perms'),
           3:('user_dtp_perms',),
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
        for key,value in params.iteritems():
            if not type(value) in ('str','unicode'):
                params[key]=str(value)
        return json.dumps(params)

class NewAgentOperation(WIFaceOperation):
    def __init__(self, uid, aid):
        self.oid=OPID[self.__class__.__name__]
        self.opclass=self.__class__.__name__
        self.params={}
        self.params['uid']=uid if type(uid)==uuid.UUID else uuid.UUID(uid)
        self.params['aid']=aid if type(aid)==uuid.UUID else uuid.UUID(aid)

class NewGraphOperation(WIFaceOperation):
    def __init__(self, uid, gid):
        self.oid=OPID[self.__class__.__name__]
        self.opclass=self.__class__.__name__
        self.params={}
        self.params['uid']=uid if type(uid)==uuid.UUID else uuid.UUID(uid)
        self.params['gid']=gid if type(gid)==uuid.UUID else uuid.UUID(gid)

class NewDatasourceOperation(WIFaceOperation):
    def __init__(self, uid, aid, did):
        self.oid=OPID[self.__class__.__name__]
        self.opclass=self.__class__.__name__
        self.params={}
        self.params['uid']=uid if type(uid)==uuid.UUID else uuid.UUID(uid)
        self.params['aid']=aid if type(aid)==uuid.UUID else uuid.UUID(aid)
        self.params['did']=did if type(did)==uuid.UUID else uuid.UUID(did)

class NewDatapointOperation(WIFaceOperation):
    def __init__(self, uid, aid, did, pid):
        self.oid=OPID[self.__class__.__name__]
        self.opclass=self.__class__.__name__
        self.params={}
        self.params['uid']=uid if type(uid)==uuid.UUID else uuid.UUID(uid)
        self.params['aid']=aid if type(aid)==uuid.UUID else uuid.UUID(aid)
        self.params['did']=did if type(did)==uuid.UUID else uuid.UUID(did)
        self.params['pid']=pid if type(pid)==uuid.UUID else uuid.UUID(pid)

class NewWidgetOperation(WIFaceOperation):
    def __init__(self, uid, wid):
        self.oid=OPID[self.__class__.__name__]
        self.opclass=self.__class__.__name__
        self.params={}
        self.params['uid']=uid if type(uid)==uuid.UUID else uuid.UUID(uid)
        self.params['wid']=wid if type(wid)==uuid.UUID else uuid.UUID(wid)

