#coding: utf-8
'''
update.py 

This file implements functions to update authorization to resources

@author: jcazor
@date: 2013/11/11

'''

from komcass.api import user as cassapiuser
from komcass.api import agent as cassapiagent
from komcass.api import datasource as cassapidatasource
from komcass.api import datapoint as cassapidatapoint
from komcass.api import widget as cassapiwidget
from komcass.api import dashboard as cassapidashboard
from komcass.api import permission as cassapiperm

def update_user_agent_perms(params):
    if 'aid' not in params or 'uid' not in params:
        return False
    aid=params['aid']
    uid=params['uid']
    perm='A'
    agent=cassapiagent.get_agent(aid)
    if agent and agent.uid==uid:
        if cassapiperm.insert_user_agent_perm(uid=uid, aid=aid, perm=perm):
            return True
    return False

def update_user_datasource_perms(params):
    if 'did' not in params or 'uid' not in params or 'aid' not in params:
        return False
    did=params['did']
    uid=params['uid']
    aid=params['aid']
    perm='A'
    datasource=cassapidatasource.get_datasource(did=did)
    agent=cassapiagent.get_agent(aid=aid)
    if agent and datasource and agent.uid==uid and datasource.aid==aid:
        if cassapiperm.insert_user_datasource_perm(uid=uid, did=did, perm=perm):
            return True
    return False

def update_agent_datasource_perms(params):
    if 'did' not in params or 'uid' not in params or 'aid' not in params:
        return False
    did=params['did']
    uid=params['uid']
    aid=params['aid']
    perm='A'
    datasource=cassapidatasource.get_datasource(did=did)
    agent=cassapiagent.get_agent(aid=aid)
    if agent and datasource and agent.uid==uid and datasource.aid==aid:
        if cassapiperm.insert_agent_datasource_perm(aid=aid, did=did, perm=perm):
            return True
    return False

def update_user_datapoint_perms(params):
    if 'did' not in params or 'uid' not in params \
    or 'aid' not in params or 'pid' not in params:
        return False
    did=params['did']
    uid=params['uid']
    aid=params['aid']
    pid=params['pid']
    perm='A'
    datapoint=cassapidatapoint.get_datapoint(pid=pid)
    datasource=cassapidatasource.get_datasource(did=did)
    agent=cassapiagent.get_agent(aid=aid)
    if agent and datasource and datapoint and agent.uid==uid and datasource.aid==aid and datapoint.did==did:
        if cassapiperm.insert_user_datapoint_perm(uid=uid, pid=pid, perm=perm):
            return True
    return False

def update_user_widget_perms(params):
    if 'wid' not in params or 'uid' not in params:
        return False
    wid=params['wid']
    uid=params['uid']
    perm='A'
    widget=cassapiwidget.get_widget(wid=wid)
    if widget and widget.uid==uid:
        if cassapiperm.insert_user_widget_perm(uid=uid, wid=wid, perm=perm):
            return True
    return False

def update_user_dashboard_perms(params):
    if 'bid' not in params or 'uid' not in params:
        return False
    bid=params['bid']
    uid=params['uid']
    perm='A'
    dashboard=cassapidashboard.get_dashboard(bid=bid)
    if dashboard and dashboard.uid==uid:
        if cassapiperm.insert_user_dashboard_perm(uid=uid, bid=bid, perm=perm):
            return True
    return False

