'''
 update.py 
 
 This file implements functions to update quotes

 @author: jcazor
 @date: 01/10/2013

'''

from komlog.komcass.api import user as cassapiuser
from komlog.komcass.api import agent as cassapiagent
from komlog.komcass.api import datasource as cassapidatasource
from komlog.komcass.api import datapoint as cassapidatapoint
from komlog.komcass.api import widget as cassapiwidget
from komlog.komcass.api import dashboard as cassapidashboard
from komlog.komcass.api import snapshot as cassapisnapshot
from komlog.komcass.api import circle as cassapicircle
from komlog.komcass.api import quote as cassapiquote
from komlog.komlibs.auth import exceptions
from komlog.komlibs.auth.errors import Errors
from komlog.komlibs.auth.model.quotes import Quotes
from komlog.komlibs.general.time import timeuuid

def quo_user_total_agents(params):
    try:
        uid=params['uid']
    except KeyError:
        raise exceptions.BadParametersException(error=Errors.E_AQU_QUTA_UIDNF)
    user=cassapiuser.get_user(uid=uid)
    if not user:
        raise exceptions.UserNotFoundException(error=Errors.E_AQU_QUTA_USRNF)
    num_agents=cassapiagent.get_number_of_agents_by_uid(uid=uid)
    quote=Quotes.quo_user_total_agents.name
    cassapiquote.set_user_quote(uid=uid, quote=quote, value=num_agents)
    return num_agents

def quo_user_total_datasources(params):
    try:
        uid=params['uid']
    except KeyError:
        raise exceptions.BadParametersException(error=Errors.E_AQU_QUTDS_UIDNF)
    user=cassapiuser.get_user(uid=uid)
    if not user:
        raise exceptions.UserNotFoundException(error=Errors.E_AQU_QUTDS_USRNF)
    aids=cassapiagent.get_agents_aids(uid=uid)
    total_datasources=0
    for aid in aids:
        agent_datasources=cassapidatasource.get_number_of_datasources_by_aid(aid=aid)
        total_datasources+=agent_datasources
    quote=Quotes.quo_user_total_datasources.name
    cassapiquote.set_user_quote(uid=uid, quote=quote, value=total_datasources)
    return total_datasources

def quo_user_total_datapoints(params):
    try:
        uid=params['uid']
    except KeyError:
        raise exceptions.BadParametersException(error=Errors.E_AQU_QUTDP_UIDNF)
    user=cassapiuser.get_user(uid=uid)
    if not user:
        raise exceptions.UserNotFoundException(error=Errors.E_AQU_QUTDP_USRNF)
    total_datapoints=cassapidatapoint.get_number_of_datapoints_by_uid(uid=uid)
    quote=Quotes.quo_user_total_datapoints.name
    cassapiquote.set_user_quote(uid=uid, quote=quote, value=total_datapoints)
    return total_datapoints

def quo_user_total_widgets(params):
    try:
        uid=params['uid']
    except KeyError:
        raise exceptions.BadParametersException(error=Errors.E_AQU_QUTW_UIDNF)
    user=cassapiuser.get_user(uid=uid)
    if not user:
        raise exceptions.UserNotFoundException(error=Errors.E_AQU_QUTW_USRNF)
    num_widgets=cassapiwidget.get_number_of_widgets_by_uid(uid=uid)
    quote=Quotes.quo_user_total_widgets.name
    cassapiquote.set_user_quote(uid=uid, quote=quote, value=num_widgets)
    return num_widgets

def quo_user_total_dashboards(params):
    try:
        uid=params['uid']
    except KeyError:
        raise exceptions.BadParametersException(error=Errors.E_AQU_QUTDB_UIDNF)
    user=cassapiuser.get_user(uid=uid)
    if not user:
        raise exceptions.UserNotFoundException(error=Errors.E_AQU_QUTDB_USRNF)
    num_dashboards=cassapidashboard.get_number_of_dashboards_by_uid(uid=uid)
    quote=Quotes.quo_user_total_dashboards.name
    cassapiquote.set_user_quote(uid=uid, quote=quote, value=num_dashboards)
    return num_dashboards

def quo_agent_total_datasources(params):
    try:
        aid=params['aid']
    except KeyError:
        raise exceptions.BadParametersException(error=Errors.E_AQU_QATDS_AIDNF)
    agent=cassapiagent.get_agent(aid=aid)
    if not agent:
        raise exceptions.AgentNotFoundException(Errors.E_AQU_QATDS_AGNF)
    num_datasources=cassapidatasource.get_number_of_datasources_by_aid(aid=aid)
    quote=Quotes.quo_agent_total_datasources.name
    cassapiquote.set_agent_quote(aid=aid, quote=quote, value=num_datasources)
    return num_datasources

def quo_agent_total_datapoints(params):
    try:
        aid=params['aid']
    except KeyError:
        raise exceptions.BadParametersException(error=Errors.E_AQU_QATDP_AIDNF)
    agent=cassapiagent.get_agent(aid=aid)
    if not agent:
        raise exceptions.AgentNotFoundException(Errors.E_AQU_QATDP_AGNF)
    total_datapoints=0
    dids=cassapidatasource.get_datasources_dids(aid=aid)
    for did in dids:
        num_datapoints=cassapidatapoint.get_number_of_datapoints_by_did(did=did)
        total_datapoints+=num_datapoints
    quote=Quotes.quo_agent_total_datapoints.name
    cassapiquote.set_agent_quote(aid=aid, quote=quote, value=total_datapoints)
    return total_datapoints

def quo_datasource_total_datapoints(params):
    try:
        did=params['did']
    except KeyError:
        raise exceptions.BadParametersException(error=Errors.E_AQU_QDSTDP_DIDNF)
    ds=cassapidatasource.get_datasource(did=did)
    if not ds:
        raise exceptions.DatasourceNotFoundException(error=Errors.E_AQU_QDSTDP_DSNF)
    total_datapoints=cassapidatapoint.get_number_of_datapoints_by_did(did=did)
    quote=Quotes.quo_datasource_total_datapoints.name
    cassapiquote.set_datasource_quote(did=did, quote=quote, value=total_datapoints)
    return total_datapoints

def quo_user_total_snapshots(params):
    try:
        uid=params['uid']
    except KeyError:
        raise exceptions.BadParametersException(error=Errors.E_AQU_QUTSN_UIDNF)
    user=cassapiuser.get_user(uid=uid)
    if not user:
        raise exceptions.UserNotFoundException(error=Errors.E_AQU_QUTSN_USRNF)
    num_snapshots=cassapisnapshot.get_number_of_snapshots(uid=uid)
    quote=Quotes.quo_user_total_snapshots.name
    cassapiquote.set_user_quote(uid=uid, quote=quote, value=num_snapshots)
    return num_snapshots

def quo_user_total_circles(params):
    try:
        uid=params['uid']
    except KeyError:
        raise exceptions.BadParametersException(error=Errors.E_AQU_QUTC_UIDNF)
    user=cassapiuser.get_user(uid=uid)
    if not user:
        raise exceptions.UserNotFoundException(error=Errors.E_AQU_QUTC_USRNF)
    num_circles=cassapicircle.get_number_of_circles(uid=uid)
    quote=Quotes.quo_user_total_circles.name
    cassapiquote.set_user_quote(uid=uid, quote=quote, value=num_circles)
    return num_circles

def quo_circle_total_members(params):
    try:
        cid=params['cid']
    except KeyError:
        raise exceptions.BadParametersException(error=Errors.E_AQU_QCTM_CIDNF)
    circle=cassapicircle.get_circle(cid=cid)
    if not circle:
        raise exceptions.CircleNotFoundException(error=Errors.E_AQU_QCTM_CRNF)
    num_members=len(circle.members)
    quote=Quotes.quo_circle_total_members.name
    cassapiquote.set_circle_quote(cid=cid, quote=quote, value=num_members)
    return num_members

def quo_daily_datasource_occupation(params):
    try:
        did=params['did']
        date=params['date']
    except KeyError:
        raise exceptions.BadParametersException(error=Errors.E_AQU_QDDSO_PNF)
    size=cassapidatasource.get_datasource_metadata_size_at(did=did,date=date)
    if size is None:
        raise exceptions.DatasourceNotFoundException(error=Errors.E_AQU_QDDSO_DSNF)
    ts=timeuuid.get_day_timestamp(date)
    quote=Quotes.quo_daily_datasource_occupation.name
    new_size=cassapiquote.increment_datasource_ts_quote(did=did, quote=quote, ts=ts, value=size)
    return new_size

def quo_daily_user_datasources_occupation(params):
    try:
        did=params['did']
        date=params['date']
    except KeyError:
        raise exceptions.BadParametersException(error=Errors.E_AQU_QDUDSO_PNF)
    dsinfo=cassapidatasource.get_datasource(did=did)
    if dsinfo and dsinfo.uid:
        uid=dsinfo.uid
    else:
        raise exceptions.DatasourceNotFoundException(error=Errors.E_AQU_QDUDSO_DSNF)
    user=cassapiuser.get_user(uid=uid)
    if not user:
        raise exceptions.UserNotFoundException(error=Errors.E_AQU_QDUDSO_USRNF)
    size=cassapidatasource.get_datasource_metadata_size_at(did=did,date=date)
    if size is None:
        return 0
    ts=timeuuid.get_day_timestamp(date)
    quote=Quotes.quo_daily_user_datasources_occupation.name
    new_size=cassapiquote.increment_user_ts_quote(uid=uid, quote=quote, ts=ts, value=size)
    return new_size

def quo_user_total_occupation(params):
    '''
        We calculate the total occupation user data. This quote is calculated once hourly at most.
        Right now, we only measure the datasources occupation.
    '''
    try:
        did=params['did']
    except KeyError:
        raise exceptions.BadParametersException(error=Errors.E_AQU_QUTO_DIDNF)
    dsinfo=cassapidatasource.get_datasource(did=did)
    if dsinfo and dsinfo.uid:
        uid=dsinfo.uid
    else:
        raise exceptions.DatasourceNotFoundException(error=Errors.E_AQU_QUTO_DSNF)
    user=cassapiuser.get_user(uid=uid)
    if not user:
        raise exceptions.UserNotFoundException(error=Errors.E_AQU_QUTO_USRNF)
    quote=Quotes.quo_user_total_occupation.name
    ts=timeuuid.get_hour_timestamp(timeuuid.uuid1())
    value=0
    if cassapiquote.new_user_ts_quote(uid=uid, quote=quote, ts=ts, value=value):
        dsquote=Quotes.quo_daily_user_datasources_occupation.name
        value=cassapiquote.get_user_ts_quote_value_sum(uid=uid, quote=dsquote)
        n_val=cassapiquote.increment_user_ts_quote(uid=uid,quote=quote,ts=ts,value=value)
        if n_val is not None:
            return n_val
    return None

def quo_daily_user_data_post_counter(params):
    ''' Increment the daily counter of samples posted. The day is the day associated to the data,
        so a user could really send in a day more samples than the quote limit if the date of those
        samples is from different days. '''
    try:
        did=params['did']
        date=params['date']
    except KeyError:
        raise exceptions.BadParametersException(error=Errors.E_AQU_QDUDPC_PNF)
    dsinfo=cassapidatasource.get_datasource(did=did)
    if not dsinfo or not dsinfo.uid:
        raise exceptions.DatasourceNotFoundException(error=Errors.E_AQU_QDUDPC_DSNF)
    user=cassapiuser.get_user(uid=dsinfo.uid)
    if not user:
        raise exceptions.UserNotFoundException(error=Errors.E_AQU_QDUDPC_USRNF)
    ts=timeuuid.get_day_timestamp(date)
    quote=Quotes.quo_daily_user_data_post_counter.name
    new_counter=cassapiquote.increment_user_ts_quote(uid=dsinfo.uid,quote=quote,ts=ts,value=1)
    return new_counter

quote_funcs = {
    Quotes.quo_daily_datasource_occupation:quo_daily_datasource_occupation,
    Quotes.quo_daily_user_datasources_occupation:quo_daily_user_datasources_occupation,
    Quotes.quo_daily_user_data_post_counter:quo_daily_user_data_post_counter,
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

