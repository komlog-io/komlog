#coding: utf-8
'''
 compare.py 
 
 This file implements functions to compare quotes with segment limits

 @author: jcazor
 @date: 01/10/2013

'''

from komcass.api import quote as cassapiquote
from komcass.api import user as cassapiuser
from komcass.api import segment as cassapisegment

def compare_quo_static_user_total_agents(params):
    if 'uid' not in params:
        return None
    uid=params['uid']
    user=cassapiuser.get_user(uid=uid)
    if not user:
        return None
    segment=cassapisegment.get_user_segment(sid=user.segment)
    userquo=cassapiquote.get_user_quotes(uid=uid)
    if userquo and segment:
        quote=userquo.get_quote('quo_static_user_total_agents')
        limit=segment.get_param('quo_static_user_max_agents')
        if limit is not None and quote is not None:
            if int(quote)>=int(limit)-1:
                return True
    return False


def compare_quo_static_user_total_datasources(params):
    if 'uid' not in params:
        return None
    uid=params['uid']
    user=cassapiuser.get_user(uid=uid)
    if not user:
        return None
    segment=cassapisegment.get_user_segment(sid=user.segment)
    userquo=cassapiquote.get_user_quotes(uid=uid)
    if userquo and segment:
        quote=userquo.get_quote('quo_static_user_total_datasources')
        limit=segment.get_param('quo_static_user_max_datasources')
        if limit is not None and quote is not None:
            if int(quote)>=int(limit)-1:
                return True
    return False

def compare_quo_static_user_total_datapoints(params):
    if 'uid' not in params:
        return None
    uid=params['uid']
    user=cassapiuser.get_user(uid=uid)
    if not user:
        return None
    segment=cassapisegment.get_user_segment(sid=user.segment)
    userquo=cassapiquote.get_user_quotes(uid=uid)
    if userquo and segment:
        quote=userquo.get_quote('quo_static_user_total_datapoints')
        limit=segment.get_param('quo_static_user_max_datapoints')
        if limit is not None and quote is not None:
            if int(quote)>=int(limit)-1:
                return True
    return False

def compare_quo_static_user_total_widgets(params):
    if 'uid' not in params:
        return None
    uid=params['uid']
    user=cassapiuser.get_user(uid=uid)
    if not user:
        return None
    segment=cassapisegment.get_user_segment(sid=user.segment)
    userquo=cassapiquote.get_user_quotes(uid=uid)
    if userquo and segment:
        quote=userquo.get_quote('quo_static_user_total_widgets')
        limit=segment.get_param('quo_static_user_max_widgets')
        if limit is not None and quote is not None:
            if int(quote)>=int(limit)-1:
                return True
    return False

def compare_quo_static_user_total_dashboards(params):
    if 'uid' not in params:
        return None
    uid=params['uid']
    user=cassapiuser.get_user(uid=uid)
    if not user:
        return None
    segment=cassapisegment.get_user_segment(sid=user.segment)
    userquo=cassapiquote.get_user_quotes(uid=uid)
    if userquo and segment:
        quote=userquo.get_quote('quo_static_user_total_dashboards')
        limit=segment.get_param('quo_static_user_max_dashboards')
        if limit is not None and quote is not None:
            if int(quote)>=int(limit)-1:
                return True
    return False

def compare_quo_static_agent_total_datasources(params):
    if 'aid' not in params or 'uid' not in params:
        return None
    aid=params['aid']
    uid=params['uid']
    user=cassapiuser.get_user(uid=uid)
    if not user:
        return None
    segment=cassapisegment.get_user_segment(sid=user.segment)
    agentquo=cassapiquote.get_agent_quotes(aid=aid)
    if agentquo and segment:
        quote=agentquo.get_quote('quo_static_agent_total_datasources')
        limit=segment.get_param('quo_static_agent_max_datasources')
        if limit is not None and quote is not None:
            if int(quote)>=int(limit)-1:
                return True
    return False

def compare_quo_static_agent_total_datapoints(params):
    if 'aid' not in params or 'uid' not in params:
        return None
    aid=params['aid']
    uid=params['uid']
    user=cassapiuser.get_user(uid=uid)
    if not user:
        return None
    segment=cassapisegment.get_user_segment(sid=user.segment)
    agentquo=cassapiquote.get_agent_quotes(aid=aid)
    if agentquo and segment:
        quote=agentquo.get_quote('quo_static_agent_total_datapoints')
        limit=segment.get_param('quo_static_agent_max_datapoints')
        if limit is not None and quote is not None:
            if int(quote)>=int(limit)-1:
                return True
    return False

def compare_quo_static_datasource_total_datapoints(params):
    if 'did' not in params or 'uid' not in params:
        return None
    did=params['did']
    uid=params['uid']
    user=cassapiuser.get_user(uid=uid)
    if not user:
        return None
    segment=cassapisegment.get_user_segment(sid=user.segment)
    dsquo=cassapiquote.get_datasource_quotes(did=did)
    if dsquo and segment:
        quote=dsquo.get_quote('quo_static_datasource_total_datapoints')
        limit=segment.get_param('quo_static_datasource_max_datapoints')
        if limit is not None and quote is not None:
            if int(quote)>=int(limit)-1:
                return True
    return False

