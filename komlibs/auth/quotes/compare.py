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
    if not params.has_key('uid'):
        return None
    uid=params['uid']
    user=cassapiuser.get_user(uid=uid)
    if user:
        segment=cassapisegment.get_user_segment(sid=user.segment)
    else:
        return None
    userquo=cassapiquote.get_user_quotes(uid=uid)
    if userquo and segment:
        quote=userquo.get_quote('quo_static_user_total_agents')
        limit=segment.get_param('quo_static_user_max_agents')
        if limit is not None and quote is not None:
            if int(quote)>=int(limit)-1:
                return True
    return False


def compare_quo_static_user_total_datasources(params):
    if not params.has_key('uid'):
        return None
    uid=params['uid']
    user=cassapiuser.get_user(uid=uid)
    if user:
        segment=cassapisegment.get_user_segment(sid=user.segment)
    else:
        return None
    userquo=cassapiquote.get_user_quotes(uid=uid)
    if userquo and segment:
        quote=userquo.get_quote('quo_static_user_total_datasources')
        limit=segment.get_param('quo_static_user_max_datasources')
        if limit is not None and quote is not None:
            if int(quote)>=int(limit)-1:
                return True
    return False

def compare_quo_static_user_total_datapoints(params):
    if not params.has_key('uid'):
        return None
    uid=params['uid']
    user=cassapiuser.get_user(uid=uid)
    if user:
        segment=cassapisegment.get_user_segment(sid=user.segment)
    else:
        return None
    userquo=cassapiquote.get_user_quotes(uid=uid)
    if userquo and segment:
        quote=userquo.get_quote('quo_static_user_total_datapoints')
        limit=segment.get_param('quo_static_user_max_datapoints')
        if limit is not None and quote is not None:
            if int(quote)>=int(limit)-1:
                return True
    return False

def compare_quo_static_user_total_widgets(params):
    if not params.has_key('uid'):
        return None
    uid=params['uid']
    user=cassapiuser.get_user(uid=uid)
    if user:
        segment=cassapisegment.get_user_segment(sid=user.segment)
    else:
        return None
    userquo=cassapiquote.get_user_quotes(uid=uid)
    if userquo and segment:
        quote=userquo.get_quote('quo_static_user_total_widgets')
        limit=segment.get_param('quo_static_user_max_widgets')
        if limit is not None and quote is not None:
            if int(quote)>=int(limit)-1:
                return True
    return False

def compare_quo_static_user_total_dashboards(params):
    if not params.has_key('uid'):
        return None
    uid=params['uid']
    user=cassapiuser.get_user(uid=uid)
    if user:
        segment=cassapisegment.get_user_segment(sid=user.segment)
    else:
        return None
    userquo=cassapiquote.get_user_quotes(uid=uid)
    if userquo and segment:
        quote=userquo.get_quote('quo_static_user_total_dashboards')
        limit=segment.get_param('quo_static_user_max_dashboards')
        if limit is not None and quote is not None:
            if int(quote)>=int(limit)-1:
                return True
    return False

def compare_quo_static_agent_total_datasources(params):
    if not params.has_key('aid') or not params.has_key('uid'):
        return None
    aid=params['aid']
    uid=params['uid']
    user=cassapiuser.get_user(uid=uid)
    if user:
        segment=cassapisegment.get_user_segment(sid=user.segment)
    else:
        return None
    agentquo=cassapiquote.get_agent_quotes(aid=aid)
    if agentquo and segment:
        quote=agentquo.get_quote('quo_static_agent_total_datasources')
        limit=segment.get_param('quo_static_agent_max_datasources')
        if limit is not None and quote is not None:
            if int(quote)>=int(limit)-1:
                return True
    return False

def compare_quo_static_agent_total_datapoints(params):
    if not params.has_key('aid') or not params.has_key('uid'):
        return None
    aid=params['aid']
    uid=params['uid']
    user=cassapiuser.get_user(uid=uid)
    if user:
        segment=cassapisegment.get_user_segment(sid=user.segment)
    else:
        return None
    agentquo=cassapiquote.get_agent_quotes(aid=aid)
    if agentquo and segment:
        quote=agentquo.get_quote('quo_static_agent_total_datapoints')
        limit=segment.get_param('quo_static_agent_max_datapoints')
        if limit is not None and quote is not None:
            if int(quote)>=int(limit)-1:
                return True
    return False

def compare_quo_static_datasource_total_datapoints(params):
    if not params.has_key('did') or not params.has_key('uid'):
        return None
    did=params['did']
    uid=params['uid']
    user=cassapiuser.get_user(uid=uid)
    if user:
        segment=cassapisegment.get_user_segment(sid=user.segment)
    else:
        return None
    dsquo=cassapiquote.get_datasource_quotes(did=did)
    if dsquo and segment:
        quote=dsquo.get_quote('quo_static_datasource_total_datapoints')
        limit=segment.get_param('quo_static_datasource_max_datapoints')
        if limit is not None and quote is not None:
            if int(quote)>=int(limit)-1:
                return True
    return False

