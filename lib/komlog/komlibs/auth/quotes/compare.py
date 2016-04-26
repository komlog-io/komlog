#coding: utf-8
'''
 compare.py 
 
 This file implements functions to compare quotes with segment limits

 @author: jcazor
 @date: 01/10/2013

'''

from komlog.komlibs.auth.model.quotes import Quotes
from komlog.komcass.api import quote as cassapiquote
from komlog.komcass.api import user as cassapiuser
from komlog.komcass.api import segment as cassapisegment

def quo_static_user_total_agents(params):
    if 'uid' not in params:
        return None
    uid=params['uid']
    user=cassapiuser.get_user(uid=uid)
    if not user:
        return None
    segmentquo=cassapisegment.get_user_segment_quote(sid=user.segment, quote=Quotes.quo_static_user_max_agents.name)
    userquo=cassapiquote.get_user_quote(uid=uid, quote=Quotes.quo_static_user_total_agents.name)
    if userquo and segmentquo:
        if userquo.value>segmentquo.value:
            return True
    return False


def quo_static_user_total_datasources(params):
    if 'uid' not in params:
        return None
    uid=params['uid']
    user=cassapiuser.get_user(uid=uid)
    if not user:
        return None
    segmentquo=cassapisegment.get_user_segment_quote(sid=user.segment, quote=Quotes.quo_static_user_max_datasources.name)
    userquo=cassapiquote.get_user_quote(uid=uid, quote=Quotes.quo_static_user_total_datasources.name)
    if userquo and segmentquo:
        if userquo.value>segmentquo.value:
            return True
    return False

def quo_static_user_total_datapoints(params):
    if 'uid' not in params:
        return None
    uid=params['uid']
    user=cassapiuser.get_user(uid=uid)
    if not user:
        return None
    segmentquo=cassapisegment.get_user_segment_quote(sid=user.segment, quote=Quotes.quo_static_user_max_datapoints.name)
    userquo=cassapiquote.get_user_quote(uid=uid, quote=Quotes.quo_static_user_total_datapoints.name)
    if userquo and segmentquo:
        if userquo.value>segmentquo.value:
            return True
    return False

def quo_static_user_total_widgets(params):
    if 'uid' not in params:
        return None
    uid=params['uid']
    user=cassapiuser.get_user(uid=uid)
    if not user:
        return None
    segmentquo=cassapisegment.get_user_segment_quote(sid=user.segment, quote=Quotes.quo_static_user_max_widgets.name)
    userquo=cassapiquote.get_user_quote(uid=uid, quote=Quotes.quo_static_user_total_widgets.name)
    if userquo and segmentquo:
        if userquo.value>segmentquo.value:
            return True
    return False

def quo_static_user_total_dashboards(params):
    if 'uid' not in params:
        return None
    uid=params['uid']
    user=cassapiuser.get_user(uid=uid)
    if not user:
        return None
    segmentquo=cassapisegment.get_user_segment_quote(sid=user.segment, quote=Quotes.quo_static_user_max_dashboards.name)
    userquo=cassapiquote.get_user_quote(uid=uid, quote=Quotes.quo_static_user_total_dashboards.name)
    if userquo and segmentquo:
        if userquo.value>segmentquo.value:
            return True
    return False

def quo_static_user_total_snapshots(params):
    if 'uid' not in params:
        return None
    uid=params['uid']
    user=cassapiuser.get_user(uid=uid)
    if not user:
        return None
    segmentquo=cassapisegment.get_user_segment_quote(sid=user.segment, quote=Quotes.quo_static_user_max_snapshots.name)
    userquo=cassapiquote.get_user_quote(uid=uid, quote=Quotes.quo_static_user_total_snapshots.name)
    if userquo and segmentquo:
        if userquo.value>segmentquo.value:
            return True
    return False

def quo_static_user_total_circles(params):
    if 'uid' not in params:
        return None
    uid=params['uid']
    user=cassapiuser.get_user(uid=uid)
    if not user:
        return None
    segmentquo=cassapisegment.get_user_segment_quote(sid=user.segment, quote=Quotes.quo_static_user_max_circles.name)
    userquo=cassapiquote.get_user_quote(uid=uid, quote=Quotes.quo_static_user_total_circles.name)
    if userquo and segmentquo:
        if userquo.value>segmentquo.value:
            return True
    return False

def quo_static_agent_total_datasources(params):
    if 'aid' not in params or 'uid' not in params:
        return None
    uid=params['uid']
    aid=params['aid']
    user=cassapiuser.get_user(uid=uid)
    if not user:
        return None
    segmentquo=cassapisegment.get_user_segment_quote(sid=user.segment, quote=Quotes.quo_static_agent_max_datasources.name)
    agentquo=cassapiquote.get_agent_quote(aid=aid, quote=Quotes.quo_static_agent_total_datasources.name)
    if agentquo and segmentquo:
        if agentquo.value>segmentquo.value:
            return True
    return False

def quo_static_agent_total_datapoints(params):
    if 'aid' not in params or 'uid' not in params:
        return None
    uid=params['uid']
    aid=params['aid']
    user=cassapiuser.get_user(uid=uid)
    if not user:
        return None
    segmentquo=cassapisegment.get_user_segment_quote(sid=user.segment, quote=Quotes.quo_static_agent_max_datapoints.name)
    agentquo=cassapiquote.get_agent_quote(aid=aid, quote=Quotes.quo_static_agent_total_datapoints.name)
    if agentquo and segmentquo:
        if agentquo.value>segmentquo.value:
            return True
    return False

def quo_static_datasource_total_datapoints(params):
    if 'did' not in params or 'uid' not in params:
        return None
    uid=params['uid']
    did=params['did']
    user=cassapiuser.get_user(uid=uid)
    if not user:
        return None
    segmentquo=cassapisegment.get_user_segment_quote(sid=user.segment, quote=Quotes.quo_static_datasource_max_datapoints.name)
    dsquo=cassapiquote.get_datasource_quote(did=did, quote=Quotes.quo_static_datasource_total_datapoints.name)
    if dsquo and segmentquo:
        if dsquo.value>segmentquo.value:
            return True
    return False

def quo_static_circle_total_members(params):
    if 'uid' not in params or 'cid' not in params:
        return None
    uid=params['uid']
    cid=params['cid']
    user=cassapiuser.get_user(uid=uid)
    if not user:
        return None
    segmentquo=cassapisegment.get_user_segment_quote(sid=user.segment, quote=Quotes.quo_static_circle_max_members.name)
    cquo=cassapiquote.get_circle_quote(cid=cid, quote=Quotes.quo_static_circle_total_members.name)
    if cquo and segmentquo:
        if cquo.value>segmentquo.value:
            return True
    return False

