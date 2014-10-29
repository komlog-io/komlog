#coding: utf-8
'''
This file is the entry point of authorization mechanisms

@author: jcazor
@date: 2013/12/08

'''

import sys
from komlibs.auth.quotes import authorization as quoauth
from komlibs.auth.resources import authorization as resauth
from komlibs.auth import exceptions as authexcept

func_requests={'NewAgentRequest':'authorize_new_agent_creation',
               'NewDatasourceRequest':'authorize_new_datasource_creation',
               'NewDatapointRequest':'authorize_new_datapoint_creation',
               'NewGraphRequest':'authorize_new_graph_creation',
               'GetAgentConfigRequest':'authorize_get_agent_config',
               'GetDatasourceDataRequest':'authorize_get_datasource_data',
               'PostDatasourceDataRequest':'authorize_post_datasource_data',
               'GetDatasourceConfigRequest':'authorize_get_datasource_config',
               'DatasourceUpdateConfigurationRequest':'authorize_datasource_update_configuration',
               'DatapointUpdateConfigurationRequest':'authorize_datapoint_update_configuration',
               'GetDatapointDataRequest':'authorize_get_datapoint_data',
               'GetDatapointConfigRequest':'authorize_get_datapoint_config',
               'GetGraphConfigRequest':'authorize_get_graph_config',
               'GraphUpdateConfigurationRequest':'authorize_graph_update_configuration',
               'UserUpdateConfigurationRequest':'authorize_user_update_configuration',
               'UserUpdateProfileRequest':'authorize_user_update_profile',
               'AgentUpdateConfigurationRequest':'authorize_agent_update_configuration',
               'GetPlotDataRequest':'authorize_get_plot_data',
               'NewWidgetRequest':'authorize_new_widget_creation',
               'GetWidgetConfigRequest':'authorize_get_widget_config',
               'WidgetUpdateConfigurationRequest':'authorize_widget_update_configuration',
               'NewDashboardRequest':'authorize_new_dashboard_creation',
               'GetDashboardConfigRequest':'authorize_get_dashboard_config',
               'DashboardUpdateConfigurationRequest':'authorize_dashboard_update_configuration',
               }

def authorize_request(request,username,session,aid=None,did=None,pid=None,gid=None,wid=None,bid=None,data=None):
    params={'aid':aid,'did':did,'username':username,'pid':pid,'gid':gid,'wid':wid,'bid':bid,'request_data':data}
    getattr(sys.modules[__name__],func_requests[request])(params,session)

def authorize_new_agent_creation(params,session):
    username=params['username']
    if not quoauth.authorize_new_agent(username,session) \
        or not resauth.authorize_new_agent(username,session):
        raise authexcept.AuthorizationException()

def authorize_get_agent_config(params,session):
    username=params['username']
    aid=params['aid']
    if not quoauth.authorize_get_agent_config(username=username,aid=aid,session=session) \
        or not resauth.authorize_get_agent_config(username=username,aid=aid,session=session):
        raise authexcept.AuthorizationException()

def authorize_get_datasource_data(params,session):
    username=params['username']
    did=params['did']
    if not quoauth.authorize_get_datasource_data(username,did,session) \
        or not resauth.authorize_get_datasource_data(username,did,session):
        raise authexcept.AuthorizationException()

def authorize_post_datasource_data(params,session):
    username=params['username']
    did=params['did']
    aid=params['aid']
    if not quoauth.authorize_post_datasource_data(username,aid,did,session) \
        or not resauth.authorize_post_datasource_data(username,aid,did,session):
        raise authexcept.AuthorizationException()

def authorize_get_datasource_config(params,session):
    username=params['username']
    did=params['did']
    if not quoauth.authorize_get_datasource_config(username,did,session) \
        or not resauth.authorize_get_datasource_config(username,did,session):
        raise authexcept.AuthorizationException()

def authorize_datasource_update_configuration(params,session):
    username=params['username']
    did=params['did']
    if not resauth.authorize_put_datasource_config(username,did,session):
        raise authexcept.AuthorizationException()

def authorize_new_datasource_creation(params,session):
    username=params['username']
    aid=params['aid']
    if not quoauth.authorize_new_datasource(username,aid,session) \
        or not resauth.authorize_new_datasource(username,aid,session):
        raise authexcept.AuthorizationException()

def authorize_get_datapoint_data(params,session):
    username=params['username']
    pid=params['pid']
    if not quoauth.authorize_get_datapoint_data(username,pid,session) \
        or not resauth.authorize_get_datapoint_data(username,pid,session):
        raise authexcept.AuthorizationException()

def authorize_get_datapoint_config(params,session):
    username=params['username']
    pid=params['pid']
    if not quoauth.authorize_get_datapoint_config(username,pid,session) \
        or not resauth.authorize_get_datapoint_config(username,pid,session):
        raise authexcept.AuthorizationException()

def authorize_new_datapoint_creation(params,session):
    username=params['username']
    did=params['did']
    if not quoauth.authorize_new_datapoint(username,did,session) \
        or not resauth.authorize_new_datapoint(username,did,session):
        raise authexcept.AuthorizationException()

def authorize_datapoint_update_configuration(params,session):
    username=params['username']
    pid=params['pid']
    if not resauth.authorize_put_datapoint_config(username,pid,session):
        raise authexcept.AuthorizationException()

def authorize_new_graph_creation(params,session):
    username=params['username']
    pid=params['pid']
    if not quoauth.authorize_new_graph(username,session) \
        or not resauth.authorize_new_graph(username,pid,session):
        raise authexcept.AuthorizationException()

def authorize_get_graph_config(params,session):
    username=params['username']
    gid=params['gid']
    if not quoauth.authorize_get_graph_config(username,gid,session) \
        or not resauth.authorize_get_graph_config(username,gid,session):
        raise authexcept.AuthorizationException()

def authorize_graph_update_configuration(params,session):
    username=params['username']
    gid=params['gid']
    if not resauth.authorize_put_graph_config(username,gid,session):
        raise authexcept.AuthorizationException()

def authorize_user_update_configuration(params,session):
    #If user authentication was successfull, authorization to its own user config is granted
    pass

def authorize_user_update_profile(params,session):
    #If user authentication was successfull, authorization to its own user profile is granted
    pass

def authorize_agent_update_configuration(params,session):
    username=params['username']
    aid=params['aid']
    if not resauth.authorize_put_agent_config(username,aid,session):
        raise authexcept.AuthorizationException()

def authorize_get_plot_data(params,session):
    username=params['username']
    gid=params['gid']
    if not resauth.authorize_get_plot_data(username,gid,session):
        raise authexcept.AuthorizationException()

def authorize_get_widget_config(params,session):
    username=params['username']
    wid=params['wid']
    if not quoauth.authorize_get_widget_config(username,wid,session) \
        or not resauth.authorize_get_widget_config(username,wid,session):
        raise authexcept.AuthorizationException()

def authorize_widget_update_configuration(params,session):
    username=params['username']
    wid=params['wid']
    if not resauth.authorize_put_widget_config(username,wid,session):
        raise authexcept.AuthorizationException()

def authorize_new_widget_creation(params,session):
    username=params['username']
    wid=params['wid']
    if not quoauth.authorize_new_widget(username,wid,session) \
        or not resauth.authorize_new_widget(username,session):
        raise authexcept.AuthorizationException()

def authorize_get_dashboard_config(params,session):
    username=params['username']
    bid=params['bid']
    if not quoauth.authorize_get_dashboard_config(username,bid,session) \
        or not resauth.authorize_get_dashboard_config(username,bid,session):
        raise authexcept.AuthorizationException()

def authorize_dashboard_update_configuration(params,session):
    username=params['username']
    bid=params['bid']
    if not resauth.authorize_put_dashboard_config(username,bid,session):
        raise authexcept.AuthorizationException()

def authorize_new_dashboard_creation(params,session):
    username=params['username']
    bid=params['bid']
    if not quoauth.authorize_new_dashboard(username,bid,session) \
        or not resauth.authorize_new_dashboard(username,session):
        raise authexcept.AuthorizationException()


