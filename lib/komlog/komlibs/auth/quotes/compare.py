#coding: utf-8
'''
 compare.py 
 
 This file implements functions to compare quotes with segment limits

 @author: jcazor
 @date: 01/10/2013

'''

from komlog.komlibs.auth.model.quotes import Quotes
from komlog.komlibs.general.time import timeuuid
from komlog.komcass.api import quote as cassapiquote
from komlog.komcass.api import user as cassapiuser
from komlog.komcass.api import segment as cassapisegment
from komlog.komcass.api import datasource as cassapidatasource

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

def quo_daily_datasource_occupation(params):
    if not 'did' in params or not 'date' in params:
        return None
    did=params['did']
    date=params['date']
    dsinfo=cassapidatasource.get_datasource(did=did)
    if not dsinfo or not dsinfo.uid:
        return None
    uid=dsinfo.uid
    user=cassapiuser.get_user(uid=uid)
    if not user:
        return None
    segmentquo=cassapisegment.get_user_segment_quote(sid=user.segment, quote=Quotes.quo_daily_datasource_occupation.name)
    ts=timeuuid.get_day_timestamp(date)
    quo=cassapiquote.get_datasource_ts_quote(did=did, quote=Quotes.quo_daily_datasource_occupation.name, ts=ts)
    if segmentquo and quo:
        if quo.value>segmentquo.value:
            return True
    return False

def quo_daily_user_datasources_occupation(params):
    if not 'did' in params or not 'date' in params:
        return None
    did=params['did']
    date=params['date']
    dsinfo=cassapidatasource.get_datasource(did=did)
    if not dsinfo or not dsinfo.uid:
        return None
    uid=dsinfo.uid
    user=cassapiuser.get_user(uid=uid)
    if not user:
        return None
    segmentquo=cassapisegment.get_user_segment_quote(sid=user.segment, quote=Quotes.quo_daily_user_datasources_occupation.name)
    ts=timeuuid.get_day_timestamp(date)
    quo=cassapiquote.get_user_ts_quote(uid=uid, quote=Quotes.quo_daily_user_datasources_occupation.name, ts=ts)
    if segmentquo and quo:
        if quo.value>segmentquo.value:
            return True
    return False

def quo_total_user_occupation(params):
    '''
        Compare total occupation value with segment. If limit is surpassed, then deny the interface.
        If limit is not surpassed, delete the deny interface.
        If quote value is not found, then return None, indicating no further accion is needed.
    '''
    if not 'did' in params:
        return None
    did=params['did']
    dsinfo=cassapidatasource.get_datasource(did=did)
    if not dsinfo or not dsinfo.uid:
        return None
    user=cassapiuser.get_user(uid=dsinfo.uid)
    if not user:
        return None
    uid=user.uid
    quote=Quotes.quo_total_user_occupation.name
    segmentquo=cassapisegment.get_user_segment_quote(sid=user.segment, quote=quote)
    quo=cassapiquote.get_user_ts_quotes(uid=uid, quote=quote, count=1)
    if segmentquo and quo and quo[0].value>segmentquo.value:
        return True
    else:
        return False

quote_funcs = {
    Quotes.quo_daily_datasource_occupation:quo_daily_datasource_occupation,
    Quotes.quo_daily_user_datasources_occupation:quo_daily_user_datasources_occupation,
    Quotes.quo_static_agent_total_datapoints:quo_static_agent_total_datapoints,
    Quotes.quo_static_agent_total_datasources:quo_static_agent_total_datasources,
    Quotes.quo_static_circle_total_members:quo_static_circle_total_members,
    Quotes.quo_static_circle_total_members:quo_static_circle_total_members,
    Quotes.quo_static_datasource_total_datapoints:quo_static_datasource_total_datapoints,
    Quotes.quo_static_user_total_agents:quo_static_user_total_agents,
    Quotes.quo_static_user_total_circles:quo_static_user_total_circles,
    Quotes.quo_static_user_total_dashboards:quo_static_user_total_dashboards,
    Quotes.quo_static_user_total_datapoints:quo_static_user_total_datapoints,
    Quotes.quo_static_user_total_datasources:quo_static_user_total_datasources,
    Quotes.quo_static_user_total_snapshots:quo_static_user_total_snapshots,
    Quotes.quo_static_user_total_widgets:quo_static_user_total_widgets,
    Quotes.quo_total_user_occupation:quo_total_user_occupation,
}

