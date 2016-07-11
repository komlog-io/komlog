'''
deny.py 

This file implements functions to deny access to resources because of quotes configuration


@author: jcazor
@date: 2013/11/13

'''

from komlog.komcass.api import user as cassapiuser
from komlog.komcass.api import interface as cassapiiface
from komlog.komcass.api import datasource as cassapidatasource
from komlog.komcass.api import segment as cassapisegment
from komlog.komcass.api import quote as cassapiquote
from komlog.komlibs.auth import exceptions
from komlog.komlibs.auth.errors import Errors
from komlog.komlibs.auth.model import interfaces
from komlog.komlibs.auth.model.quotes import Quotes
from komlog.komlibs.general.time import timeuuid
from komlog.komfig import logging

DEFAULT_PERM='A'

def quo_user_total_agents(params,deny):
    try:
        uid=params['uid']
    except KeyError:
        raise exceptions.BadParametersException(error=Errors.E_AQD_QUTA_UIDNF)
    iface=interfaces.User_AgentCreation().value
    if deny:
        if cassapiiface.insert_user_iface_deny(uid=uid, iface=iface, perm=DEFAULT_PERM):
            return True
    else:
        if cassapiiface.delete_user_iface_deny(uid=uid, iface=iface):
            return True
    return False

def quo_user_total_datasources(params,deny):
    try:
        uid=params['uid']
    except KeyError:
        raise exceptions.BadParametersException(error=Errors.E_AQD_QUTDS_UIDNF)
    iface=interfaces.User_DatasourceCreation().value
    if deny:
        if cassapiiface.insert_user_iface_deny(uid=uid, iface=iface, perm=DEFAULT_PERM):
            return True
    else:
        if cassapiiface.delete_user_iface_deny(uid=uid, iface=iface):
            return True
    return False

def quo_user_total_datapoints(params,deny):
    try:
        uid=params['uid']
    except KeyError:
        raise exceptions.BadParametersException(error=Errors.E_AQD_QUTDP_UIDNF)
    iface=interfaces.User_DatapointCreation().value
    if deny:
        if cassapiiface.insert_user_iface_deny(uid=uid, iface=iface, perm=DEFAULT_PERM):
            return True
    else:
        if cassapiiface.delete_user_iface_deny(uid=uid, iface=iface):
            return True
    return False

def quo_user_total_widgets(params,deny):
    try:
        uid=params['uid']
    except KeyError:
        raise exceptions.BadParametersException(error=Errors.E_AQD_QUTW_UIDNF)
    iface=interfaces.User_WidgetCreation().value
    if deny:
        if cassapiiface.insert_user_iface_deny(uid=uid, iface=iface, perm=DEFAULT_PERM):
            return True
    else:
        if cassapiiface.delete_user_iface_deny(uid=uid, iface=iface):
            return True
    return False

def quo_user_total_dashboards(params,deny):
    try:
        uid=params['uid']
    except KeyError:
        raise exceptions.BadParametersException(error=Errors.E_AQD_QUTDB_UIDNF)
    iface=interfaces.User_DashboardCreation().value
    if deny:
        if cassapiiface.insert_user_iface_deny(uid=uid, iface=iface, perm=DEFAULT_PERM):
            return True
    else:
        if cassapiiface.delete_user_iface_deny(uid=uid, iface=iface):
            return True
    return False

def quo_user_total_circles(params,deny):
    try:
        uid=params['uid']
    except KeyError:
        raise exceptions.BadParametersException(error=Errors.E_AQD_QUTC_UIDNF)
    iface=interfaces.User_CircleCreation().value
    if deny:
        if cassapiiface.insert_user_iface_deny(uid=uid, iface=iface, perm=DEFAULT_PERM):
            return True
    else:
        if cassapiiface.delete_user_iface_deny(uid=uid, iface=iface):
            return True
    return False

def quo_agent_total_datasources(params,deny):
    try:
        uid=params['uid']
        aid=params['aid']
    except KeyError:
        raise exceptions.BadParametersException(error=Errors.E_AQD_QATDS_PNF)
    iface=interfaces.Agent_DatasourceCreation(aid).value
    if deny:
        if cassapiiface.insert_user_iface_deny(uid=uid, iface=iface, perm=DEFAULT_PERM):
            return True
    else:
        if cassapiiface.delete_user_iface_deny(uid=uid, iface=iface):
            return True
    return False

def quo_agent_total_datapoints(params,deny):
    try:
        uid=params['uid']
        aid=params['aid']
    except KeyError:
        raise exceptions.BadParametersException(error=Errors.E_AQD_QATDP_PNF)
    iface=interfaces.Agent_DatapointCreation(aid).value
    uid=uid
    if deny:
        if cassapiiface.insert_user_iface_deny(uid=uid, iface=iface, perm=DEFAULT_PERM):
            return True
    else:
        if cassapiiface.delete_user_iface_deny(uid=uid, iface=iface):
            return True
    return False

def quo_datasource_total_datapoints(params,deny):
    try:
        uid=params['uid']
        did=params['did']
    except KeyError:
        raise exceptions.BadParametersException(error=Errors.E_AQD_QDSTDP_PNF)
    iface=interfaces.Datasource_DatapointCreation(did).value
    if deny:
        if cassapiiface.insert_user_iface_deny(uid=uid, iface=iface, perm=DEFAULT_PERM):
            return True
    else:
        if cassapiiface.delete_user_iface_deny(uid=uid, iface=iface):
            return True
    return False

def quo_user_total_snapshots(params,deny):
    try:
        uid=params['uid']
    except KeyError:
        raise exceptions.BadParametersException(error=Errors.E_AQD_QUTSN_UIDNF)
    iface=interfaces.User_SnapshotCreation().value
    if deny:
        if cassapiiface.insert_user_iface_deny(uid=uid, iface=iface, perm=DEFAULT_PERM):
            return True
    else:
        if cassapiiface.delete_user_iface_deny(uid=uid, iface=iface):
            return True
    return False

def quo_circle_total_members(params,deny):
    try:
        uid=params['uid']
        cid=params['cid']
    except KeyError:
        raise exceptions.BadParametersException(error=Errors.E_AQD_QCTM_PNF)
    iface=interfaces.User_AddMemberToCircle(cid).value
    if deny:
        if cassapiiface.insert_user_iface_deny(uid=uid, iface=iface, perm=DEFAULT_PERM):
            return True
    else:
        if cassapiiface.delete_user_iface_deny(uid=uid, iface=iface):
            return True
    return False

def quo_daily_datasource_occupation(params, deny):
    try:
        did=params['did']
        date=params['date']
    except KeyError:
        raise exceptions.BadParametersException(error=Errors.E_AQD_QDDSO_PNF)
    ts=timeuuid.get_day_timestamp(date)
    dsinfo=cassapidatasource.get_datasource(did=did)
    if not dsinfo or not dsinfo.uid:
        raise exceptions.DatasourceNotFoundException(error=Errors.E_AQD_QDDSO_DSNF)
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
    try:
        did=params['did']
        date=params['date']
    except KeyError:
        raise exceptions.BadParametersException(error=Errors.E_AQD_QDUDSO_PNF)
    ts=timeuuid.get_day_timestamp(date)
    dsinfo=cassapidatasource.get_datasource(did=did)
    if not dsinfo or not dsinfo.uid:
        raise exceptions.DatasourceNotFoundException(error=Errors.E_AQD_QDUDSO_DSNF)
    uid=dsinfo.uid
    iface=interfaces.User_PostDatasourceDataDaily().value
    if deny:
        if cassapiiface.insert_user_ts_iface_deny(uid=uid, iface=iface, ts=ts, perm=DEFAULT_PERM):
            return True
    else:
        if cassapiiface.delete_user_ts_iface_deny(uid=uid, iface=iface, ts=ts):
            return True
    return False

def quo_user_total_occupation(params, deny):
    ''' In this case, if we receive True, calculate the min timestamp where the occupation
        equals segment limit.
        if we received a False flag, the remove the deny interface.
    '''
    try:
        did=params['did']
    except KeyError:
        raise exceptions.BadParametersException(error=Errors.E_AQD_QUTO_DIDNF)
    dsinfo=cassapidatasource.get_datasource(did=did)
    if not dsinfo or not dsinfo.uid:
        raise exceptions.DatasourceNotFoundException(error=Errors.E_AQD_QUTO_DSNF)
    user=cassapiuser.get_user(uid=dsinfo.uid)
    if not user:
        raise exceptions.UserNotFoundException(error=Errors.E_AQD_QUTO_USRNF)
    uid=user.uid
    quote=Quotes.quo_user_total_occupation.name
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
    Quotes.quo_agent_total_datapoints:quo_agent_total_datapoints,
    Quotes.quo_agent_total_datasources:quo_agent_total_datasources,
    Quotes.quo_circle_total_members:quo_circle_total_members,
    Quotes.quo_circle_total_members:quo_circle_total_members,
    Quotes.quo_datasource_total_datapoints:quo_datasource_total_datapoints,
    Quotes.quo_user_total_agents:quo_user_total_agents,
    Quotes.quo_user_total_circles:quo_user_total_circles,
    Quotes.quo_user_total_dashboards:quo_user_total_dashboards,
    Quotes.quo_user_total_datapoints:quo_user_total_datapoints,
    Quotes.quo_user_total_datasources:quo_user_total_datasources,
    Quotes.quo_user_total_snapshots:quo_user_total_snapshots,
    Quotes.quo_user_total_widgets:quo_user_total_widgets,
    Quotes.quo_user_total_occupation:quo_user_total_occupation,
}

