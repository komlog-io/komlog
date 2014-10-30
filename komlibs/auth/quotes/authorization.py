#coding:utf-8

'''
This library implements authorization mechanisms based on user quotas


@author: jcazor
@date: 2013/12/08
'''

import deny
from komcass.api import user as cassapiuser
from komcass.api import datasource as cassapidatasource
from komcass.api import interface as cassapiiface


def authorize_new_agent(username):
    user=cassapiuser.get_user(username=username)
    interfaces=[]
    interfaces.append(deny.interfaces['User_AgentCreation'])
    for iface in interfaces:
        if cassapiiface.get_user_iface_deny(uid=user.uid, iface=iface):
            return False
    return True

def authorize_get_agent_config(username,aid):
    ''' Not quotes authorization needed '''
    return True

def authorize_get_datasource_data(username,did):
    ''' Not quotes authorization needed '''
    return True

def authorize_post_datasource_data(username,aid,did):
    ''' Not quotes authorization needed '''
    return True

def authorize_get_datasource_config(username,did):
    ''' Not quotes authorization needed '''
    return True

def authorize_put_datasource_config(username,aid,did):
    ''' Not quotes authorization needed '''
    return True

def authorize_new_datasource(username,aid):
    user=cassapiuser.get_user(username=username)
    interfaces=[]
    interfaces.append(deny.interfaces['User_DatasourceCreation'])
    interfaces.append(deny.interfaces['Agent_DatasourceCreation']+str(aid))
    for iface in interfaces:
        if cassapiiface.get_user_iface_deny(uid=user.uid, iface=iface):
            return False
    return True

def authorize_get_datapoint_data(username,pid):
    ''' Not quotes authorization needed '''
    return True

def authorize_get_datapoint_config(username,pid):
    ''' Not quotes authorization needed '''
    return True

def authorize_new_datapoint(username,did):
    user=cassapiuser.get_user(username=username)
    datasource=cassapidatasource.get_datasource(did=did)
    interfaces=[]
    interfaces.append(deny.interfaces['User_DatapointCreation'])
    interfaces.append(deny.interfaces['Agent_DatapointCreation']+str(datasource.aid))
    interfaces.append(deny.interfaces['Datasource_DatapointCreation']+str(did))
    for iface in interfaces:
        if cassapiiface.get_user_iface_deny(uid=user.uid, iface=iface):
            return False
    return True

def authorize_new_widget(username):
    user=cassapiuser.get_user(username=username)
    interfaces=[]
    interfaces.append(deny.interfaces['User_WidgetCreation'])
    for iface in interfaces:
        if cassapiiface.get_user_iface_deny(uid=user.uid, iface=iface):
            return False
    return True

def authorize_get_widget_config(username,wid):
    ''' Not quotes authorization needed '''
    return True

def authorize_put_widget_config(username,wid):
    ''' Not quotes authorization needed '''
    return True

def authorize_new_dashboard(username):
    user=cassapiuser.get_user(username=username)
    interfaces=[]
    interfaces.append(deny.interfaces['User_DashboardCreation'])
    for iface in interfaces:
        if cassapiiface.get_user_iface_deny(uid=user.uid, iface=iface):
            return False
    return True

def authorize_get_dashboard_config(username,bid):
    ''' Not quotes authorization needed '''
    return True

def authorize_put_dashboard_config(username,bid):
    ''' Not quotes authorization needed '''
    return True


