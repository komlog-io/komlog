#coding:utf-8
'''
operations.py

This file contains classes and functions related with web interface operations (operation=requests done)
We associate web operations with auth operations, so that we can
update user resource utilization and control access based on this

'''

import json
import uuid
from komlog.komlibs.general.validation import arguments
from komlog.komlibs.auth.model.operations import Operations as AuthOperations
from komlog.komlibs.interface.web.model.types import Operations

OPAUTHS={
    Operations.NEW_USER:AuthOperations.NEW_USER,
    Operations.NEW_AGENT:AuthOperations.NEW_AGENT,
    Operations.NEW_DATASOURCE:AuthOperations.NEW_DATASOURCE,
    Operations.NEW_DATASOURCE_DATAPOINT:AuthOperations.NEW_DATASOURCE_DATAPOINT,
    Operations.NEW_WIDGET:AuthOperations.NEW_WIDGET,
    Operations.NEW_DASHBOARD:AuthOperations.NEW_DASHBOARD,
    Operations.NEW_WIDGET_SYSTEM:AuthOperations.NEW_WIDGET_SYSTEM,
    Operations.NEW_SNAPSHOT:AuthOperations.NEW_SNAPSHOT,
    Operations.NEW_CIRCLE:AuthOperations.NEW_CIRCLE,
    Operations.DELETE_USER: AuthOperations.DELETE_USER,
    Operations.DELETE_AGENT: AuthOperations.DELETE_AGENT,
    Operations.DELETE_DATASOURCE: AuthOperations.DELETE_DATASOURCE,
    Operations.DELETE_DATASOURCE_DATAPOINT: AuthOperations.DELETE_DATASOURCE_DATAPOINT,
    Operations.DELETE_USER_DATAPOINT: AuthOperations.DELETE_USER_DATAPOINT,
    Operations.DELETE_WIDGET: AuthOperations.DELETE_WIDGET,
    Operations.DELETE_DASHBOARD: AuthOperations.DELETE_DASHBOARD,
    Operations.DELETE_SNAPSHOT:AuthOperations.DELETE_SNAPSHOT,
    Operations.DELETE_CIRCLE:AuthOperations.DELETE_CIRCLE,
    Operations.DISSOCIATE_DATAPOINT_FROM_DATASOURCE:AuthOperations.DISSOCIATE_DATAPOINT_FROM_DATASOURCE,
    Operations.UPDATE_CIRCLE_MEMBERS:AuthOperations.UPDATE_CIRCLE_MEMBERS,
}

class WIFaceOperation:
    def __init__(self):
        pass

    def get_operationid(self):
        return self.oid 
    
    def get_auth_operation(self):
        return OPAUTHS[self.oid]

    def get_params(self):
        return self.params

class NewUserOperation(WIFaceOperation):
    def __init__(self, uid):
        self.oid=Operations.NEW_USER
        self.params={}
        self.params['uid']=uid

class NewAgentOperation(WIFaceOperation):
    def __init__(self, uid, aid):
        self.oid=Operations.NEW_AGENT
        self.params={}
        self.params['uid']=uid
        self.params['aid']=aid

class NewDatasourceOperation(WIFaceOperation):
    def __init__(self, uid, aid, did):
        self.oid=Operations.NEW_DATASOURCE
        self.params={}
        self.params['uid']=uid
        self.params['aid']=aid
        self.params['did']=did

class NewDatasourceDatapointOperation(WIFaceOperation):
    def __init__(self, uid, aid, did, pid):
        self.oid=Operations.NEW_DATASOURCE_DATAPOINT
        self.params={}
        self.params['uid']=uid
        self.params['aid']=aid
        self.params['did']=did
        self.params['pid']=pid

class NewWidgetOperation(WIFaceOperation):
    def __init__(self, uid, wid):
        self.oid=Operations.NEW_WIDGET
        self.params={}
        self.params['uid']=uid
        self.params['wid']=wid

class NewDashboardOperation(WIFaceOperation):
    def __init__(self, uid, bid):
        self.oid=Operations.NEW_DASHBOARD
        self.params={}
        self.params['uid']=uid
        self.params['bid']=bid

class NewWidgetSystemOperation(WIFaceOperation):
    def __init__(self, uid, wid):
        self.oid=Operations.NEW_WIDGET_SYSTEM
        self.params={}
        self.params['uid']=uid
        self.params['wid']=wid

class NewSnapshotOperation(WIFaceOperation):
    def __init__(self, uid, wid, nid):
        self.oid=Operations.NEW_SNAPSHOT
        self.params={}
        self.params['uid']=uid
        self.params['wid']=wid
        self.params['nid']=nid

class NewCircleOperation(WIFaceOperation):
    def __init__(self, uid, cid):
        self.oid=Operations.NEW_CIRCLE
        self.params={}
        self.params['uid']=uid
        self.params['cid']=cid

class DeleteUserOperation(WIFaceOperation):
    def __init__(self, uid, aids):
        self.oid=Operations.DELETE_USER
        self.params={}
        self.params['uid']=uid
        self.params['aids']=aids

class DeleteAgentOperation(WIFaceOperation):
    def __init__(self, uid, aid):
        self.oid=Operations.DELETE_AGENT
        self.params={}
        self.params['uid']=uid
        self.params['aid']=aid

class DeleteDatasourceOperation(WIFaceOperation):
    def __init__(self, uid, aid, did, pids):
        self.oid=Operations.DELETE_DATASOURCE
        self.params={}
        self.params['uid']=uid
        self.params['aid']=aid
        self.params['did']=did
        self.params['pids']=pids

class DeleteDatasourceDatapointOperation(WIFaceOperation):
    def __init__(self, uid, aid, pid):
        self.oid=Operations.DELETE_DATASOURCE_DATAPOINT
        self.params={}
        self.params['uid']=uid
        self.params['aid']=aid
        self.params['pid']=pid

class DeleteUserDatapointOperation(WIFaceOperation):
    def __init__(self, uid, pid):
        self.oid=Operations.DELETE_USER_DATAPOINT
        self.params={}
        self.params['uid']=uid
        self.params['pid']=pid

class DeleteWidgetOperation(WIFaceOperation):
    def __init__(self, uid, wid):
        self.oid=Operations.DELETE_WIDGET
        self.params={}
        self.params['uid']=uid
        self.params['wid']=wid

class DeleteDashboardOperation(WIFaceOperation):
    def __init__(self, uid, bid):
        self.oid=Operations.DELETE_DASHBOARD
        self.params={}
        self.params['uid']=uid
        self.params['bid']=bid

class DeleteSnapshotOperation(WIFaceOperation):
    def __init__(self, uid, nid):
        self.oid=Operations.DELETE_SNAPSHOT
        self.params={}
        self.params['uid']=uid
        self.params['nid']=nid

class DeleteCircleOperation(WIFaceOperation):
    def __init__(self, uid, cid):
        self.oid=Operations.DELETE_CIRCLE
        self.params={}
        self.params['uid']=uid
        self.params['cid']=cid

class DissociateDatapointFromDatasourceOperation(WIFaceOperation):
    def __init__(self, pid, did):
        self.oid=Operations.DISSOCIATE_DATAPOINT_FROM_DATASOURCE
        self.params={}
        self.params['pid']=pid
        self.params['did']=did

class UpdateCircleMembersOperation(WIFaceOperation):
    def __init__(self, uid, cid):
        self.oid=Operations.UPDATE_CIRCLE_MEMBERS
        self.params={}
        self.params['uid']=uid
        self.params['cid']=cid

