'''
 compare.py 
 
 This file implements functions to compare quotes with segment limits

 @author: jcazor
 @date: 01/10/2013

'''

from komlog.komlibs.auth import exceptions
from komlog.komlibs.auth.errors import Errors
from komlog.komlibs.auth.model.quotes import Quotes
from komlog.komlibs.general.time import timeuuid
from komlog.komcass.api import quote as cassapiquote
from komlog.komcass.api import user as cassapiuser
from komlog.komcass.api import segment as cassapisegment
from komlog.komcass.api import datasource as cassapidatasource

def quo_user_total_agents(params):
    try:
        uid=params['uid']
    except KeyError:
        raise exceptions.BadParametersException(error=Errors.E_AQC_QUTA_UIDNF)
    user=cassapiuser.get_user(uid=uid)
    if not user:
        raise exceptions.UserNotFoundException(error=Errors.E_AQC_QUTA_USRNF)
    quote=Quotes.quo_user_total_agents.name
    segmentquo=cassapisegment.get_user_segment_quote(sid=user.segment, quote=quote)
    userquo=cassapiquote.get_user_quote(uid=uid, quote=quote)
    if userquo and segmentquo:
        if userquo.value>segmentquo.value:
            return True
    return False


def quo_user_total_datasources(params):
    try:
        uid=params['uid']
    except KeyError:
        raise exceptions.BadParametersException(error=Errors.E_AQC_QUTDS_UIDNF)
    user=cassapiuser.get_user(uid=uid)
    if not user:
        raise exceptions.UserNotFoundException(error=Errors.E_AQC_QUTDS_USRNF)
    quote=Quotes.quo_user_total_datasources.name
    segmentquo=cassapisegment.get_user_segment_quote(sid=user.segment, quote=quote)
    userquo=cassapiquote.get_user_quote(uid=uid, quote=quote)
    if userquo and segmentquo:
        if userquo.value>segmentquo.value:
            return True
    return False

def quo_user_total_datapoints(params):
    try:
        uid=params['uid']
    except KeyError:
        raise exceptions.BadParametersException(error=Errors.E_AQC_QUTDP_UIDNF)
    user=cassapiuser.get_user(uid=uid)
    if not user:
        raise exceptions.UserNotFoundException(error=Errors.E_AQC_QUTDP_USRNF)
    quote=Quotes.quo_user_total_datapoints.name
    segmentquo=cassapisegment.get_user_segment_quote(sid=user.segment, quote=quote)
    userquo=cassapiquote.get_user_quote(uid=uid, quote=quote)
    if userquo and segmentquo:
        if userquo.value>segmentquo.value:
            return True
    return False

def quo_user_total_widgets(params):
    try:
        uid=params['uid']
    except KeyError:
        raise exceptions.BadParametersException(error=Errors.E_AQC_QUTW_UIDNF)
    user=cassapiuser.get_user(uid=uid)
    if not user:
        raise exceptions.UserNotFoundException(error=Errors.E_AQC_QUTW_USRNF)
    quote=Quotes.quo_user_total_widgets.name
    segmentquo=cassapisegment.get_user_segment_quote(sid=user.segment, quote=quote)
    userquo=cassapiquote.get_user_quote(uid=uid, quote=quote)
    if userquo and segmentquo:
        if userquo.value>segmentquo.value:
            return True
    return False

def quo_user_total_dashboards(params):
    try:
        uid=params['uid']
    except KeyError:
        raise exceptions.BadParametersException(error=Errors.E_AQC_QUTDB_UIDNF)
    user=cassapiuser.get_user(uid=uid)
    if not user:
        raise exceptions.UserNotFoundException(error=Errors.E_AQC_QUTDB_USRNF)
    quote=Quotes.quo_user_total_dashboards.name
    segmentquo=cassapisegment.get_user_segment_quote(sid=user.segment, quote=quote)
    userquo=cassapiquote.get_user_quote(uid=uid, quote=quote)
    if userquo and segmentquo:
        if userquo.value>segmentquo.value:
            return True
    return False

def quo_user_total_snapshots(params):
    try:
        uid=params['uid']
    except KeyError:
        raise exceptions.BadParametersException(error=Errors.E_AQC_QUTSN_UIDNF)
    user=cassapiuser.get_user(uid=uid)
    if not user:
        raise exceptions.UserNotFoundException(error=Errors.E_AQC_QUTSN_USRNF)
    quote=Quotes.quo_user_total_snapshots.name
    segmentquo=cassapisegment.get_user_segment_quote(sid=user.segment, quote=quote)
    userquo=cassapiquote.get_user_quote(uid=uid, quote=quote)
    if userquo and segmentquo:
        if userquo.value>segmentquo.value:
            return True
    return False

def quo_user_total_circles(params):
    try:
        uid=params['uid']
    except KeyError:
        raise exceptions.BadParametersException(error=Errors.E_AQC_QUTC_UIDNF)
    user=cassapiuser.get_user(uid=uid)
    if not user:
        raise exceptions.UserNotFoundException(error=Errors.E_AQC_QUTC_USRNF)
    quote=Quotes.quo_user_total_circles.name
    segmentquo=cassapisegment.get_user_segment_quote(sid=user.segment, quote=quote)
    userquo=cassapiquote.get_user_quote(uid=uid, quote=quote)
    if userquo and segmentquo:
        if userquo.value>segmentquo.value:
            return True
    return False

def quo_agent_total_datasources(params):
    try:
        uid=params['uid']
        aid=params['aid']
    except KeyError:
        raise exceptions.BadParametersException(error=Errors.E_AQC_QATDS_PNF)
    user=cassapiuser.get_user(uid=uid)
    if not user:
        raise exceptions.UserNotFoundException(error=Errors.E_AQC_QATDS_USRNF)
    quote=Quotes.quo_agent_total_datasources.name
    segmentquo=cassapisegment.get_user_segment_quote(sid=user.segment, quote=quote)
    agentquo=cassapiquote.get_agent_quote(aid=aid, quote=quote)
    if agentquo and segmentquo:
        if agentquo.value>segmentquo.value:
            return True
    return False

def quo_agent_total_datapoints(params):
    try:
        uid=params['uid']
        aid=params['aid']
    except KeyError:
        raise exceptions.BadParametersException(error=Errors.E_AQC_QATDP_PNF)
    user=cassapiuser.get_user(uid=uid)
    if not user:
        raise exceptions.UserNotFoundException(error=Errors.E_AQC_QATDP_USRNF)
    quote=Quotes.quo_agent_total_datapoints.name
    segmentquo=cassapisegment.get_user_segment_quote(sid=user.segment, quote=quote)
    agentquo=cassapiquote.get_agent_quote(aid=aid, quote=quote)
    if agentquo and segmentquo:
        if agentquo.value>segmentquo.value:
            return True
    return False

def quo_datasource_total_datapoints(params):
    try:
        uid=params['uid']
        did=params['did']
    except KeyError:
        raise exceptions.BadParametersException(error=Errors.E_AQC_QDSTDP_PNF)
    user=cassapiuser.get_user(uid=uid)
    if not user:
        raise exceptions.UserNotFoundException(error=Errors.E_AQC_QDSTDP_USRNF)
    quote=Quotes.quo_datasource_total_datapoints.name
    segmentquo=cassapisegment.get_user_segment_quote(sid=user.segment, quote=quote)
    dsquo=cassapiquote.get_datasource_quote(did=did, quote=quote)
    if dsquo and segmentquo:
        if dsquo.value>segmentquo.value:
            return True
    return False

def quo_circle_total_members(params):
    try:
        uid=params['uid']
        cid=params['cid']
    except KeyError:
        raise exceptions.BadParametersException(error=Errors.E_AQC_QCTM_PNF)
    user=cassapiuser.get_user(uid=uid)
    if not user:
        raise exceptions.UserNotFoundException(error=Errors.E_AQC_QCTM_USRNF)
    quote=Quotes.quo_circle_total_members.name
    segmentquo=cassapisegment.get_user_segment_quote(sid=user.segment, quote=quote)
    cquo=cassapiquote.get_circle_quote(cid=cid, quote=quote)
    if cquo and segmentquo:
        if cquo.value>segmentquo.value:
            return True
    return False

def quo_daily_datasource_occupation(params):
    try:
        did=params['did']
        date=params['date']
    except KeyError:
        raise exceptions.BadParametersException(error=Errors.E_AQC_QDDSO_PNF)
    dsinfo=cassapidatasource.get_datasource(did=did)
    if not dsinfo or not dsinfo.uid:
        raise exceptions.DatasourceNotFoundException(error=Errors.E_AQC_QDDSO_DSNF)
    uid=dsinfo.uid
    user=cassapiuser.get_user(uid=uid)
    if not user:
        raise exceptions.UserNotFoundException(error=Errors.E_AQC_QDDSO_USRNF)
    quote=Quotes.quo_daily_datasource_occupation.name
    segmentquo=cassapisegment.get_user_segment_quote(sid=user.segment, quote=quote)
    ts=timeuuid.get_day_timestamp(date)
    dsquo=cassapiquote.get_datasource_ts_quote(did=did, quote=quote, ts=ts)
    if segmentquo and dsquo:
        if dsquo.value>segmentquo.value:
            return True
    return False

def quo_daily_user_datasources_occupation(params):
    try:
        did=params['did']
        date=params['date']
    except KeyError:
        raise exceptions.BadParametersException(error=Errors.E_AQC_QDUDSO_PNF)
    dsinfo=cassapidatasource.get_datasource(did=did)
    if not dsinfo or not dsinfo.uid:
        raise exceptions.DatasourceNotFoundException(error=Errors.E_AQC_QDUDSO_DSNF)
    uid=dsinfo.uid
    user=cassapiuser.get_user(uid=uid)
    if not user:
        raise exceptions.UserNotFoundException(error=Errors.E_AQC_QDUDSO_USRNF)
    quote=Quotes.quo_daily_user_datasources_occupation.name
    segmentquo=cassapisegment.get_user_segment_quote(sid=user.segment, quote=quote)
    ts=timeuuid.get_day_timestamp(date)
    userquo=cassapiquote.get_user_ts_quote(uid=uid, quote=quote, ts=ts)
    if segmentquo and userquo:
        if userquo.value>segmentquo.value:
            return True
    return False

def quo_user_total_occupation(params):
    '''
        Compare total occupation value with segment. If limit is surpassed, then deny the interface.
        If limit is not surpassed, delete the deny interface.
        If quote value is not found, then return None, indicating no further accion is needed.
    '''
    try:
        did=params['did']
    except KeyError:
        raise exceptions.BadParametersException(error=Errors.E_AQC_QUTO_DIDNF)
    dsinfo=cassapidatasource.get_datasource(did=did)
    if not dsinfo or not dsinfo.uid:
        raise exceptions.DatasourceNotFoundException(error=Errors.E_AQC_QUTO_DSNF)
    user=cassapiuser.get_user(uid=dsinfo.uid)
    if not user:
        raise exceptions.UserNotFoundException(error=Errors.E_AQC_QUTO_USRNF)
    uid=user.uid
    quote=Quotes.quo_user_total_occupation.name
    segmentquo=cassapisegment.get_user_segment_quote(sid=user.segment, quote=quote)
    userquo=cassapiquote.get_user_ts_quotes(uid=uid, quote=quote, count=1)
    if segmentquo and userquo and userquo[0].value>segmentquo.value:
        return True
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

