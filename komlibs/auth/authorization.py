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
               'GetDatasourceDataRequest':'authorize_get_ds_data',
               'PostDatasourceDataRequest':'authorize_post_ds_data',
               'GetDatasourceConfigRequest':'authorize_get_ds_config',
               'PutDatasourceConfigRequest':'authorize_put_ds_config',
               'GetDatapointDataRequest':'authorize_get_dp_data',
               'GetGraphConfigRequest':'authorize_get_graph_config'
               }

def authorize_request(request,username,session,aid=None,did=None,pid=None,gid=None):
    params={'aid':aid,'did':did,'username':username,'pid':pid,'gid':gid}
    getattr(sys.modules[__name__],func_requests[request])(params,session)

def authorize_new_agent_creation(params,session):
    username=params['username']
    if not quoauth.authorize_new_agent(username,session) \
        or not resauth.authorize_new_agent(username,session):
        raise authexcept.AuthorizationException()

def authorize_get_agent_config(params,session):
    username=params['username']
    aid=params['aid']
    if not quoauth.authorize_get_agent_config(username,aid,session) \
        or not resauth.authorize_get_agent_config(username,aid,session):
        raise authexcept.AuthorizationException()

def authorize_get_ds_data(params,session):
    username=params['username']
    did=params['did']
    if not quoauth.authorize_get_ds_data(username,did,session) \
        or not resauth.authorize_get_ds_data(username,did,session):
        raise authexcept.AuthorizationException()

def authorize_post_ds_data(params,session):
    username=params['username']
    did=params['did']
    aid=params['aid']
    if not quoauth.authorize_post_ds_data(username,aid,did,session) \
        or not resauth.authorize_get_ds_data(username,aid,did,session):
        raise authexcept.AuthorizationException()

def authorize_get_ds_config(params,session):
    username=params['username']
    did=params['did']
    if not quoauth.authorize_get_ds_config(username,did,session) \
        or not resauth.authorize_get_ds_config(username,did,session):
        raise authexcept.AuthorizationException()

def authorize_put_ds_config(params,session):
    username=params['username']
    did=params['did']
    if not quoauth.authorize_put_ds_config(username,did,session) \
        or not resauth.authorize_put_ds_config(username,did,session):
        raise authexcept.AuthorizationException()

def authorize_new_datasource_creation(params,session):
    username=params['username']
    aid=params['aid']
    if not quoauth.authorize_new_datasource(username,aid,session) \
        or not resauth.authorize_new_datasource(username,aid,session):
        raise authexcept.AuthorizationException()

def authorize_get_dp_data(params,session):
    username=params['username']
    pid=params['pid']
    if not quoauth.authorize_get_dp_data(username,pid,session) \
        or not resauth.authorize_get_dp_data(username,pid,session):
        raise authexcept.AuthorizationException()

def authorize_new_datapoint_creation(params,session):
    username=params['username']
    did=params['did']
    if not quoauth.authorize_new_datapoint(username,did,session) \
        or not resauth.authorize_new_datapoint(username,did,session):
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
