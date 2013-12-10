#coding: utf-8
'''
deny.py 

This file implements functions to deny access to resourcess because of quotes configuration


@author: jcazor
@date: 2013/11/13

'''

from komcass import api as cassapi

interfaces={'User_AgentCreation':'/user/agentcreation/',
            'User_GraphCreation':'/user/graphcreation/',
            'User_DatasourceCreation':'/user/dscreation/',
            'User_DatapointCreation':'/user/dpcreation/',
            'Agent_DatasourceCreation':'/agent/dscreation/',
            'Agent_DatapointCreation':'/agent/dpcreation/',
            'Ds_DatapointCreation':'/ds/dpcreation/'}

def deny_quo_static_user_total_agents(params,cf,deny):
    ''' Insert/Delete /etc/agent/ to User Deny List'''
    if not params.has_key('uid'):
        return False
    uid=params['uid']
    iface=interfaces['User_AgentCreation']
    userifd=cassapi.UserIfaceDeny(uid)
    userifd.add_interface(iface)
    if deny:
        if cassapi.insert_userifacedeny(userifd,cf):
            return True
    else:
        if cassapi.delete_userifacedeny(userifd,cf):
            return True
    return False

def deny_quo_static_user_total_graphs(params,cf,deny):
    ''' Add/Del /user/graphcreation/ to User deny List'''
    if not params.has_key('uid'):
        return False
    uid=params['uid']
    iface=interfaces['User_GraphCreation']
    userifd=cassapi.UserIfaceDeny(uid)     
    userifd.add_interface(iface)
    if deny:
        if cassapi.insert_userifacedeny(userifd,cf):
            return True
    else:
        if cassapi.delete_userifacedeny(userifd,cf):
            return True
    return False

def deny_quo_static_user_total_datasources(params,cf,deny):
    ''' Add/Del /etc/ds/ to User Deny List'''
    if not params.has_key('uid'):
        return False
    uid=params['uid']
    iface=interfaces['User_DatasourceCreation']
    userifd=cassapi.UserIfaceDeny(uid)
    userifd.add_interface(iface)
    if deny:
        if cassapi.insert_userifacedeny(userifd,cf):
            return True
    else:
        if cassapi.delete_userifacedeny(userifd,cf):
            return True
    return False

def deny_quo_static_user_total_datapoints(params,cf,deny):
    if not params.has_key('uid'):
        return False
    uid=params['uid']
    iface=interfaces['User_DatapointCreation']
    userifd=cassapi.UserIfaceDeny(uid)
    userifd.add_interface(iface)
    if deny:
        if cassapi.insert_userifacedeny(userifd,cf):
            return True
    else:
        if cassapi.delete_userifacedeny(userifd,cf):
            return True
    return False

def deny_quo_static_agent_total_datasources(params,cf,deny):
    if not params.has_key('aid') or not params.has_key('uid'):
        return False
    aid=params['aid']
    uid=params['uid']
    iface=interfaces['Agent_DatasourceCreation']+str(aid)
    uid=uid
    userifd=cassapi.UserIfaceDeny(uid)
    userifd.add_interface(iface)
    if deny:
        if cassapi.insert_userifacedeny(userifd,cf):
            return True
    else:
        if cassapi.delete_userifacedeny(userifd,cf):
            return True
    return False

def deny_quo_static_agent_total_datapoints(params,cf,deny):
    if not params.has_key('aid') or not params.has_key('uid'):
        return False
    aid=params['aid']
    uid=params['uid']
    iface=interfaces['Agent_DatapointCreation']+str(aid)
    uid=uid
    userifd=cassapi.UserIfaceDeny(uid)
    userifd.add_interface(iface)
    if deny:
        if cassapi.insert_userifacedeny(userifd,cf):
            return True
    else:
        if cassapi.delete_userifacedeny(userifd,cf):
            return True
    return False

def deny_quo_static_ds_total_datapoints(params,cf,deny):
    if not params.has_key('did') or not params.has_key('uid'):
        return False
    did=params['did']
    uid=params['uid']
    iface=interfaces['Ds_DatapointCreation']+str(did)
    userifd=cassapi.UserIfaceDeny(uid)
    userifd.add_interface(iface)
    if deny:
        if cassapi.insert_userifacedeny(userifd,cf):
            return True
    else:
        if cassapi.delete_userifacedeny(userifd,cf):
            return True
    return False

