'''
 update.py 
 
 This file implements functions to update quotes

 @author: jcazor
 @date: 01/10/2013

'''

from komlog.komlibs.auth import operations
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
                operations.NEW_AGENT: ['quo_static_user_total_agents'],
                operations.NEW_DATASOURCE: ['quo_static_agent_total_datasources','quo_static_user_total_datasources'],
                operations.NEW_DATAPOINT: ['quo_static_datasource_total_datapoints','quo_static_agent_total_datapoints','quo_static_user_total_datapoints'],
                operations.NEW_WIDGET: ['quo_static_user_total_widgets'],
                operations.NEW_DASHBOARD: ['quo_static_user_total_dashboards'],
                operations.NEW_WIDGET_SYSTEM: ['quo_static_user_total_widgets'],
                operations.NEW_SNAPSHOT: ['quo_static_user_total_snapshots'],
                operations.NEW_CIRCLE: ['quo_static_user_total_circles','quo_static_circle_total_members'],
                operations.UPDATE_CIRCLE_MEMBERS: ['quo_static_circle_total_members'],
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
    if cassapiquote.set_user_quote(uid=uid, quote='quo_static_user_total_agents', value=str(num_agents)):
        return str(num_agents)
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
    if cassapiquote.set_user_quote(uid=uid, quote='quo_static_user_total_datasources', value=str(total_datasources)):
        return str(total_datasources)
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
    if cassapiquote.set_user_quote(uid=uid, quote='quo_static_user_total_datapoints', value=str(total_datapoints)):
        return str(total_datapoints)
    return None

def quo_static_user_total_widgets(params):
    if 'uid' not in params:
        return None
    uid=params['uid']
    num_widgets=cassapiwidget.get_number_of_widgets_by_uid(uid=uid)
    if cassapiquote.set_user_quote(uid=uid, quote='quo_static_user_total_widgets', value=str(num_widgets)):
        return str(num_widgets)
    return None

def quo_static_user_total_dashboards(params):
    if 'uid' not in params:
        return None
    uid=params['uid']
    num_dashboards=cassapidashboard.get_number_of_dashboards_by_uid(uid=uid)
    if cassapiquote.set_user_quote(uid=uid, quote='quo_static_user_total_dashboards', value=str(num_dashboards)):
        return str(num_dashboards)
    return None

def quo_static_agent_total_datasources(params):
    if 'aid' not in params:
        return None
    aid=params['aid']
    num_datasources=cassapidatasource.get_number_of_datasources_by_aid(aid=aid)
    if cassapiquote.set_agent_quote(aid=aid, quote='quo_static_agent_total_datasources', value=str(num_datasources)):
        return str(num_datasources)
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
    if cassapiquote.set_agent_quote(aid=aid, quote='quo_static_agent_total_datapoints', value=str(total_datapoints)):
        return str(total_datapoints)
    return None

def quo_static_datasource_total_datapoints(params):
    if 'did' not in params:
        return None
    did=params['did']
    total_datapoints=cassapidatapoint.get_number_of_datapoints_by_did(did=did)
    if cassapiquote.set_datasource_quote(did=did, quote='quo_static_datasource_total_datapoints', value=str(total_datapoints)):
        return str(total_datapoints)
    return None

def quo_static_user_total_snapshots(params):
    if 'uid' not in params:
        return None
    uid=params['uid']
    num_snapshots=cassapisnapshot.get_number_of_snapshots(uid=uid)
    if cassapiquote.set_user_quote(uid=uid, quote='quo_static_user_total_snapshots', value=str(num_snapshots)):
        return str(num_snapshots)
    return None

def quo_static_user_total_circles(params):
    if 'uid' not in params:
        return None
    uid=params['uid']
    num_circles=cassapicircle.get_number_of_circles(uid=uid)
    if cassapiquote.set_user_quote(uid=uid, quote='quo_static_user_total_circles', value=str(num_circles)):
        return str(num_circles)
    return None

def quo_static_circle_total_members(params):
    if 'cid' not in params:
        return None
    cid=params['cid']
    circle=cassapicircle.get_circle(cid=cid)
    if not circle:
        return '0'
    num_members=len(circle.members)
    if cassapiquote.set_circle_quote(cid=cid, quote='quo_static_circle_total_members', value=str(num_members)):
        return str(num_members)
    return None
