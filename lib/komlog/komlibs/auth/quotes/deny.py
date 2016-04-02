#coding: utf-8
'''
deny.py 

This file implements functions to deny access to resourcess because of quotes configuration


@author: jcazor
@date: 2013/11/13

'''

from komlog.komcass.api import interface as cassapiiface
from komlog.komfig import logger

interfaces={'User_AgentCreation':'/user/agentcreation/',
            'User_GraphCreation':'/user/graphcreation/',
            'User_DatasourceCreation':'/user/dscreation/',
            'User_DatapointCreation':'/user/dpcreation/',
            'Agent_DatasourceCreation':'/agent/dscreation/',
            'Agent_DatapointCreation':'/agent/dpcreation/',
            'Datasource_DatapointCreation':'/ds/dpcreation/',
            'User_WidgetCreation':'/user/wgcreation/',
            'User_DashboardCreation':'/user/dbcreation/',
            'User_SnapshotCreation':'/user/snapshotcreation/',
            'User_CircleCreation':'/user/circlecreation/',
            'User_AddMemberToCircle':'/user/addmembertocircle/',
           }

DEFAULT_PERM='A'

def quo_static_user_total_agents(params,deny):
    if 'uid' not in params:
        return False
    uid=params['uid']
    iface=interfaces['User_AgentCreation']
    if deny:
        if cassapiiface.insert_user_iface_deny(uid=uid, iface=iface, perm=DEFAULT_PERM):
            return True
    else:
        if cassapiiface.delete_user_iface_deny(uid=uid, iface=iface):
            return True
    return False

def quo_static_user_total_datasources(params,deny):
    if 'uid' not in params:
        return False
    uid=params['uid']
    iface=interfaces['User_DatasourceCreation']
    if deny:
        if cassapiiface.insert_user_iface_deny(uid=uid, iface=iface, perm=DEFAULT_PERM):
            return True
    else:
        if cassapiiface.delete_user_iface_deny(uid=uid, iface=iface):
            return True
    return False

def quo_static_user_total_datapoints(params,deny):
    if 'uid' not in params:
        return False
    uid=params['uid']
    iface=interfaces['User_DatapointCreation']
    if deny:
        if cassapiiface.insert_user_iface_deny(uid=uid, iface=iface, perm=DEFAULT_PERM):
            return True
    else:
        if cassapiiface.delete_user_iface_deny(uid=uid, iface=iface):
            return True
    return False

def quo_static_user_total_widgets(params,deny):
    if 'uid' not in params:
        return False
    uid=params['uid']
    iface=interfaces['User_WidgetCreation']
    if deny:
        if cassapiiface.insert_user_iface_deny(uid=uid, iface=iface, perm=DEFAULT_PERM):
            return True
    else:
        if cassapiiface.delete_user_iface_deny(uid=uid, iface=iface):
            return True
    return False

def quo_static_user_total_dashboards(params,deny):
    if 'uid' not in params:
        return False
    uid=params['uid']
    iface=interfaces['User_DashboardCreation']
    if deny:
        if cassapiiface.insert_user_iface_deny(uid=uid, iface=iface, perm=DEFAULT_PERM):
            return True
    else:
        if cassapiiface.delete_user_iface_deny(uid=uid, iface=iface):
            return True
    return False

def quo_static_user_total_circles(params,deny):
    if 'uid' not in params:
        return False
    uid=params['uid']
    iface=interfaces['User_CircleCreation']
    if deny:
        if cassapiiface.insert_user_iface_deny(uid=uid, iface=iface, perm=DEFAULT_PERM):
            return True
    else:
        if cassapiiface.delete_user_iface_deny(uid=uid, iface=iface):
            return True
    return False

def quo_static_agent_total_datasources(params,deny):
    if 'aid' not in params or 'uid' not in params:
        return False
    aid=params['aid']
    uid=params['uid']
    iface=interfaces['Agent_DatasourceCreation']+aid.hex
    if deny:
        if cassapiiface.insert_user_iface_deny(uid=uid, iface=iface, perm=DEFAULT_PERM):
            return True
    else:
        if cassapiiface.delete_user_iface_deny(uid=uid, iface=iface):
            return True
    return False

def quo_static_agent_total_datapoints(params,deny):
    if 'aid' not in params or 'uid' not in params:
        return False
    aid=params['aid']
    uid=params['uid']
    iface=interfaces['Agent_DatapointCreation']+aid.hex
    uid=uid
    if deny:
        if cassapiiface.insert_user_iface_deny(uid=uid, iface=iface, perm=DEFAULT_PERM):
            return True
    else:
        if cassapiiface.delete_user_iface_deny(uid=uid, iface=iface):
            return True
    return False

def quo_static_datasource_total_datapoints(params,deny):
    if 'did' not in params or 'uid' not in params:
        return False
    did=params['did']
    uid=params['uid']
    iface=interfaces['Datasource_DatapointCreation']+did.hex
    if deny:
        if cassapiiface.insert_user_iface_deny(uid=uid, iface=iface, perm=DEFAULT_PERM):
            return True
    else:
        if cassapiiface.delete_user_iface_deny(uid=uid, iface=iface):
            return True
    return False

def quo_static_user_total_snapshots(params,deny):
    if 'uid' not in params:
        return False
    uid=params['uid']
    iface=interfaces['User_SnapshotCreation']
    if deny:
        if cassapiiface.insert_user_iface_deny(uid=uid, iface=iface, perm=DEFAULT_PERM):
            return True
    else:
        if cassapiiface.delete_user_iface_deny(uid=uid, iface=iface):
            return True
    return False

def quo_static_circle_total_members(params,deny):
    if 'uid' not in params or 'cid' not in params:
        return False
    uid=params['uid']
    cid=params['cid']
    iface=interfaces['User_AddMemberToCircle']+cid.hex
    if deny:
        if cassapiiface.insert_user_iface_deny(uid=uid, iface=iface, perm=DEFAULT_PERM):
            return True
    else:
        if cassapiiface.delete_user_iface_deny(uid=uid, iface=iface):
            return True
    return False

