#coding: utf-8
'''
deny.py 

This file implements functions to deny access to resourcess because of quotes configuration


@author: jcazor
@date: 2013/11/13

'''

from komlog.komcass.api import user as cassapiuser
from komlog.komcass.api import interface as cassapiiface
from komlog.komcass.api import datasource as cassapidatasource
from komlog.komcass.api import segment as cassapisegment
from komlog.komcass.api import quote as cassapiquote
from komlog.komlibs.auth.model import interfaces
from komlog.komlibs.auth.model.quotes import Quotes
from komlog.komlibs.general.time import timeuuid
from komlog.komfig import logging

DEFAULT_PERM='A'

def quo_static_user_total_agents(params,deny):
    if 'uid' not in params:
        return False
    uid=params['uid']
    iface=interfaces.User_AgentCreation().value
    if deny:
        if cassapiiface.insert_user_iface_deny(uid=uid, iface=iface, perm=DEFAULT_PERM):
            return True
    else:
        if cassapiiface.delete_user_iface_deny(uid=uid, iface=iface):
            return True
    return False

def quo_static_user_total_datasources(params,deny):
    if 'uid' not in params:
        return False
    uid=params['uid']
    iface=interfaces.User_DatasourceCreation().value
    if deny:
        if cassapiiface.insert_user_iface_deny(uid=uid, iface=iface, perm=DEFAULT_PERM):
            return True
    else:
        if cassapiiface.delete_user_iface_deny(uid=uid, iface=iface):
            return True
    return False

def quo_static_user_total_datapoints(params,deny):
    if 'uid' not in params:
        return False
    uid=params['uid']
    iface=interfaces.User_DatapointCreation().value
    if deny:
        if cassapiiface.insert_user_iface_deny(uid=uid, iface=iface, perm=DEFAULT_PERM):
            return True
    else:
        if cassapiiface.delete_user_iface_deny(uid=uid, iface=iface):
            return True
    return False

def quo_static_user_total_widgets(params,deny):
    if 'uid' not in params:
        return False
    uid=params['uid']
    iface=interfaces.User_WidgetCreation().value
    if deny:
        if cassapiiface.insert_user_iface_deny(uid=uid, iface=iface, perm=DEFAULT_PERM):
            return True
    else:
        if cassapiiface.delete_user_iface_deny(uid=uid, iface=iface):
            return True
    return False

def quo_static_user_total_dashboards(params,deny):
    if 'uid' not in params:
        return False
    uid=params['uid']
    iface=interfaces.User_DashboardCreation().value
    if deny:
        if cassapiiface.insert_user_iface_deny(uid=uid, iface=iface, perm=DEFAULT_PERM):
            return True
    else:
        if cassapiiface.delete_user_iface_deny(uid=uid, iface=iface):
            return True
    return False

def quo_static_user_total_circles(params,deny):
    if 'uid' not in params:
        return False
    uid=params['uid']
    iface=interfaces.User_CircleCreation().value
    if deny:
        if cassapiiface.insert_user_iface_deny(uid=uid, iface=iface, perm=DEFAULT_PERM):
            return True
    else:
        if cassapiiface.delete_user_iface_deny(uid=uid, iface=iface):
            return True
    return False

def quo_static_agent_total_datasources(params,deny):
    if 'aid' not in params or 'uid' not in params:
        return False
    aid=params['aid']
    uid=params['uid']
    iface=interfaces.Agent_DatasourceCreation(aid).value
    if deny:
        if cassapiiface.insert_user_iface_deny(uid=uid, iface=iface, perm=DEFAULT_PERM):
            return True
    else:
        if cassapiiface.delete_user_iface_deny(uid=uid, iface=iface):
            return True
    return False

def quo_static_agent_total_datapoints(params,deny):
    if 'aid' not in params or 'uid' not in params:
        return False
    aid=params['aid']
    uid=params['uid']
    iface=interfaces.Agent_DatapointCreation(aid).value
    uid=uid
    if deny:
        if cassapiiface.insert_user_iface_deny(uid=uid, iface=iface, perm=DEFAULT_PERM):
            return True
    else:
        if cassapiiface.delete_user_iface_deny(uid=uid, iface=iface):
            return True
    return False

def quo_static_datasource_total_datapoints(params,deny):
    if 'did' not in params or 'uid' not in params:
        return False
    did=params['did']
    uid=params['uid']
    iface=interfaces.Datasource_DatapointCreation(did).value
    if deny:
        if cassapiiface.insert_user_iface_deny(uid=uid, iface=iface, perm=DEFAULT_PERM):
            return True
    else:
        if cassapiiface.delete_user_iface_deny(uid=uid, iface=iface):
            return True
    return False

def quo_static_user_total_snapshots(params,deny):
    if 'uid' not in params:
        return False
    uid=params['uid']
    iface=interfaces.User_SnapshotCreation().value
    if deny:
        if cassapiiface.insert_user_iface_deny(uid=uid, iface=iface, perm=DEFAULT_PERM):
            return True
    else:
        if cassapiiface.delete_user_iface_deny(uid=uid, iface=iface):
            return True
    return False

def quo_static_circle_total_members(params,deny):
    if 'uid' not in params or 'cid' not in params:
        return False
    uid=params['uid']
    cid=params['cid']
    iface=interfaces.User_AddMemberToCircle(cid).value
    if deny:
        if cassapiiface.insert_user_iface_deny(uid=uid, iface=iface, perm=DEFAULT_PERM):
            return True
    else:
        if cassapiiface.delete_user_iface_deny(uid=uid, iface=iface):
            return True
    return False

def quo_daily_datasource_occupation(params, deny):
    if 'did' not in params or 'date' not in params:
        return False
    did=params['did']
    date=params['date']
    ts=timeuuid.get_day_timestamp(date)
    dsinfo=cassapidatasource.get_datasource(did=did)
    if not dsinfo or not dsinfo.uid:
        return False
    uid=dsinfo.uid
    iface=interfaces.User_PostDatasourceDataDaily(did=did).value
    if deny:
        if cassapiiface.insert_user_ts_iface_deny(uid=uid, iface=iface, ts=ts, perm=DEFAULT_PERM):
            return True
    else:
        if cassapiiface.delete_user_ts_iface_deny(uid=uid, iface=iface, ts=ts):
            return True
    return False

def quo_daily_user_datasources_occupation(params, deny):
    if 'did' not in params or 'date' not in params:
        return False
    did=params['did']
    date=params['date']
    ts=timeuuid.get_day_timestamp(date)
    dsinfo=cassapidatasource.get_datasource(did=did)
    if not dsinfo or not dsinfo.uid:
        return False
    uid=dsinfo.uid
    iface=interfaces.User_PostDatasourceDataDaily().value
    if deny:
        if cassapiiface.insert_user_ts_iface_deny(uid=uid, iface=iface, ts=ts, perm=DEFAULT_PERM):
            return True
    else:
        if cassapiiface.delete_user_ts_iface_deny(uid=uid, iface=iface, ts=ts):
            return True
    return False

def quo_total_user_occupation(params, deny):
    ''' In this case, if we receive True, calculate the min timestamp where the occupation
        equals segment limit.
        if we received a False flag, the remove the deny interface.
    '''
    if not 'did' in params:
        return False
    did=params['did']
    dsinfo=cassapidatasource.get_datasource(did=did)
    if not dsinfo or not dsinfo.uid:
        return False
    user=cassapiuser.get_user(uid=dsinfo.uid)
    if not user:
        return False
    uid=user.uid
    quote=Quotes.quo_total_user_occupation.name
    iface=interfaces.User_DataRetrievalMinTimestamp().value
    if deny:
        segmentquo=cassapisegment.get_user_segment_quote(sid=user.segment, quote=quote)
        if segmentquo is None:
            return False
        dsquote=Quotes.quo_daily_user_datasources_occupation.name
        daily_occupations=cassapiquote.get_user_ts_quotes(uid=uid, quote=dsquote)
        min_ts=None
        total_occupation=0
        for daily_occupation in daily_occupations:
            total_occupation+=daily_occupation.value
            if total_occupation>segmentquo.value:
                min_ts=timeuuid.min_uuid_from_time(daily_occupation.ts).hex
        if min_ts:
            if cassapiiface.insert_user_iface_deny(uid=uid, iface=iface, perm=min_ts):
                return True
            else:
                return False
        else:
            return True
    elif cassapiiface.delete_user_iface_deny(uid=uid, iface=iface):
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

