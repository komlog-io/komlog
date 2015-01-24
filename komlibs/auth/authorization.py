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
    params={'aid':aid,'did':did,'uid':user.uid,'pid':pid,'wid':wid,'bid':bid}
    try:
        getattr(sys.modules[__name__],func_requests[request])(params)
    except KeyError:
        raise authexcept.RequestNotFoundException()

def authorize_new_agent_creation(params):
    uid=params['uid']
    if not quoauth.authorize_new_agent(uid=uid) \
        or not resauth.authorize_new_agent(uid=uid):
        raise authexcept.AuthorizationException()

def authorize_get_agent_config(params):
    uid=params['uid']
    aid=params['aid']
    if not quoauth.authorize_get_agent_config(uid=uid,aid=aid) \
        or not resauth.authorize_get_agent_config(uid=uid,aid=aid):
        raise authexcept.AuthorizationException()

def authorize_get_datasource_data(params):
    uid=params['uid']
    did=params['did']
    if not quoauth.authorize_get_datasource_data(uid=uid,did=did) \
        or not resauth.authorize_get_datasource_data(uid=uid,did=did):
        raise authexcept.AuthorizationException()

def authorize_post_datasource_data(params):
    uid=params['uid']
    did=params['did']
    aid=params['aid']
    if not quoauth.authorize_post_datasource_data(uid=uid,aid=aid,did=did) \
        or not resauth.authorize_post_datasource_data(uid=uid,aid=aid,did=did):
        raise authexcept.AuthorizationException()

def authorize_get_datasource_config(params):
    uid=params['uid']
    did=params['did']
    if not quoauth.authorize_get_datasource_config(uid=uid,did=did) \
        or not resauth.authorize_get_datasource_config(uid=uid,did=did):
        raise authexcept.AuthorizationException()

def authorize_datasource_update_configuration(params):
    uid=params['uid']
    did=params['did']
    if not resauth.authorize_put_datasource_config(uid=uid,did=did):
        raise authexcept.AuthorizationException()

def authorize_new_datasource_creation(params):
    uid=params['uid']
    aid=params['aid']
    if not quoauth.authorize_new_datasource(uid=uid,aid=aid) \
        or not resauth.authorize_new_datasource(uid=uid,aid=aid):
        raise authexcept.AuthorizationException()

def authorize_get_datapoint_data(params):
    uid=params['uid']
    pid=params['pid']
    if not quoauth.authorize_get_datapoint_data(uid,pid=pid) \
        or not resauth.authorize_get_datapoint_data(uid,pid=pid):
        raise authexcept.AuthorizationException()

def authorize_get_datapoint_config(params):
    uid=params['uid']
    pid=params['pid']
    if not quoauth.authorize_get_datapoint_config(uid=uid,pid=pid) \
        or not resauth.authorize_get_datapoint_config(uid=uid,pid=pid):
        raise authexcept.AuthorizationException()

def authorize_new_datapoint_creation(params):
    uid=params['uid']
    did=params['did']
    if not quoauth.authorize_new_datapoint(uid=uid,did=did) \
        or not resauth.authorize_new_datapoint(uid=uid,did=did):
        raise authexcept.AuthorizationException()

def authorize_datapoint_update_configuration(params):
    uid=params['uid']
    pid=params['pid']
    if not resauth.authorize_put_datapoint_config(uid=uid,pid=pid):
        raise authexcept.AuthorizationException()

def authorize_uid_update_configuration(params):
    #If uid authentication was successfull, authorization to its own uid config is granted
    pass

def authorize_uid_update_profile(params):
    #If uid authentication was successfull, authorization to its own uid profile is granted
    pass

def authorize_agent_update_configuration(params):
    uid=params['uid']
    aid=params['aid']
    if not resauth.authorize_put_agent_config(uid=uid,aid=aid):
        raise authexcept.AuthorizationException()

def authorize_get_widget_config(params):
    uid=params['uid']
    wid=params['wid']
    if not quoauth.authorize_get_widget_config(uid=uid,wid=wid) \
        or not resauth.authorize_get_widget_config(uid=uid,wid=wid):
        raise authexcept.AuthorizationException()

def authorize_widget_update_configuration(params):
    uid=params['uid']
    wid=params['wid']
    if not resauth.authorize_put_widget_config(uid=uid,wid=wid):
        raise authexcept.AuthorizationException()

def authorize_new_widget_creation(params):
    uid=params['uid']
    if not quoauth.authorize_new_widget(uid=uid) \
        or not resauth.authorize_new_widget(uid=uid):
        raise authexcept.AuthorizationException()

def authorize_get_dashboard_config(params):
    uid=params['uid']
    bid=params['bid']
    if not quoauth.authorize_get_dashboard_config(uid=uid,bid=bid) \
        or not resauth.authorize_get_dashboard_config(uid=uid,bid=bid):
        raise authexcept.AuthorizationException()

def authorize_dashboard_update_configuration(params):
    uid=params['uid']
    bid=params['bid']
    if not resauth.authorize_put_dashboard_config(uid=uid,bid=bid):
        raise authexcept.AuthorizationException()

def authorize_new_dashboard_creation(params):
    uid=params['uid']
    if not quoauth.authorize_new_dashboard(uid=uid) \
        or not resauth.authorize_new_dashboard(uid=uid):
        raise authexcept.AuthorizationException()

