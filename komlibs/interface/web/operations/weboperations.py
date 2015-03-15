#coding:utf-8
'''
operations.py

This file contains classes and functions related with web interface operations (operation=requests done)
We associate web operations with auth operations, so that we can
update user resource utilization and control access based on this

'''

import json
import uuid
from komlibs.general.validation import arguments
from komlibs.auth import operations

NEW_AGENT             = 0
NEW_DATASOURCE        = 1
NEW_DATAPOINT         = 2
NEW_WIDGET            = 3
NEW_DASHBOARD         = 4
NEW_WIDGET_SYSTEM     = 5
NEW_SNAPSHOT          = 6
NEW_CIRCLE            = 7
DELETE_USER           = 8
DELETE_AGENT          = 9
DELETE_DATASOURCE     = 10
DELETE_DATAPOINT      = 11
DELETE_WIDGET         = 12
DELETE_DASHBOARD      = 13
DELETE_SNAPSHOT       = 14
DELETE_CIRCLE         = 15
UPDATE_CIRCLE_MEMBERS = 16


OPAUTHS={NEW_AGENT:operations.NEW_AGENT,
         NEW_DATASOURCE:operations.NEW_DATASOURCE,
         NEW_DATAPOINT:operations.NEW_DATAPOINT,
         NEW_WIDGET:operations.NEW_WIDGET,
         NEW_DASHBOARD:operations.NEW_DASHBOARD,
         NEW_WIDGET_SYSTEM:operations.NEW_WIDGET_SYSTEM,
         NEW_SNAPSHOT:operations.NEW_SNAPSHOT,
         NEW_CIRCLE:operations.NEW_CIRCLE,
         DELETE_USER: operations.DELETE_USER,
         DELETE_AGENT: operations.DELETE_AGENT,
         DELETE_DATASOURCE: operations.DELETE_DATASOURCE,
         DELETE_DATAPOINT: operations.DELETE_DATAPOINT,
         DELETE_WIDGET: operations.DELETE_WIDGET,
         DELETE_DASHBOARD: operations.DELETE_DASHBOARD,
         DELETE_SNAPSHOT:operations.DELETE_SNAPSHOT,
         DELETE_CIRCLE:operations.DELETE_CIRCLE,
         UPDATE_CIRCLE_MEMBERS:operations.UPDATE_CIRCLE_MEMBERS,
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

class NewAgentOperation(WIFaceOperation):
    def __init__(self, uid, aid):
        self.oid=NEW_AGENT
        self.params={}
        self.params['uid']=uid
        self.params['aid']=aid

class NewDatasourceOperation(WIFaceOperation):
    def __init__(self, uid, aid, did):
        self.oid=NEW_DATASOURCE
        self.params={}
        self.params['uid']=uid
        self.params['aid']=aid
        self.params['did']=did

class NewDatapointOperation(WIFaceOperation):
    def __init__(self, uid, aid, did, pid):
        self.oid=NEW_DATAPOINT
        self.params={}
        self.params['uid']=uid
        self.params['aid']=aid
        self.params['did']=did
        self.params['pid']=pid

class NewWidgetOperation(WIFaceOperation):
    def __init__(self, uid, wid):
        self.oid=NEW_WIDGET
        self.params={}
        self.params['uid']=uid
        self.params['wid']=wid

class NewDashboardOperation(WIFaceOperation):
    def __init__(self, uid, bid):
        self.oid=NEW_DASHBOARD
        self.params={}
        self.params['uid']=uid
        self.params['bid']=bid

class NewWidgetSystemOperation(WIFaceOperation):
    def __init__(self, uid, wid):
        self.oid=NEW_WIDGET_SYSTEM
        self.params={}
        self.params['uid']=uid
        self.params['wid']=wid

class NewSnapshotOperation(WIFaceOperation):
    def __init__(self, uid, wid, nid):
        self.oid=NEW_SNAPSHOT
        self.params={}
        self.params['uid']=uid
        self.params['wid']=wid
        self.params['nid']=nid

class NewCircleOperation(WIFaceOperation):
    def __init__(self, uid, cid):
        self.oid=NEW_CIRCLE
        self.params={}
        self.params['uid']=uid
        self.params['cid']=cid

class DeleteUserOperation(WIFaceOperation):
    def __init__(self, uid, aids):
        self.oid=DELETE_USER
        self.params={}
        self.params['uid']=uid
        self.params['aids']=aids

class DeleteAgentOperation(WIFaceOperation):
    def __init__(self, uid, aid):
        self.oid=DELETE_AGENT
        self.params={}
        self.params['uid']=uid
        self.params['aid']=aid

class DeleteDatasourceOperation(WIFaceOperation):
    def __init__(self, uid, aid, did, pids):
        self.oid=DELETE_DATASOURCE
        self.params={}
        self.params['uid']=uid
        self.params['aid']=aid
        self.params['did']=did
        self.params['pids']=pids

class DeleteDatapointOperation(WIFaceOperation):
    def __init__(self, uid, aid, pid):
        self.oid=DELETE_DATAPOINT
        self.params={}
        self.params['uid']=uid
        self.params['aid']=aid
        self.params['pid']=pid

class DeleteWidgetOperation(WIFaceOperation):
    def __init__(self, uid, wid):
        self.oid=DELETE_WIDGET
        self.params={}
        self.params['uid']=uid
        self.params['wid']=wid

class DeleteDashboardOperation(WIFaceOperation):
    def __init__(self, uid, bid):
        self.oid=DELETE_DASHBOARD
        self.params={}
        self.params['uid']=uid
        self.params['bid']=bid

class DeleteSnapshotOperation(WIFaceOperation):
    def __init__(self, uid, nid):
        self.oid=DELETE_SNAPSHOT
        self.params={}
        self.params['uid']=uid
        self.params['nid']=nid

class DeleteCircleOperation(WIFaceOperation):
    def __init__(self, uid, cid):
        self.oid=DELETE_CIRCLE
        self.params={}
        self.params['uid']=uid
        self.params['cid']=cid

class UpdateCircleMembersOperation(WIFaceOperation):
    def __init__(self, cid):
        self.oid=UPDATE_CIRCLE_MEMBERS
        self.params={}
        self.params['cid']=cid

