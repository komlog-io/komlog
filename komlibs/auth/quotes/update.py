#coding: utf-8
###############################################################################
# update.py 
# 
# This file implements functions to update quotes
#
# @author: jcazor
# @date: 01/10/2013
#
###############################################################################

from komcass.api import user as cassapiuser
from komcass.api import agent as cassapiagent
from komcass.api import datasource as cassapidatasource
from komcass.api import datapoint as cassapidatapoint
from komcass.api import widget as cassapiwidget
from komcass.api import dashboard as cassapidashboard
from komcass.api import quote as cassapiquote

def update_quo_static_user_total_agents(params,session):
    if not params.has_key('uid'):
        return None
    uid=params['uid']
    num_agents=cassapiagent.get_number_of_agents_by_uid(session, uid=uid)
    if cassapiquote.set_user_quote(session, uid=uid, quote='quo_static_user_total_agents', value=str(num_agents)):
        return str(num_agents)
    return None

def update_quo_static_user_total_datasources(params,session):
    if not params.has_key('uid'):
        return None
    uid=params['uid']
    aids=cassapiagent.get_agents_aids(session, uid=uid)
    total_datasources=0
    for aid in aids:
        agent_datasources=cassapidatasource.get_number_of_datasources_by_aid(session,aid=aid)
        total_datasources+=int(agent_datasources)
    if cassapiquote.set_user_quote(session, uid=uid, quote='quo_static_user_total_datasources', value=str(total_datasources)):
        return str(total_datasources)
    return None

def update_quo_static_user_total_datapoints(params,session):
    if not params.has_key('uid'):
        return None
    uid=params['uid']
    aids=cassapiagent.get_agents_aids(session, uid=uid)
    total_datapoints=0
    for aid in aids:
        dids=cassapidatasource.get_datasources_dids(session,aid=aid)
        for did in dids:
            datasource_datapoints=cassapidatapoint.get_number_of_datapoints_by_did(session, did=did)
            total_datapoints+=int(datasource_datapoints)
    if cassapiquote.set_user_quote(session, uid=uid, quote='quo_static_user_total_datapoints', value=str(total_datapoints)):
        return str(total_datapoints)
    return None

def update_quo_static_user_total_widgets(params,session):
    if not params.has_key('uid'):
        return None
    uid=params['uid']
    num_widgets=cassapiwidget.get_number_of_widgets_by_uid(session, uid=uid)
    if cassapiquote.set_user_quote(session, uid=uid, quote='quo_static_user_total_widgets', value=str(num_widgets)):
        return str(num_widgets)
    return None

def update_quo_static_user_total_dashboards(params,session):
    if not params.has_key('uid'):
        return None
    uid=params['uid']
    num_dashboards=cassapidashboard.get_number_of_dashboards_by_uid(session, uid=uid)
    if cassapiquote.set_user_quotes(session, uid=uid, quote='quo_static_user_total_dashboards', value=str(num_dashboards)):
        return str(num_dashboards)
    return None

def update_quo_static_agent_total_datasources(params,session):
    if not params.has_key('aid'):
        return None
    aid=params['aid']
    num_datasources=cassapidatasource.get_number_of_datasources_by_aid(session, aid=aid)
    if cassapiquote.set_agent_quote(session, aid=aid, quote='quo_static_agent_total_datasources', value=str(num_datasources)):
        return str(num_datasources)
    return None

def update_quo_static_agent_total_datapoints(params,session):
    if not params.has_key('uid') or not params.has_key('aid'):
        return None
    uid=params['uid']
    aid=params['aid']
    total_datapoints=0
    dids=cassapidatasource.get_datasources_dids(session, aid=aid)
    for did in dids:
        num_datapoints=cassapidatapoint.get_number_of_datapoints_by_did(session,did=did)
        total_datapoints+=int(num_datapoints)
    if cassapiquote.set_agent_quote(session, aid=aid, quote='quo_static_agent_total_datapoints', value=str(total_datapoints)):
        return str(total_datapoints)
    return None

def update_quo_static_datasource_total_datapoints(params,session):
    if not params.has_key('did'):
        return None
    did=params['did']
    total_datapoints=cassapidatapoint.get_number_of_datapoints_by_did(session, did=did)
    if cassapiquote.set_datasource_quote(session, did=did, quote='quo_static_datasource_total_datapoints', value=str(total_datapoints)):
        return str(total_datapoints)
    return None

