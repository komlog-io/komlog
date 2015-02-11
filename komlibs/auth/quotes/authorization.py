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


def authorize_new_agent(uid):
    interfaces=[]
    interfaces.append(deny.interfaces['User_AgentCreation'])
    for iface in interfaces:
        if cassapiiface.get_user_iface_deny(uid=uid, iface=iface):
            return False
    return True

def authorize_get_agent_config(uid,aid):
    ''' Not quotes authorization needed '''
    return True

def authorize_get_datasource_data(uid,did):
    ''' Not quotes authorization needed '''
    return True

def authorize_post_datasource_data(uid,aid,did):
    ''' Not quotes authorization needed '''
    return True

def authorize_get_datasource_config(uid,did):
    ''' Not quotes authorization needed '''
    return True

def authorize_put_datasource_config(uid,aid,did):
    ''' Not quotes authorization needed '''
    return True

def authorize_new_datasource(uid,aid):
    interfaces=[]
    interfaces.append(deny.interfaces['User_DatasourceCreation'])
    interfaces.append(deny.interfaces['Agent_DatasourceCreation']+aid.hex)
    for iface in interfaces:
        if cassapiiface.get_user_iface_deny(uid=uid, iface=iface):
            return False
    return True

def authorize_get_datapoint_data(uid,pid):
    ''' Not quotes authorization needed '''
    return True

def authorize_get_datapoint_config(uid,pid):
    ''' Not quotes authorization needed '''
    return True

def authorize_new_datapoint(uid,did):
    datasource=cassapidatasource.get_datasource(did=did)
    if not datasource:
        raise authexcept.DatasourceNotFoundException()
    interfaces=[]
    interfaces.append(deny.interfaces['User_DatapointCreation'])
    interfaces.append(deny.interfaces['Agent_DatapointCreation']+datasource.aid.hex)
    interfaces.append(deny.interfaces['Datasource_DatapointCreation']+did.hex)
    for iface in interfaces:
        if cassapiiface.get_user_iface_deny(uid=uid, iface=iface):
            return False
    return True

def authorize_new_widget(uid):
    interfaces=[]
    interfaces.append(deny.interfaces['User_WidgetCreation'])
    for iface in interfaces:
        if cassapiiface.get_user_iface_deny(uid=uid, iface=iface):
            return False
    return True

def authorize_get_widget_config(uid,wid):
    ''' Not quotes authorization needed '''
    return True

def authorize_put_widget_config(uid,wid):
    ''' Not quotes authorization needed '''
    return True

def authorize_new_dashboard(uid):
    interfaces=[]
    interfaces.append(deny.interfaces['User_DashboardCreation'])
    for iface in interfaces:
        if cassapiiface.get_user_iface_deny(uid=uid, iface=iface):
            return False
    return True

def authorize_get_dashboard_config(uid,bid):
    ''' Not quotes authorization needed '''
    return True

def authorize_put_dashboard_config(uid,bid):
    ''' Not quotes authorization needed '''
    return True

def authorize_mark_negative_variable(uid,pid):
    ''' Not quotes authorization needed '''
    return True

def authorize_mark_positive_variable(uid,pid):
    ''' Not quotes authorization needed '''
    return True

def authorize_add_widget_to_dashboard(uid,bid,wid):
    ''' Not quotes authorization needed '''
    return True

def authorize_delete_widget_from_dashboard(uid,bid):
    ''' Not quotes authorization needed '''
    return True

def authorize_add_datapoint_to_widget(uid, pid, wid):
    ''' Not quotes authorization needed '''
    return True

def authorize_delete_datapoint_from_widget(uid, wid):
    ''' Not quotes authorization needed '''
    return True

