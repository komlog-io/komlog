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
from komlibs.auth import requests
from komcass.api import user as cassapiuser

func_requests={
               requests.NEW_AGENT:'authorize_new_agent_creation',
               requests.NEW_DATASOURCE:'authorize_new_datasource_creation',
               requests.NEW_DATAPOINT:'authorize_new_datapoint_creation',
               requests.NEW_WIDGET:'authorize_new_widget_creation',
               requests.NEW_DASHBOARD:'authorize_new_dashboard_creation',
               requests.POST_DATASOURCE_DATA:'authorize_post_datasource_data',
               requests.GET_AGENT_CONFIG:'authorize_get_agent_config',
               requests.GET_DATASOURCE_DATA:'authorize_get_datasource_data',
               requests.GET_DATASOURCE_CONFIG:'authorize_get_datasource_config',
               requests.GET_DATAPOINT_DATA:'authorize_get_datapoint_data',
               requests.GET_DATAPOINT_CONFIG:'authorize_get_datapoint_config',
               requests.GET_WIDGET_CONFIG:'authorize_get_widget_config',
               requests.GET_DASHBOARD_CONFIG:'authorize_get_dashboard_config',
               requests.UPDATE_DATASOURCE_CONFIG:'authorize_datasource_update_configuration',
               requests.UPDATE_DATAPOINT_CONFIG:'authorize_datapoint_update_configuration',
               requests.UPDATE_AGENT_CONFIG:'authorize_agent_update_configuration',
               requests.UPDATE_WIDGET_CONFIG:'authorize_widget_update_configuration',
               requests.UPDATE_DASHBOARD_CONFIG:'authorize_dashboard_update_configuration',
               requests.MARK_POSITIVE_VARIABLE:'authorize_mark_positive_variable',
               requests.MARK_NEGATIVE_VARIABLE:'authorize_mark_negative_variable',
               requests.DELETE_AGENT:'authorize_delete_agent',
               requests.DELETE_DATASOURCE:'authorize_delete_datasource',
               requests.DELETE_DATAPOINT:'authorize_delete_datapoint',
               requests.DELETE_WIDGET:'authorize_delete_widget',
               requests.DELETE_DASHBOARD:'authorize_delete_dashboard',
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

def authorize_mark_positive_variable(params):
    uid=params['uid']
    pid=params['pid']
    if not quoauth.authorize_mark_positive_variable(uid,pid=pid) \
        or not resauth.authorize_mark_positive_variable(uid,pid=pid):
        raise authexcept.AuthorizationException()

def authorize_mark_negative_variable(params):
    uid=params['uid']
    pid=params['pid']
    if not quoauth.authorize_mark_negative_variable(uid,pid=pid) \
        or not resauth.authorize_mark_negative_variable(uid,pid=pid):
        raise authexcept.AuthorizationException()

def authorize_delete_agent(params):
    uid=params['uid']
    aid=params['aid']
    if not resauth.authorize_delete_agent(uid,aid):
        raise authexcept.AuthorizationException()

def authorize_delete_datasource(params):
    uid=params['uid']
    did=params['did']
    if not resauth.authorize_delete_datasource(uid,did):
        raise authexcept.AuthorizationException()

def authorize_delete_datapoint(params):
    uid=params['uid']
    pid=params['pid']
    if not resauth.authorize_delete_datapoint(uid,pid):
        raise authexcept.AuthorizationException()

def authorize_delete_widget(params):
    uid=params['uid']
    wid=params['wid']
    if not resauth.authorize_delete_widget(uid,wid):
        raise authexcept.AuthorizationException()

def authorize_delete_dashboard(params):
    uid=params['uid']
    bid=params['bid']
    if not resauth.authorize_delete_dashboard(uid,bid):
        raise authexcept.AuthorizationException()

