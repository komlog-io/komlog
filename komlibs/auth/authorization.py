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
from komcass.api import user as cassapiuser

func_requests={
               'DummyRequest':'authorize_dummy_request',
               'NewAgentRequest':'authorize_new_agent_creation',
               'NewDatasourceRequest':'authorize_new_datasource_creation',
               'NewDatapointRequest':'authorize_new_datapoint_creation',
               'GetAgentConfigRequest':'authorize_get_agent_config',
               'GetDatasourceDataRequest':'authorize_get_datasource_data',
               'PostDatasourceDataRequest':'authorize_post_datasource_data',
               'GetDatasourceConfigRequest':'authorize_get_datasource_config',
               'DatasourceUpdateConfigurationRequest':'authorize_datasource_update_configuration',
               'DatapointUpdateConfigurationRequest':'authorize_datapoint_update_configuration',
               'GetDatapointDataRequest':'authorize_get_datapoint_data',
               'GetDatapointConfigRequest':'authorize_get_datapoint_config',
               'UserUpdateConfigurationRequest':'authorize_user_update_configuration',
               'UserUpdateProfileRequest':'authorize_user_update_profile',
               'AgentUpdateConfigurationRequest':'authorize_agent_update_configuration',
               'NewWidgetRequest':'authorize_new_widget_creation',
               'GetWidgetConfigRequest':'authorize_get_widget_config',
               'WidgetUpdateConfigurationRequest':'authorize_widget_update_configuration',
               'NewDashboardRequest':'authorize_new_dashboard_creation',
               'GetDashboardConfigRequest':'authorize_get_dashboard_config',
               'DashboardUpdateConfigurationRequest':'authorize_dashboard_update_configuration',
               }

def authorize_request(request,username,aid=None,did=None,pid=None,gid=None,wid=None,bid=None):
    user=cassapiuser.get_user(username=username)
    if not user:
        raise authexcept.UserNotFoundException()
    params={'aid':aid,'did':did,'user':user,'pid':pid,'wid':wid,'bid':bid}
    try:
        getattr(sys.modules[__name__],func_requests[request])(params)
    except KeyError:
        raise authexcept.RequestNotFoundException()

def authorize_dummy_request(params):
    pass

def authorize_new_agent_creation(params):
    user=params['user']
    if not quoauth.authorize_new_agent(user) \
        or not resauth.authorize_new_agent(user):
        raise authexcept.AuthorizationException()

def authorize_get_agent_config(params):
    user=params['user']
    aid=params['aid']
    if not quoauth.authorize_get_agent_config(user=user,aid=aid) \
        or not resauth.authorize_get_agent_config(user=user,aid=aid):
        raise authexcept.AuthorizationException()

def authorize_get_datasource_data(params):
    user=params['user']
    did=params['did']
    if not quoauth.authorize_get_datasource_data(user,did) \
        or not resauth.authorize_get_datasource_data(user,did):
        raise authexcept.AuthorizationException()

def authorize_post_datasource_data(params):
    user=params['user']
    did=params['did']
    aid=params['aid']
    if not quoauth.authorize_post_datasource_data(user,aid,did) \
        or not resauth.authorize_post_datasource_data(user,aid,did):
        raise authexcept.AuthorizationException()

def authorize_get_datasource_config(params):
    user=params['user']
    did=params['did']
    if not quoauth.authorize_get_datasource_config(user,did) \
        or not resauth.authorize_get_datasource_config(user,did):
        raise authexcept.AuthorizationException()

def authorize_datasource_update_configuration(params):
    user=params['user']
    did=params['did']
    if not resauth.authorize_put_datasource_config(user,did):
        raise authexcept.AuthorizationException()

def authorize_new_datasource_creation(params):
    user=params['user']
    aid=params['aid']
    if not quoauth.authorize_new_datasource(user,aid) \
        or not resauth.authorize_new_datasource(user,aid):
        raise authexcept.AuthorizationException()

def authorize_get_datapoint_data(params):
    user=params['user']
    pid=params['pid']
    if not quoauth.authorize_get_datapoint_data(user,pid) \
        or not resauth.authorize_get_datapoint_data(user,pid):
        raise authexcept.AuthorizationException()

def authorize_get_datapoint_config(params):
    user=params['user']
    pid=params['pid']
    if not quoauth.authorize_get_datapoint_config(user,pid) \
        or not resauth.authorize_get_datapoint_config(user,pid):
        raise authexcept.AuthorizationException()

def authorize_new_datapoint_creation(params):
    user=params['user']
    did=params['did']
    if not quoauth.authorize_new_datapoint(user,did) \
        or not resauth.authorize_new_datapoint(user,did):
        raise authexcept.AuthorizationException()

def authorize_datapoint_update_configuration(params):
    user=params['user']
    pid=params['pid']
    if not resauth.authorize_put_datapoint_config(user,pid):
        raise authexcept.AuthorizationException()

def authorize_user_update_configuration(params):
    #If user authentication was successfull, authorization to its own user config is granted
    pass

def authorize_user_update_profile(params):
    #If user authentication was successfull, authorization to its own user profile is granted
    pass

def authorize_agent_update_configuration(params):
    user=params['user']
    aid=params['aid']
    if not resauth.authorize_put_agent_config(user,aid):
        raise authexcept.AuthorizationException()

def authorize_get_widget_config(params):
    user=params['user']
    wid=params['wid']
    if not quoauth.authorize_get_widget_config(user,wid) \
        or not resauth.authorize_get_widget_config(user,wid):
        raise authexcept.AuthorizationException()

def authorize_widget_update_configuration(params):
    user=params['user']
    wid=params['wid']
    if not resauth.authorize_put_widget_config(user,wid):
        raise authexcept.AuthorizationException()

def authorize_new_widget_creation(params):
    user=params['user']
    if not quoauth.authorize_new_widget(user) \
        or not resauth.authorize_new_widget(user):
        raise authexcept.AuthorizationException()

def authorize_get_dashboard_config(params):
    user=params['user']
    bid=params['bid']
    if not quoauth.authorize_get_dashboard_config(user,bid) \
        or not resauth.authorize_get_dashboard_config(user,bid):
        raise authexcept.AuthorizationException()

def authorize_dashboard_update_configuration(params):
    user=params['user']
    bid=params['bid']
    if not resauth.authorize_put_dashboard_config(user,bid):
        raise authexcept.AuthorizationException()

def authorize_new_dashboard_creation(params):
    user=params['user']
    if not quoauth.authorize_new_dashboard(user) \
        or not resauth.authorize_new_dashboard(user):
        raise authexcept.AuthorizationException()


