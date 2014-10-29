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

def deny_quo_static_user_total_agents(params,session,deny):
    if not params.has_key('uid'):
        return False
    uid=params['uid']
    iface=interfaces['User_AgentCreation']
    if deny:
        if cassapiiface.insert_user_iface_deny(session, uid=uid, iface=iface, perm=DEFAULT_PERM):
            return True
    else:
        if cassapiiface.delete_user_iface_deny(session, uid=uid, iface=iface):
            return True
    return False

def deny_quo_static_user_total_datasources(params,session,deny):
    if not params.has_key('uid'):
        return False
    uid=params['uid']
    iface=interfaces['User_DatasourceCreation']
    if deny:
        if cassapiiface.insert_user_iface_deny(session, uid=uid, iface=iface, perm=DEFAULT_PERM):
            return True
    else:
        if cassapiiface.delete_user_iface_deny(session, uid=uid, iface=iface):
            return True
    return False

def deny_quo_static_user_total_datapoints(params,session,deny):
    if not params.has_key('uid'):
        return False
    uid=params['uid']
    iface=interfaces['User_DatapointCreation']
    if deny:
        if cassapiiface.insert_user_iface_deny(session, uid=uid, iface=iface, perm=DEFAULT_PERM):
            return True
    else:
        if cassapiiface.delete_user_iface_deny(session, uid=uid, iface=iface):
            return True
    return False

def deny_quo_static_user_total_widgets(params,session,deny):
    if not params.has_key('uid'):
        return False
    uid=params['uid']
    iface=interfaces['User_WidgetCreation']
    if deny:
        if cassapiiface.insert_user_iface_deny(session, uid=uid, iface=iface, perm=DEFAULT_PERM):
            return True
    else:
        if cassapiiface.delete_user_iface_deny(session, uid=uid, iface=iface):
            return True
    return False

def deny_quo_static_user_total_dashboards(params,session,deny):
    if not params.has_key('uid'):
        return False
    uid=params['uid']
    iface=interfaces['User_DashboardCreation']
    if deny:
        if cassapiiface.insert_user_iface_deny(session, uid=uid, iface=iface, perm=DEFAULT_PERM):
            return True
    else:
        if cassapiiface.delete_user_iface_deny(session, uid=uid, iface=iface):
            return True
    return False

def deny_quo_static_agent_total_datasources(params,session,deny):
    if not params.has_key('aid') or not params.has_key('uid'):
        return False
    aid=params['aid']
    uid=params['uid']
    iface=interfaces['Agent_DatasourceCreation']+str(aid)
    uid=uid
    if deny:
        if cassapiiface.insert_user_iface_deny(session, uid=uid, iface=iface, perm=DEFAULT_PERM):
            return True
    else:
        if cassapiiface.delete_user_iface_deny(session, uid=uid, iface=iface):
            return True
    return False

def deny_quo_static_agent_total_datapoints(params,session,deny):
    if not params.has_key('aid') or not params.has_key('uid'):
        return False
    aid=params['aid']
    uid=params['uid']
    iface=interfaces['Agent_DatapointCreation']+str(aid)
    uid=uid
    if deny:
        if cassapiiface.insert_user_iface_deny(session, uid=uid, iface=iface, perm=DEFAULT_PERM):
            return True
    else:
        if cassapiiface.delete_user_iface_deny(session, uid=uid, iface=iface):
            return True
    return False

def deny_quo_static_datasource_total_datapoints(params,session,deny):
    if not params.has_key('did') or not params.has_key('uid'):
        return False
    did=params['did']
    uid=params['uid']
    iface=interfaces['Datasource_DatapointCreation']+str(did)
    if deny:
        if cassapiiface.insert_user_iface_deny(session, uid=uid, iface=iface, perm=DEFAULT_PERM):
            return True
    else:
        if cassapiiface.delete_user_iface_deny(session, uid=uid, iface=iface):
            return True
    return False

