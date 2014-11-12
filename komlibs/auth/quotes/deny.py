#coding: utf-8
'''
deny.py 

This file implements functions to deny access to resourcess because of quotes configuration


@author: jcazor
@date: 2013/11/13

'''

from komcass.api import interface as cassapiiface

interfaces={'User_AgentCreation':'/user/agentcreation/',
            'User_GraphCreation':'/user/graphcreation/',
            'User_DatasourceCreation':'/user/dscreation/',
            'User_DatapointCreation':'/user/dpcreation/',
            'Agent_DatasourceCreation':'/agent/dscreation/',
            'Agent_DatapointCreation':'/agent/dpcreation/',
            'Datasource_DatapointCreation':'/ds/dpcreation/',
            'User_WidgetCreation':'/user/wgcreation/',
            'User_DashboardCreation':'/user/dbcreation/',
           }

DEFAULT_PERM='A'

def deny_quo_static_user_total_agents(params,deny):
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

def deny_quo_static_user_total_datasources(params,deny):
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

def deny_quo_static_user_total_datapoints(params,deny):
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

def deny_quo_static_user_total_widgets(params,deny):
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

def deny_quo_static_user_total_dashboards(params,deny):
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

def deny_quo_static_agent_total_datasources(params,deny):
    if 'aid' not in params or 'uid' not in params:
        return False
    aid=params['aid']
    uid=params['uid']
    iface=interfaces['Agent_DatasourceCreation']+str(aid)
    uid=uid
    if deny:
        if cassapiiface.insert_user_iface_deny(uid=uid, iface=iface, perm=DEFAULT_PERM):
            return True
    else:
        if cassapiiface.delete_user_iface_deny(uid=uid, iface=iface):
            return True
    return False

def deny_quo_static_agent_total_datapoints(params,deny):
    if 'aid' not in params or 'uid' not in params:
        return False
    aid=params['aid']
    uid=params['uid']
    iface=interfaces['Agent_DatapointCreation']+str(aid)
    uid=uid
    if deny:
        if cassapiiface.insert_user_iface_deny(uid=uid, iface=iface, perm=DEFAULT_PERM):
            return True
    else:
        if cassapiiface.delete_user_iface_deny(uid=uid, iface=iface):
            return True
    return False

def deny_quo_static_datasource_total_datapoints(params,deny):
    if 'did' not in params or 'uid' not in params:
        return False
    did=params['did']
    uid=params['uid']
    iface=interfaces['Datasource_DatapointCreation']+str(did)
    if deny:
        if cassapiiface.insert_user_iface_deny(uid=uid, iface=iface, perm=DEFAULT_PERM):
            return True
    else:
        if cassapiiface.delete_user_iface_deny(uid=uid, iface=iface):
            return True
    return False

