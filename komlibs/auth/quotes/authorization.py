#coding:utf-8

'''
This library implements authorization mechanisms based on user quotas


@author: jcazor
@date: 2013/12/08
'''

from komlibs.auth.quotes import deny
from komcass.api import datasource as cassapidatasource
from komcass.api import interface as cassapiiface
from komlibs.auth import exceptions as authexcept


def authorize_new_agent(user):
    interfaces=[]
    interfaces.append(deny.interfaces['User_AgentCreation'])
    for iface in interfaces:
        if cassapiiface.get_user_iface_deny(uid=user.uid, iface=iface):
            return False
    return True

def authorize_get_agent_config(user,aid):
    ''' Not quotes authorization needed '''
    return True

def authorize_get_datasource_data(user,did):
    ''' Not quotes authorization needed '''
    return True

def authorize_post_datasource_data(user,aid,did):
    ''' Not quotes authorization needed '''
    return True

def authorize_get_datasource_config(user,did):
    ''' Not quotes authorization needed '''
    return True

def authorize_put_datasource_config(user,aid,did):
    ''' Not quotes authorization needed '''
    return True

def authorize_new_datasource(user,aid):
    interfaces=[]
    interfaces.append(deny.interfaces['User_DatasourceCreation'])
    interfaces.append(deny.interfaces['Agent_DatasourceCreation']+str(aid))
    for iface in interfaces:
        if cassapiiface.get_user_iface_deny(uid=user.uid, iface=iface):
            return False
    return True

def authorize_get_datapoint_data(user,pid):
    ''' Not quotes authorization needed '''
    return True

def authorize_get_datapoint_config(user,pid):
    ''' Not quotes authorization needed '''
    return True

def authorize_new_datapoint(user,did):
    datasource=cassapidatasource.get_datasource(did=did)
    if not datasource:
        raise authexcept.DatasourceNotFoundException()
    interfaces=[]
    interfaces.append(deny.interfaces['User_DatapointCreation'])
    interfaces.append(deny.interfaces['Agent_DatapointCreation']+str(datasource.aid))
    interfaces.append(deny.interfaces['Datasource_DatapointCreation']+str(did))
    for iface in interfaces:
        if cassapiiface.get_user_iface_deny(uid=user.uid, iface=iface):
            return False
    return True

def authorize_new_widget(user):
    interfaces=[]
    interfaces.append(deny.interfaces['User_WidgetCreation'])
    for iface in interfaces:
        if cassapiiface.get_user_iface_deny(uid=user.uid, iface=iface):
            return False
    return True

def authorize_get_widget_config(user,wid):
    ''' Not quotes authorization needed '''
    return True

def authorize_put_widget_config(user,wid):
    ''' Not quotes authorization needed '''
    return True

def authorize_new_dashboard(user):
    interfaces=[]
    interfaces.append(deny.interfaces['User_DashboardCreation'])
    for iface in interfaces:
        if cassapiiface.get_user_iface_deny(uid=user.uid, iface=iface):
            return False
    return True

def authorize_get_dashboard_config(user,bid):
    ''' Not quotes authorization needed '''
    return True

def authorize_put_dashboard_config(user,bid):
    ''' Not quotes authorization needed '''
    return True


