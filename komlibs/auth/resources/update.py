#coding: utf-8
'''
update.py 

This file implements functions to update authorization to resources

@author: jcazor
@date: 2013/11/11

'''

from komlibs.auth import operations, permissions
from komcass.api import user as cassapiuser
from komcass.api import agent as cassapiagent
from komcass.api import datasource as cassapidatasource
from komcass.api import datapoint as cassapidatapoint
from komcass.api import widget as cassapiwidget
from komcass.api import dashboard as cassapidashboard
from komcass.api import snapshot as cassapisnapshot
from komcass.api import permission as cassapiperm

update_funcs = {
                operations.NEW_AGENT: ['new_agent'],
                operations.NEW_DATASOURCE: ['new_datasource'],
                operations.NEW_DATAPOINT: ['new_datapoint'],
                operations.NEW_WIDGET: ['new_widget'],
                operations.NEW_DASHBOARD: ['new_dashboard'],
                operations.NEW_WIDGET_SYSTEM: ['new_widget_system'],
                operations.NEW_SNAPSHOT: ['new_snapshot'],
                operations.DELETE_USER: ['delete_user'],
                operations.DELETE_AGENT: ['delete_agent'],
                operations.DELETE_DATASOURCE: ['delete_datasource'],
                operations.DELETE_DATAPOINT: ['delete_datapoint'],
                operations.DELETE_WIDGET: ['delete_widget'],
                operations.DELETE_DASHBOARD: ['delete_dashboard'],
                operations.DELETE_SNAPSHOT: ['delete_snapshot'],
}

def get_update_funcs(operation):
    try:
        return update_funcs[operation]
    except KeyError:
        return []

def new_agent(params):
    if 'aid' not in params or 'uid' not in params:
        return False
    aid=params['aid']
    uid=params['uid']
    perm=permissions.CAN_READ|permissions.CAN_EDIT|permissions.CAN_DELETE
    if cassapiperm.insert_user_agent_perm(uid=uid, aid=aid, perm=perm):
        return True
    return False

def new_datasource(params):
    if not 'aid' in params or not 'uid' in params or not 'did' in params:
        return False
    aid=params['aid']
    uid=params['uid']
    did=params['did']
    perm=permissions.CAN_READ|permissions.CAN_EDIT|permissions.CAN_DELETE
    if cassapiperm.insert_user_datasource_perm(uid=uid, did=did, perm=perm) and \
       cassapiperm.insert_agent_datasource_perm(aid=aid, did=did, perm=perm):
        return True
    return False

def new_datapoint(params):
    if not 'uid' in params or not 'pid' in params:
        return False
    uid=params['uid']
    pid=params['pid']
    user_perm=permissions.CAN_READ|permissions.CAN_EDIT|permissions.CAN_DELETE
    if cassapiperm.insert_user_datapoint_perm(uid=uid, pid=pid, perm=user_perm):
        return True
    return False

def new_widget(params):
    if not 'uid' in params or not 'wid' in params:
        return False
    uid=params['uid']
    wid=params['wid']
    user_perm=permissions.CAN_READ|permissions.CAN_EDIT|permissions.CAN_DELETE|permissions.CAN_SNAPSHOT
    if cassapiperm.insert_user_widget_perm(uid=uid, wid=wid, perm=user_perm):
        return True
    return False

def new_dashboard(params):
    if not 'uid' in params or not 'bid' in params:
        return False
    uid=params['uid']
    bid=params['bid']
    user_perm=permissions.CAN_READ|permissions.CAN_EDIT|permissions.CAN_DELETE
    if cassapiperm.insert_user_dashboard_perm(uid=uid, bid=bid, perm=user_perm):
        return True
    return False

def new_widget_system(params):
    ''' the *_system operations are those that automatically launches the system. In this case, 
        owner is the user, but it can't delete the widget '''
    if not 'uid' in params or not 'wid' in params:
        return False
    uid=params['uid']
    wid=params['wid']
    user_perm=permissions.CAN_READ|permissions.CAN_EDIT|permissions.CAN_SNAPSHOT
    if cassapiperm.insert_user_widget_perm(uid=uid, wid=wid, perm=user_perm):
        return True
    return False

def new_snapshot(params):
    if not 'uid' in params or not 'nid' in params:
        return False
    uid=params['uid']
    nid=params['nid']
    user_perm=permissions.CAN_READ|permissions.CAN_EDIT|permissions.CAN_DELETE
    if cassapiperm.insert_user_snapshot_perm(uid=uid, nid=nid, perm=user_perm):
        return True
    return False

def delete_user(uid):
    ''' This function revoke all access to every element a user and its agents can have'''
    perm=permissions.NONE
    agents=cassapiperm.get_user_agents_perm(uid=uid)
    for agent in agents:
        cassapiperm.insert_user_agent_perm(uid=uid, aid=agent.aid, perm=perm)
    widgets=cassapiperm.get_user_widgets_perm(uid=uid)
    for widget in widgets:
        cassapiperm.insert_user_widget_perm(uid=uid, wid=widget.wid, perm=perm)
    dashboards=cassapiperm.get_user_dashboards_perm(uid=uid)
    for dashboard in dashboards:
        cassapiperm.insert_user_dashboard_perm(uid=uid, bid=dashboard.bid, perm=perm)
    datasources=cassapiperm.get_user_datasources_perm(uid=uid)
    for datasource in datasources:
        cassapiperm.insert_user_datasource_perm(uid=uid, did=datasource.did, perm=perm)
    datapoints=cassapiperm.get_user_datapoints_perm(uid=uid)
    for datapoint in datapoints:
        cassapiperm.insert_user_datapoint_perm(uid=uid, pid=datapoint.pid, perm=perm)
    aids=cassapiagent.get_agents_aids(uid=uid)
    for aid in aids:
        datasources=cassapiperm.get_agent_datasources_perm(aid=aid)
        for datasource in datasources:
            cassapiperm.insert_agent_datasource_perm(aid=aid, did=datasource.did, perm=perm)
        datapoints=cassapiperm.get_agent_datapoints_perm(aid=aid)
        for datapoint in datapoints:
            cassapiperm.insert_agent_datapoint_perm(aid=aid, pid=datapoint.pid, perm=perm)
    return True


def delete_agent(aid):
    ''' This function revoke all access to every element an agent has'''
    perm=permissions.NONE
    agent=cassapiagent.get_agent(aid=aid)
    if agent:
        cassapiperm.insert_user_agent_perm(uid=agent.uid, aid=aid, perm=perm)
        dids=cassapidatasource.get_datasources_dids(aid=aid)
        for did in dids:
            cassapiperm.insert_user_datasource_perm(uid=agent.uid, did=did, perm=perm)
            pids=cassapidatapoint.get_datapoints_pids(did=did)
            for pid in pids:
                cassapiperm.insert_user_datapoint_perm(uid=agent.uid, pid=pid, perm=perm)
    datasources=cassapiperm.get_agent_datasources_perm(aid=aid)
    for datasource in datasources:
        cassapiperm.insert_agent_datasource_perm(aid=aid, did=datasource.did, perm=perm)
        widgetds=cassapiwidget.get_widget_ds(did=datasource.did)
        if widgetds:
            cassapiperm.insert_user_widget_perm(uid=agent.uid, wid=widgetds.wid, perm=perm)
    datapoints=cassapiperm.get_agent_datapoints_perm(aid=aid)
    for datapoint in datapoints:
        cassapiperm.insert_agent_datapoint_perm(aid=aid, pid=datapoint.pid, perm=perm)
        widgetdp=cassapiwidget.get_widget_dp(pid=datapoint.pid)
        if widgetdp:
            cassapiperm.insert_user_widget_perm(uid=agent.uid, wid=widgetdp.wid, perm=perm)
    return True

def delete_datasource(did):
    ''' This function revoke all access to the datasource by the user and its agent '''
    perm=permissions.NONE
    datasource=cassapidatasource.get_datasource(did=did)
    if datasource:
        cassapiperm.insert_user_datasource_perm(uid=datasource.uid, did=did, perm=perm)
        cassapiperm.insert_agent_datasource_perm(aid=datasource.aid, did=did, perm=perm)
        widgetds=cassapiwidget.get_widget_ds(did=datasource.did)
        if widgetds:
            cassapiperm.insert_user_widget_perm(uid=datasource.uid, wid=widgetds.wid, perm=perm)
        pids=cassapidatapoint.get_datapoints_pids(did=did)
        for pid in pids:
            cassapiperm.insert_user_datapoint_perm(uid=datasource.uid, pid=pid, perm=perm)
            cassapiperm.insert_agent_datapoint_perm(aid=datasource.aid, pid=pid, perm=perm)
            widgetdp=cassapiwidget.get_widget_dp(pid=pid)
            if widgetdp:
                cassapiperm.insert_user_widget_perm(uid=datasource.uid, wid=widgetdp.wid, perm=perm)
    return True

def delete_datapoint(pid):
    ''' This function revoke all access to the datapoint by the user and its agent '''
    perm=permissions.NONE
    datapoint=cassapidatapoint.get_datapoint(pid=pid)
    if datapoint:
        datasource=cassapidatasource.get_datasource(did=datapoint.did)
        if datasource:
            cassapiperm.insert_user_datapoint_perm(uid=datasource.uid, pid=pid, perm=perm)
            cassapiperm.insert_agent_datapoint_perm(aid=datasource.aid, pid=pid, perm=perm)
            widgetdp=cassapiwidget.get_widget_dp(pid=pid)
            if widgetdp:
                cassapiperm.insert_user_widget_perm(uid=datasource.uid, wid=widgetdp.wid, perm=perm)
    return True

def delete_widget(wid):
    ''' This function revoke all access to the widget passed '''
    perm=permissions.NONE
    widget=cassapiwidget.get_widget(wid=wid)
    if widget:
        cassapiperm.insert_user_widget_perm(uid=widget.uid, wid=wid, perm=perm)
    return True

def delete_dashboard(bid):
    ''' This function revoke all access to the dashboard passed '''
    perm=permissions.NONE
    dashboard=cassapidashboard.get_dashboard(bid=bid)
    if dashboard:
        cassapiperm.insert_user_dashboard_perm(uid=dashboard.uid, bid=bid, perm=perm)
    return True

def delete_snapshot(nid):
    ''' This function revoke all access to the snapshot passed '''
    perm=permissions.NONE
    snapshot=cassapisnapshot.get_snapshot(nid=nid)
    if snapshot:
        cassapiperm.insert_user_snapshot_perm(uid=snapshot.uid, nid=nid, perm=perm)
    return True

