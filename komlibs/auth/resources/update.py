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

def update_user_agent_perms(params,session):
    if not params.has_key('aid') or not params.has_key('uid'):
        return False
    aid=params['aid']
    uid=params['uid']
    perm='A'
    agent=cassapiagent.get_agent(session, aid)
    if agent and agent.uid==uid:
        if cassapiperm.insert_user_agent_perm(session, uid=uid, aid=aid, perm=perm):
            return True
    return False

def update_user_datasource_perms(params,session):
    if not params.has_key('did') or not params.has_key('uid') or not params.has_key('aid'):
        return False
    did=params['did']
    uid=params['uid']
    aid=params['aid']
    perm='A'
    datasource=cassapidatasource.get_datasource(session, did=did)
    agent=cassapiagent.get_agent(session, aid=aid)
    if agent and datasource and agent.uid==uid and datasource.aid==aid:
        if cassapiperm.insert_user_datasource_perm(session, uid=uid, did=did, perm=perm):
            return True
    return False

def update_agent_datasource_perms(params,session):
    if not params.has_key('did') or not params.has_key('uid') or not params.has_key('aid'):
        return False
    did=params['did']
    uid=params['uid']
    aid=params['aid']
    perm='A'
    datasource=cassapidatasource.get_datasource(session, did=did)
    agent=cassapiagent.get_agent(session, aid=aid)
    if agent and datasource and agent.uid==uid and datasource.aid==aid:
        if cassapiperm.insert_agent_datasource_perm(session, aid=aid, did=did, perm=perm):
            return True
    return False

def update_user_datapoint_perms(params,session):
    if not params.has_key('did') or not params.has_key('uid') \
    or not params.has_key('aid') or not params.has_key('pid'):
        return False
    did=params['did']
    uid=params['uid']
    aid=params['aid']
    pid=params['pid']
    perm='A'
    datapoint=cassapidatapoint.get_datapoint(session, pid=pid)
    datasource=cassapidatasource.get_datasource(session, did=did)
    agent=cassapiagent.get_agent(session, aid=aid)
    if agent and datasource and datapoint and agent.uid==uid and datasource.aid==aid and datapoint.did==did:
        if cassapiperm.insert_user_datapoint_perm(session, uid=uid, pid=pid, perm=perm):
            return True
    return False

def update_user_widget_perms(params,session):
    if not params.has_key('wid') or not params.has_key('uid'):
        return False
    wid=params['wid']
    uid=params['uid']
    perm='A'
    widget=cassapiwidget.get_widget(session, wid=wid)
    if widget and widget.uid==uid:
        if cassapiperm.insert_user_widget_perm(session, uid=uid, wid=wid, perm=perm):
            return True
    return False

def update_user_dashboard_perms(params,session):
    if not params.has_key('bid') or not params.has_key('uid'):
        return False
    bid=params['bid']
    uid=params['uid']
    perm='A'
    dashboard=cassapidashboard.get_dashboard(session, bid=bid)
    if dashboard and dashboard.uid==uid:
        if cassapiperm.insert_user_dashboard_perm(session, uid=uid, bid=bid, perm=perm):
            return True
    return False

