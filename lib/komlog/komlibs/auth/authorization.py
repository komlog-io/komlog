'''
This file is the entry point of authorization mechanisms

@author: jcazor
@date: 2013/12/08

'''

from komlog.komlibs.auth.quotes import authorization as quoauth
from komlog.komlibs.auth.resources import authorization as resauth
from komlog.komlibs.auth.tickets import authorization as ticketsauth
from komlog.komlibs.auth import exceptions
from komlog.komlibs.auth.errors import Errors
from komlog.komlibs.auth.model.requests import Requests
from komlog.komlibs.gestaccount.user.states import UserStates
from komlog.komlibs.gestaccount.agent.states import AgentStates
from komlog.komfig import logging

def authorize_request(*args, **kwargs):
    if len(args)>0:
        kwargs['request']=args[0]
    if len(args)>1:
        kwargs['passport']=args[1]
    request=kwargs.pop('request',None)
    if not request:
        raise exceptions.BadParametersException(error=Errors.E_AA_AR_BP)
    try:
        func_requests[request](**kwargs)
    except KeyError as e:
        logging.logger.error('Request not found: '+str(request))
        logging.logger.debug(str(type(e))+str(e))
        raise exceptions.RequestNotFoundException(error=Errors.E_AA_AR_RNF)
    except (SyntaxError, TypeError) as e:
        logging.logger.error('Request call error: '+str(request))
        logging.logger.debug(str(type(e))+str(e))
        raise exceptions.BadParametersException(error=Errors.E_AA_AR_FBP)

def authorize_new_agent_creation(passport):
    quoauth.authorize_new_agent(uid=passport.uid)

def authorize_get_agent_config(passport, aid):
    resauth.authorize_get_agent_config(uid=passport.uid, aid=aid)

def authorize_get_agents_config(passport):
    pass

def authorize_get_datasource_data(passport, did, ii, ie, tid):
    try:
        resauth.authorize_get_datasource_data(uid=passport.uid,did=did)
    except Exception as e:
        if ii and ie and tid:
            ticketsauth.authorize_get_datasource_data(uid=passport.uid, did=did, ii=ii, ie=ie, tid=tid)
        else:
            raise e
    quoauth.authorize_get_datasource_data(did=did, ii=ii, ie=ie)

def authorize_post_datasource_data(passport, did):
    resauth.authorize_post_datasource_data(uid=passport.uid,aid=passport.aid,did=did)
    quoauth.authorize_post_datasource_data(uid=passport.uid,did=did)

def authorize_post_datapoint_data(passport, pid):
    resauth.authorize_post_datapoint_data(uid=passport.uid,aid=passport.aid,pid=pid)
    quoauth.authorize_post_datapoint_data(uid=passport.uid,pid=pid)

def authorize_get_datasource_config(passport, did):
    resauth.authorize_get_datasource_config(uid=passport.uid,did=did)

def authorize_get_datasources_config(passport):
    pass

def authorize_update_datasource_config(passport, did):
    resauth.authorize_put_datasource_config(uid=passport.uid,did=did)

def authorize_new_datasource_creation(passport):
    quoauth.authorize_new_datasource(uid=passport.uid,aid=passport.aid)
    resauth.authorize_new_datasource(uid=passport.uid,aid=passport.aid)

def authorize_get_datapoint_data(passport, pid, ii, ie, tid):
    try:
        resauth.authorize_get_datapoint_data(uid=passport.uid,pid=pid)
    except Exception as e:
        if ii and ie and tid:
            ticketsauth.authorize_get_datapoint_data(uid=passport.uid, pid=pid, ii=ii, ie=ie, tid=tid)
        else:
            raise e
    quoauth.authorize_get_datapoint_data(pid=pid, ii=ii, ie=ie)

def authorize_get_datapoint_config(passport, pid):
    resauth.authorize_get_datapoint_config(uid=passport.uid,pid=pid)

def authorize_new_datasource_datapoint_creation(passport, did):
    quoauth.authorize_new_datasource_datapoint(uid=passport.uid,did=did)
    resauth.authorize_new_datasource_datapoint(uid=passport.uid,did=did)

def authorize_new_user_datapoint_creation(passport):
    quoauth.authorize_new_user_datapoint(uid=passport.uid,aid=passport.aid)
    resauth.authorize_new_user_datapoint(uid=passport.uid,aid=passport.aid)

def authorize_update_datapoint_config(passport, pid):
    resauth.authorize_put_datapoint_config(uid=passport.uid,pid=pid)

def authorize_update_user_config(passport):
    #If uid authentication was successfull, authorization to its own uid config is granted
    pass

def authorize_update_agent_config(passport, aid):
    resauth.authorize_put_agent_config(uid=passport.uid,aid=aid)

def authorize_get_widget_config(passport, wid):
    resauth.authorize_get_widget_config(uid=passport.uid,wid=wid)

def authorize_get_widgets_config(passport):
    pass

def authorize_update_widget_config(passport, wid):
    resauth.authorize_put_widget_config(uid=passport.uid,wid=wid)

def authorize_new_widget_creation(passport):
    quoauth.authorize_new_widget(uid=passport.uid)

def authorize_get_dashboard_config(passport, bid):
    resauth.authorize_get_dashboard_config(uid=passport.uid,bid=bid)

def authorize_get_dashboards_config(passport):
    pass

def authorize_update_dashboard_config(passport, bid):
    resauth.authorize_put_dashboard_config(uid=passport.uid,bid=bid)

def authorize_new_dashboard_creation(passport):
    quoauth.authorize_new_dashboard(uid=passport.uid)

def authorize_mark_positive_variable(passport, pid):
    resauth.authorize_mark_positive_variable(uid=passport.uid,pid=pid)

def authorize_mark_negative_variable(passport, pid):
    resauth.authorize_mark_negative_variable(uid=passport.uid,pid=pid)

def authorize_add_widget_to_dashboard(passport, bid, wid):
    resauth.authorize_add_widget_to_dashboard(uid=passport.uid,bid=bid,wid=wid)

def authorize_delete_widget_from_dashboard(passport, bid):
    resauth.authorize_delete_widget_from_dashboard(uid=passport.uid,bid=bid)

def authorize_delete_agent(passport, aid):
    resauth.authorize_delete_agent(uid=passport.uid,aid=aid)

def authorize_delete_datasource(passport, did):
    resauth.authorize_delete_datasource(uid=passport.uid,did=did)

def authorize_delete_datapoint(passport, pid):
    resauth.authorize_delete_datapoint(uid=passport.uid,pid=pid)

def authorize_delete_widget(passport, wid):
    resauth.authorize_delete_widget(uid=passport.uid,wid=wid)

def authorize_delete_dashboard(passport, bid):
    resauth.authorize_delete_dashboard(uid=passport.uid,bid=bid)

def authorize_add_datapoint_to_widget(passport, pid, wid):
    resauth.authorize_add_datapoint_to_widget(uid=passport.uid, pid=pid, wid=wid)

def authorize_delete_datapoint_from_widget(passport, wid):
    resauth.authorize_delete_datapoint_from_widget(uid=passport.uid, wid=wid)

def authorize_new_snapshot_creation(passport, wid):
    quoauth.authorize_new_snapshot(uid=passport.uid)
    resauth.authorize_new_snapshot(uid=passport.uid,wid=wid)

def authorize_get_snapshot_data(passport, nid):
    resauth.authorize_get_snapshot_data(uid=passport.uid,nid=nid)

def authorize_get_snapshot_config(passport, nid, tid):
    try:
        resauth.authorize_get_snapshot_config(uid=passport.uid,nid=nid)
    except Exception as e:
        if not tid:
            raise e
        else:
            ticketsauth.authorize_get_snapshot_config(uid=passport.uid, nid=nid, tid=tid)

def authorize_get_snapshots_config(passport):
    pass

def authorize_delete_snapshot(passport, nid):
    resauth.authorize_delete_snapshot(uid=passport.uid,nid=nid)

def authorize_new_circle_creation(passport):
    quoauth.authorize_new_circle(uid=passport.uid)

def authorize_get_circle_config(passport, cid):
    resauth.authorize_get_circle_config(uid=passport.uid,cid=cid)

def authorize_get_circles_config(passport):
    pass

def authorize_update_circle_config(passport, cid):
    resauth.authorize_update_circle_config(uid=passport.uid,cid=cid)

def authorize_delete_circle(passport, cid):
    resauth.authorize_delete_circle(uid=passport.uid,cid=cid)

def authorize_add_member_to_circle(passport, cid):
    quoauth.authorize_add_member_to_circle(uid=passport.uid, cid=cid)
    resauth.authorize_add_member_to_circle(uid=passport.uid, cid=cid)

def authorize_delete_member_from_circle(passport, cid):
    resauth.authorize_delete_member_from_circle(uid=passport.uid, cid=cid)

def authorize_delete_user(passport):
    pass

def authorize_get_user_config(passport):
    pass

def authorize_get_user_events(passport):
    pass

def authorize_disable_event(passport):
    pass

def authorize_response_event(passport):
    pass

def authorize_get_uri(passport):
    pass

def authorize_dissociate_datapoint_from_datasource(passport, pid):
    resauth.authorize_dissociate_datapoint_from_datasource(uid=passport.uid,pid=pid)

func_requests={
    Requests.ADD_DATAPOINT_TO_WIDGET:authorize_add_datapoint_to_widget,
    Requests.ADD_MEMBER_TO_CIRCLE:authorize_add_member_to_circle,
    Requests.ADD_WIDGET_TO_DASHBOARD:authorize_add_widget_to_dashboard,
    Requests.DELETE_AGENT:authorize_delete_agent,
    Requests.DELETE_CIRCLE:authorize_delete_circle,
    Requests.DELETE_DASHBOARD:authorize_delete_dashboard,
    Requests.DELETE_DATAPOINT:authorize_delete_datapoint,
    Requests.DELETE_DATAPOINT_FROM_WIDGET:authorize_delete_datapoint_from_widget,
    Requests.DELETE_DATASOURCE:authorize_delete_datasource,
    Requests.DELETE_MEMBER_FROM_CIRCLE:authorize_delete_member_from_circle,
    Requests.DELETE_SNAPSHOT:authorize_delete_snapshot,
    Requests.DELETE_USER:authorize_delete_user,
    Requests.DELETE_WIDGET:authorize_delete_widget,
    Requests.DELETE_WIDGET_FROM_DASHBOARD:authorize_delete_widget_from_dashboard,
    Requests.DISABLE_EVENT:authorize_disable_event,
    Requests.DISSOCIATE_DATAPOINT_FROM_DATASOURCE:authorize_dissociate_datapoint_from_datasource,
    Requests.GET_AGENT_CONFIG:authorize_get_agent_config,
    Requests.GET_AGENTS_CONFIG:authorize_get_agents_config,
    Requests.GET_CIRCLE_CONFIG:authorize_get_circle_config,
    Requests.GET_CIRCLES_CONFIG:authorize_get_circles_config,
    Requests.GET_DASHBOARD_CONFIG:authorize_get_dashboard_config,
    Requests.GET_DASHBOARDS_CONFIG:authorize_get_dashboards_config,
    Requests.GET_DATAPOINT_CONFIG:authorize_get_datapoint_config,
    Requests.GET_DATAPOINT_DATA:authorize_get_datapoint_data,
    Requests.GET_DATASOURCE_CONFIG:authorize_get_datasource_config,
    Requests.GET_DATASOURCES_CONFIG:authorize_get_datasources_config,
    Requests.GET_DATASOURCE_DATA:authorize_get_datasource_data,
    Requests.GET_SNAPSHOT_CONFIG:authorize_get_snapshot_config,
    Requests.GET_SNAPSHOTS_CONFIG:authorize_get_snapshots_config,
    Requests.GET_SNAPSHOT_DATA:authorize_get_snapshot_data,
    Requests.GET_URI:authorize_get_uri,
    Requests.GET_USER_CONFIG:authorize_get_user_config,
    Requests.GET_USER_EVENTS:authorize_get_user_events,
    Requests.GET_WIDGET_CONFIG:authorize_get_widget_config,
    Requests.GET_WIDGETS_CONFIG:authorize_get_widgets_config,
    Requests.MARK_NEGATIVE_VARIABLE:authorize_mark_negative_variable,
    Requests.MARK_POSITIVE_VARIABLE:authorize_mark_positive_variable,
    Requests.NEW_AGENT:authorize_new_agent_creation,
    Requests.NEW_CIRCLE:authorize_new_circle_creation,
    Requests.NEW_DASHBOARD:authorize_new_dashboard_creation,
    Requests.NEW_DATASOURCE_DATAPOINT:authorize_new_datasource_datapoint_creation,
    Requests.NEW_USER_DATAPOINT:authorize_new_user_datapoint_creation,
    Requests.NEW_DATASOURCE:authorize_new_datasource_creation,
    Requests.NEW_SNAPSHOT:authorize_new_snapshot_creation,
    Requests.NEW_WIDGET:authorize_new_widget_creation,
    Requests.UPDATE_AGENT_CONFIG:authorize_update_agent_config,
    Requests.UPDATE_CIRCLE_CONFIG:authorize_update_circle_config,
    Requests.UPDATE_DASHBOARD_CONFIG:authorize_update_dashboard_config,
    Requests.UPDATE_DATAPOINT_CONFIG:authorize_update_datapoint_config,
    Requests.UPDATE_DATASOURCE_CONFIG:authorize_update_datasource_config,
    Requests.UPDATE_USER_CONFIG:authorize_update_user_config,
    Requests.UPDATE_WIDGET_CONFIG:authorize_update_widget_config,
    Requests.POST_DATASOURCE_DATA:authorize_post_datasource_data,
    Requests.POST_DATAPOINT_DATA:authorize_post_datapoint_data,
    Requests.RESPONSE_EVENT:authorize_response_event,
}

