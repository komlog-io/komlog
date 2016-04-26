'''
 update.py 
 
 This file implements functions to update quotes

 @author: jcazor
 @date: 01/10/2013

'''

from komlog.komlibs.auth.operations import Operations
from komlog.komlibs.auth.model.quotes import Quotes
from komlog.komcass.api import user as cassapiuser
from komlog.komcass.api import agent as cassapiagent
from komlog.komcass.api import datasource as cassapidatasource
from komlog.komcass.api import datapoint as cassapidatapoint
from komlog.komcass.api import widget as cassapiwidget
from komlog.komcass.api import dashboard as cassapidashboard
from komlog.komcass.api import snapshot as cassapisnapshot
from komlog.komcass.api import circle as cassapicircle
from komlog.komcass.api import quote as cassapiquote

update_funcs = {
                Operations.NEW_AGENT: ['quo_static_user_total_agents'],
                Operations.NEW_DATASOURCE: ['quo_static_agent_total_datasources','quo_static_user_total_datasources'],
                Operations.NEW_DATAPOINT: ['quo_static_datasource_total_datapoints','quo_static_agent_total_datapoints','quo_static_user_total_datapoints'],
                Operations.NEW_WIDGET: ['quo_static_user_total_widgets'],
                Operations.NEW_DASHBOARD: ['quo_static_user_total_dashboards'],
                Operations.NEW_WIDGET_SYSTEM: ['quo_static_user_total_widgets'],
                Operations.NEW_SNAPSHOT: ['quo_static_user_total_snapshots'],
                Operations.NEW_CIRCLE: ['quo_static_user_total_circles','quo_static_circle_total_members'],
                Operations.UPDATE_CIRCLE_MEMBERS: ['quo_static_circle_total_members'],
}

def get_update_funcs(operation):
    try:
        return update_funcs[operation]
    except KeyError:
        return []

def quo_static_user_total_agents(params):
    if 'uid' not in params:
        return None
    uid=params['uid']
    num_agents=cassapiagent.get_number_of_agents_by_uid(uid=uid)
    quote=Quotes.quo_static_user_total_agents.name
    if cassapiquote.set_user_quote(uid=uid, quote=quote, value=num_agents):
        return num_agents
    return None

def quo_static_user_total_datasources(params):
    if 'uid' not in params:
        return None
    uid=params['uid']
    aids=cassapiagent.get_agents_aids(uid=uid)
    total_datasources=0
    for aid in aids:
        agent_datasources=cassapidatasource.get_number_of_datasources_by_aid(aid=aid)
        total_datasources+=int(agent_datasources)
    quote=Quotes.quo_static_user_total_datasources.name
    if cassapiquote.set_user_quote(uid=uid, quote=quote, value=total_datasources):
        return total_datasources
    return None

def quo_static_user_total_datapoints(params):
    if 'uid' not in params:
        return None
    uid=params['uid']
    aids=cassapiagent.get_agents_aids(uid=uid)
    total_datapoints=0
    for aid in aids:
        dids=cassapidatasource.get_datasources_dids(aid=aid)
        for did in dids:
            datasource_datapoints=cassapidatapoint.get_number_of_datapoints_by_did(did=did)
            total_datapoints+=int(datasource_datapoints)
    quote=Quotes.quo_static_user_total_datapoints.name
    if cassapiquote.set_user_quote(uid=uid, quote=quote, value=total_datapoints):
        return total_datapoints
    return None

def quo_static_user_total_widgets(params):
    if 'uid' not in params:
        return None
    uid=params['uid']
    num_widgets=cassapiwidget.get_number_of_widgets_by_uid(uid=uid)
    quote=Quotes.quo_static_user_total_widgets.name
    if cassapiquote.set_user_quote(uid=uid, quote=quote, value=num_widgets):
        return num_widgets
    return None

def quo_static_user_total_dashboards(params):
    if 'uid' not in params:
        return None
    uid=params['uid']
    num_dashboards=cassapidashboard.get_number_of_dashboards_by_uid(uid=uid)
    quote=Quotes.quo_static_user_total_dashboards.name
    if cassapiquote.set_user_quote(uid=uid, quote=quote, value=num_dashboards):
        return num_dashboards
    return None

def quo_static_agent_total_datasources(params):
    if 'aid' not in params:
        return None
    aid=params['aid']
    num_datasources=cassapidatasource.get_number_of_datasources_by_aid(aid=aid)
    quote=Quotes.quo_static_agent_total_datasources.name
    if cassapiquote.set_agent_quote(aid=aid, quote=quote, value=num_datasources):
        return num_datasources
    return None

def quo_static_agent_total_datapoints(params):
    if 'aid' not in params:
        return None
    aid=params['aid']
    total_datapoints=0
    dids=cassapidatasource.get_datasources_dids(aid=aid)
    for did in dids:
        num_datapoints=cassapidatapoint.get_number_of_datapoints_by_did(did=did)
        total_datapoints+=int(num_datapoints)
    quote=Quotes.quo_static_agent_total_datapoints.name
    if cassapiquote.set_agent_quote(aid=aid, quote=quote, value=total_datapoints):
        return total_datapoints
    return None

def quo_static_datasource_total_datapoints(params):
    if 'did' not in params:
        return None
    did=params['did']
    total_datapoints=cassapidatapoint.get_number_of_datapoints_by_did(did=did)
    quote=Quotes.quo_static_datasource_total_datapoints.name
    if cassapiquote.set_datasource_quote(did=did, quote=quote, value=total_datapoints):
        return total_datapoints
    return None

def quo_static_user_total_snapshots(params):
    if 'uid' not in params:
        return None
    uid=params['uid']
    num_snapshots=cassapisnapshot.get_number_of_snapshots(uid=uid)
    quote=Quotes.quo_static_user_total_snapshots.name
    if cassapiquote.set_user_quote(uid=uid, quote=quote, value=num_snapshots):
        return num_snapshots
    return None

def quo_static_user_total_circles(params):
    if 'uid' not in params:
        return None
    uid=params['uid']
    num_circles=cassapicircle.get_number_of_circles(uid=uid)
    quote=Quotes.quo_static_user_total_circles.name
    if cassapiquote.set_user_quote(uid=uid, quote=quote, value=num_circles):
        return num_circles
    return None

def quo_static_circle_total_members(params):
    if 'cid' not in params:
        return None
    cid=params['cid']
    circle=cassapicircle.get_circle(cid=cid)
    if not circle:
        return '0'
    num_members=len(circle.members)
    quote=Quotes.quo_static_circle_total_members.name
    if cassapiquote.set_circle_quote(cid=cid, quote=quote, value=num_members):
        return num_members
    return None

