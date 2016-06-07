#coding: utf-8
'''
update.py 

This file implements functions to update authorization to resources

@author: jcazor
@date: 2013/11/11

'''

from komlog.komlibs.auth import permissions
from komlog.komlibs.auth.model.operations import Operations
from komlog.komcass.api import user as cassapiuser
from komlog.komcass.api import agent as cassapiagent
from komlog.komcass.api import datasource as cassapidatasource
from komlog.komcass.api import datapoint as cassapidatapoint
from komlog.komcass.api import widget as cassapiwidget
from komlog.komcass.api import dashboard as cassapidashboard
from komlog.komcass.api import snapshot as cassapisnapshot
from komlog.komcass.api import circle as cassapicircle
from komlog.komcass.api import permission as cassapiperm

def get_update_funcs(operation):
    return update_funcs[operation]

def new_agent(params):
    if not 'aid' in params or not 'uid' in params:
        return False
    aid=params['aid']
    uid=params['uid']
    perm=permissions.CAN_READ|permissions.CAN_EDIT|permissions.CAN_DELETE
    if cassapiperm.insert_user_agent_perm(uid=uid, aid=aid, perm=perm):
        return True
    return False

def new_datasource(params):
    if not 'uid' in params or not 'did' in params:
        return False
    uid=params['uid']
    did=params['did']
    perm=permissions.CAN_READ|permissions.CAN_EDIT|permissions.CAN_DELETE
    if cassapiperm.insert_user_datasource_perm(uid=uid, did=did, perm=perm):
        return True
    return False

def new_datasource_datapoint(params):
    if not 'uid' in params or not 'pid' in params:
        return False
    uid=params['uid']
    pid=params['pid']
    user_perm=permissions.CAN_READ|permissions.CAN_EDIT|permissions.CAN_DELETE
    if cassapiperm.insert_user_datapoint_perm(uid=uid, pid=pid, perm=user_perm):
        return True
    return False

def new_user_datapoint(params):
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
    return True


def delete_agent(aid):
    ''' This function revoke access to the agent '''
    perm=permissions.NONE
    agent=cassapiagent.get_agent(aid=aid)
    if agent:
        cassapiperm.insert_user_agent_perm(uid=agent.uid, aid=aid, perm=perm)
    return True

def delete_datasource(did):
    ''' This function revoke all access to the datasource by the user and its agent '''
    perm=permissions.NONE
    datasource=cassapidatasource.get_datasource(did=did)
    if datasource:
        cassapiperm.insert_user_datasource_perm(uid=datasource.uid, did=did, perm=perm)
        widgetds=cassapiwidget.get_widget_ds(did=datasource.did)
        if widgetds:
            cassapiperm.insert_user_widget_perm(uid=datasource.uid, wid=widgetds.wid, perm=perm)
        pids=cassapidatapoint.get_datapoints_pids(did=did)
        for pid in pids:
            cassapiperm.insert_user_datapoint_perm(uid=datasource.uid, pid=pid, perm=perm)
            widgetdp=cassapiwidget.get_widget_dp(pid=pid)
            if widgetdp:
                cassapiperm.insert_user_widget_perm(uid=datasource.uid, wid=widgetdp.wid, perm=perm)
    return True

def delete_datapoint(pid):
    ''' This function revoke all access to the datapoint by the user and its agent '''
    perm=permissions.NONE
    datapoint=cassapidatapoint.get_datapoint(pid=pid)
    if datapoint:
        cassapiperm.insert_user_datapoint_perm(uid=datapoint.uid, pid=pid, perm=perm)
        widgetdp=cassapiwidget.get_widget_dp(pid=pid)
        if widgetdp:
            cassapiperm.insert_user_widget_perm(uid=datapoint.uid, wid=widgetdp.wid, perm=perm)
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

def new_circle(params):
    if not 'uid' in params or not 'cid' in params:
        return False
    uid=params['uid']
    cid=params['cid']
    user_perm=permissions.CAN_READ|permissions.CAN_EDIT|permissions.CAN_DELETE
    if cassapiperm.insert_user_circle_perm(uid=uid, cid=cid, perm=user_perm):
        return True
    return False

def delete_circle(cid):
    ''' This function revoke all access to the circle passed '''
    perm=permissions.NONE
    circle=cassapicircle.get_circle(cid=cid)
    if circle:
        cassapiperm.insert_user_circle_perm(uid=circle.uid, cid=cid, perm=perm)
    return True

update_funcs = {
    Operations.NEW_AGENT: (new_agent,),
    Operations.NEW_DATASOURCE: (new_datasource,),
    Operations.NEW_DATASOURCE_DATAPOINT: (new_datasource_datapoint,),
    Operations.NEW_USER_DATAPOINT: (new_user_datapoint,),
    Operations.NEW_WIDGET: (new_widget,),
    Operations.NEW_DASHBOARD: (new_dashboard,),
    Operations.NEW_WIDGET_SYSTEM: (new_widget_system,),
    Operations.NEW_SNAPSHOT: (new_snapshot,),
    Operations.NEW_CIRCLE: (new_circle,),
    Operations.DELETE_USER: (delete_user,),
    Operations.DELETE_AGENT: (delete_agent,),
    Operations.DELETE_DATASOURCE: (delete_datasource,),
    Operations.DELETE_DATASOURCE_DATAPOINT: (delete_datapoint,),
    Operations.DELETE_USER_DATAPOINT: (delete_datapoint,),
    Operations.DELETE_WIDGET: (delete_widget,),
    Operations.DELETE_DASHBOARD: (delete_dashboard,),
    Operations.DELETE_SNAPSHOT: (delete_snapshot,),
    Operations.DELETE_CIRCLE: (delete_circle,),
    Operations.DISSOCIATE_DATAPOINT_FROM_DATASOURCE: (),
}

