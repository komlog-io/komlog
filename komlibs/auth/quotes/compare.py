#coding: utf-8
'''
 compare.py 
 
 This file implements functions to compare quotes with segment limits

 @author: jcazor
 @date: 01/10/2013

'''

from komcass import api as cassapi

def compare_quo_static_user_total_agents(params,cf):
    if not params.has_key('uid'):
        return None
    uid=params['uid']
    userquo=cassapi.get_user_quotes(uid,cf)
    userinfo=cassapi.get_userinfo(uid,{'segment':''},cf)
    if userinfo:
        seginfo=cassapi.get_segment_info(userinfo.segment,cf)
    else:
        return None
    if userquo and seginfo:
        quote=userquo.get_quote('quo_static_user_total_agents')
        limit=seginfo.get_param('quo_static_user_max_agents')
        if limit:
            if int(quote)>=int(limit)-1:
                return True
    return False


def compare_quo_static_user_total_graphs(params,cf):
    if not params.has_key('uid'):
        return None
    uid=params['uid']
    userquo=cassapi.get_user_quotes(uid,cf)
    userinfo=cassapi.get_userinfo(uid,{'segment':''},cf)
    if userinfo:
        seginfo=cassapi.get_segment_info(userinfo.segment,cf)
    else:
        return None
    if userquo and seginfo:
        quote=userquo.get_quote('quo_static_user_total_graphs')
        limit=seginfo.get_param('quo_static_user_max_graphs')
        if limit:
            print 'Comparing quota limits of quo_static_user_total_graphs: '+quote+' vs limit: '+limit
            if int(quote)>=int(limit)-1:
                return True
    return False

def compare_quo_static_user_total_datasources(params,cf):
    if not params.has_key('uid'):
        return None
    uid=params['uid']
    userquo=cassapi.get_user_quotes(uid,cf)
    userinfo=cassapi.get_userinfo(uid,{'segment':''},cf)
    if userinfo:
        seginfo=cassapi.get_segment_info(userinfo.segment,cf)
    else:
        return None
    if userquo and seginfo:
        quote=userquo.get_quote('quo_static_user_total_datasources')
        limit=seginfo.get_param('quo_static_user_max_datasources')
        if limit:
            print 'Comparing quota limits of quo_static_user_total_datasources: '+quote+' vs limit: '+limit
            if int(quote)>=int(limit)-1:
                return True
    return False

def compare_quo_static_user_total_datapoints(params,cf):
    if not params.has_key('uid'):
        return None
    uid=params['uid']
    userquo=cassapi.get_user_quotes(uid,cf)
    userinfo=cassapi.get_userinfo(uid,{'segment':''},cf)
    if userinfo:
        seginfo=cassapi.get_segment_info(userinfo.segment,cf)
    else:
        return None
    if userquo and seginfo:
        quote=userquo.get_quote('quo_static_user_total_datapoints')
        limit=seginfo.get_param('quo_static_user_max_datapoints')
        if limit:
            print 'Comparing quota limits of quo_static_user_total_datapoints: '+quote+' vs limit: '+limit
            if int(quote)>=int(limit)-1:
                return True
    return False

def compare_quo_static_user_total_widgets(params,cf):
    if not params.has_key('uid'):
        return None
    uid=params['uid']
    userquo=cassapi.get_user_quotes(uid,cf)
    userinfo=cassapi.get_userinfo(uid,{'segment':''},cf)
    if userinfo:
        seginfo=cassapi.get_segment_info(userinfo.segment,cf)
    else:
        return None
    if userquo and seginfo:
        quote=userquo.get_quote('quo_static_user_total_widgets')
        limit=seginfo.get_param('quo_static_user_max_widgets')
        if limit:
            if int(quote)>=int(limit)-1:
                return True
    return False

def compare_quo_static_user_total_dashboards(params,cf):
    if not params.has_key('uid'):
        return None
    uid=params['uid']
    userquo=cassapi.get_user_quotes(uid,cf)
    userinfo=cassapi.get_userinfo(uid,{'segment':''},cf)
    if userinfo:
        seginfo=cassapi.get_segment_info(userinfo.segment,cf)
    else:
        return None
    if userquo and seginfo:
        quote=userquo.get_quote('quo_static_user_total_dashboards')
        limit=seginfo.get_param('quo_static_user_max_dashboards')
        if limit:
            if int(quote)>=int(limit)-1:
                return True
    return False

def compare_quo_static_agent_total_datasources(params,cf):
    if not params.has_key('aid') or not params.has_key('uid'):
        return None
    aid=params['aid']
    uid=params['uid']
    agentquo=cassapi.get_agent_quotes(aid,cf)
    userinfo=cassapi.get_userinfo(uid,{'segment':''},cf)
    if userinfo:
        seginfo=cassapi.get_segment_info(userinfo.segment,cf)
    else:
        return None
    if agentquo and seginfo:
        quote=agentquo.get_quote('quo_static_agent_total_datasources')
        limit=seginfo.get_param('quo_static_agent_max_datasources')
        if limit:
            print 'Comparing quota limits of quo_static_agent_total_datasources: '+quote+' vs limit: '+limit
            if int(quote)>=int(limit)-1:
                return True
    return False

def compare_quo_static_agent_total_datapoints(params,cf):
    if not params.has_key('aid') or not params.has_key('uid'):
        return None
    aid=params['aid']
    uid=params['uid']
    agentquo=cassapi.get_agent_quotes(aid,cf)
    userinfo=cassapi.get_userinfo(uid,{'segment':''},cf)
    if userinfo:
        seginfo=cassapi.get_segment_info(userinfo.segment,cf)
    else:
        return None
    if agentquo and seginfo:
        quote=agentquo.get_quote('quo_static_agent_total_datapoints')
        limit=seginfo.get_param('quo_static_agent_max_datapoints')
        if limit:
            print 'Comparing quota limits of quo_static_agent_total_datapoints: '+quote+' vs limit: '+limit
            if int(quote)>=int(limit)-1:
                return True
    return False

def compare_quo_static_ds_total_datapoints(params,cf):
    if not params.has_key('did') or not params.has_key('uid'):
        return None
    did=params['did']
    uid=params['uid']
    dsquo=cassapi.get_ds_quotes(did,cf)
    userinfo=cassapi.get_userinfo(uid,{'segment':''},cf)
    if userinfo:
        seginfo=cassapi.get_segment_info(userinfo.segment,cf)
    else:
        return None
    if dsquo and seginfo:
        quote=dsquo.get_quote('quo_static_ds_total_datapoints')
        limit=seginfo.get_param('quo_static_ds_max_datapoints')
        if limit:
            print 'Comparing quota limits of quo_static_ds_total_datapoints: '+quote+' vs limit: '+limit
            if int(quote)>=int(limit)-1:
                return True
    return False

