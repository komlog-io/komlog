'''
@author: komlog crew
'''

import json
from komlog.komcass.model.orm import events as ormevents
from komlog.komcass.model.parametrization.events import types
from komlog.komcass.model.statement import events as stmtevents
from komlog.komcass import connection, exceptions


@exceptions.ExceptionHandler
def get_user_event(uid, date):
    row=connection.session.execute(stmtevents.S_A_DATUSEREVENTS_B_UID_DATE,(uid,date))
    if row:
        return _get_user_event(ormevents.UserEvent(**row[0]))
    else:
        return None

@exceptions.ExceptionHandler
def get_disabled_user_event(uid, date):
    row=connection.session.execute(stmtevents.S_A_DATUSEREVENTSDISABLED_B_UID_DATE,(uid,date))
    if row:
        return _get_user_event(ormevents.UserEvent(**row[0]))
    else:
        return None

@exceptions.ExceptionHandler
def get_user_events(uid, end_date=None, from_date=None, count=None):
    events=[]
    if end_date and from_date:
        row=connection.session.execute(stmtevents.S_A_DATUSEREVENTS_B_UID_ENDDATE_FROMDATE,(uid,end_date,from_date))
    elif end_date:
        row=connection.session.execute(stmtevents.S_A_DATUSEREVENTS_B_UID_ENDDATE_COUNT,(uid,end_date,count))
    elif from_date:
        row=connection.session.execute(stmtevents.S_A_DATUSEREVENTS_B_UID_FROMDATE,(uid,from_date))
    else:
        return events
    if row:
        for r in row:
            event=_get_user_event(ormevents.UserEvent(**r))
            if event:
                events.append(event)
    return events

@exceptions.ExceptionHandler
def get_disabled_user_events(uid, end_date=None, from_date=None, count=None):
    events=[]
    if end_date and from_date:
        row=connection.session.execute(stmtevents.S_A_DATUSEREVENTSDISABLED_B_UID_ENDDATE_FROMDATE,(uid,end_date,from_date))
    elif end_date:
        row=connection.session.execute(stmtevents.S_A_DATUSEREVENTSDISABLED_B_UID_ENDDATE_COUNT,(uid,end_date,count))
    elif from_date:
        row=connection.session.execute(stmtevents.S_A_DATUSEREVENTSDISABLED_B_UID_FROMDATE,(uid,from_date))
    else:
        return events
    if row:
        for r in row:
            event=_get_user_event(ormevents.UserEvent(**r))
            if event:
                events.append(event)
    return events

def _get_user_event(event):
    if not isinstance(event, ormevents.UserEvent):
        return None
    else:
        try:
            return get_user_event_funcs[event.type](event)
        except KeyError:
            return None

@exceptions.ExceptionHandler
def _get_user_event_notification_new_user(event):
    event_info=connection.session.execute(stmtevents.S_A_DATUENOTIFNEWUSER_B_UID_DATE,(event.uid, event.date))
    if event_info:
        return ormevents.UserEventNotificationNewUser(uid=event.uid, date=event.date, priority=event.priority, username=event_info[0]['username'])
    else:
        return None

@exceptions.ExceptionHandler
def _get_user_event_notification_new_agent(event):
    event_info=connection.session.execute(stmtevents.S_A_DATUENOTIFNEWAGENT_B_UID_DATE,(event.uid, event.date))
    if event_info:
        return ormevents.UserEventNotificationNewAgent(uid=event.uid, date=event.date, priority=event.priority, aid=event_info[0]['aid'], agentname=event_info[0]['agentname'])
    else:
        return None

@exceptions.ExceptionHandler
def _get_user_event_notification_new_datasource(event):
    event_info=connection.session.execute(stmtevents.S_A_DATUENOTIFNEWDATASOURCE_B_UID_DATE,(event.uid, event.date))
    if event_info:
        return ormevents.UserEventNotificationNewDatasource(uid=event.uid, date=event.date, priority=event.priority, aid=event_info[0]['aid'], did=event_info[0]['did'], datasourcename=event_info[0]['datasourcename'])
    else:
        return None

@exceptions.ExceptionHandler
def _get_user_event_notification_new_datapoint(event):
    event_info=connection.session.execute(stmtevents.S_A_DATUENOTIFNEWDATAPOINT_B_UID_DATE,(event.uid, event.date))
    if event_info:
        return ormevents.UserEventNotificationNewDatapoint(uid=event.uid, date=event.date, priority=event.priority, did=event_info[0]['did'], pid=event_info[0]['pid'], datasourcename=event_info[0]['datasourcename'], datapointname=event_info[0]['datapointname'])
    else:
        return None

@exceptions.ExceptionHandler
def _get_user_event_notification_new_widget(event):
    event_info=connection.session.execute(stmtevents.S_A_DATUENOTIFNEWWIDGET_B_UID_DATE,(event.uid, event.date))
    if event_info:
        return ormevents.UserEventNotificationNewWidget(uid=event.uid, date=event.date, priority=event.priority, wid=event_info[0]['wid'], widgetname=event_info[0]['widgetname'])
    else:
        return None

@exceptions.ExceptionHandler
def _get_user_event_notification_new_dashboard(event):
    event_info=connection.session.execute(stmtevents.S_A_DATUENOTIFNEWDASHBOARD_B_UID_DATE,(event.uid, event.date))
    if event_info:
        return ormevents.UserEventNotificationNewDashboard(uid=event.uid, date=event.date, priority=event.priority, bid=event_info[0]['bid'], dashboardname=event_info[0]['dashboardname'])
    else:
        return None

@exceptions.ExceptionHandler
def _get_user_event_notification_new_circle(event):
    event_info=connection.session.execute(stmtevents.S_A_DATUENOTIFNEWCIRCLE_B_UID_DATE,(event.uid, event.date))
    if event_info:
        return ormevents.UserEventNotificationNewCircle(uid=event.uid, date=event.date, priority=event.priority, cid=event_info[0]['cid'], circlename=event_info[0]['circlename'])
    else:
        return None

@exceptions.ExceptionHandler
def _get_user_event_notification_new_snapshot_shared(event):
    event_info=connection.session.execute(stmtevents.S_A_DATUENOTIFNEWSNAPSHOTSHARED_B_UID_DATE,(event.uid, event.date))
    if event_info:
        return ormevents.UserEventNotificationNewSnapshotShared(uid=event.uid, date=event.date, priority=event.priority, nid=event_info[0]['nid'],tid=event_info[0]['tid'], widgetname=event_info[0]['widgetname'],shared_with_users=event_info[0]['shared_with_users'],shared_with_circles=event_info[0]['shared_with_circles'])
    else:
        return None

@exceptions.ExceptionHandler
def _get_user_event_notification_new_snapshot_shared_with_me(event):
    event_info=connection.session.execute(stmtevents.S_A_DATUENOTIFNEWSNAPSHOTSHAREDWITHME_B_UID_DATE,(event.uid, event.date))
    if event_info:
        return ormevents.UserEventNotificationNewSnapshotSharedWithMe(uid=event.uid, date=event.date, priority=event.priority, nid=event_info[0]['nid'],tid=event_info[0]['tid'], widgetname=event_info[0]['widgetname'],username=event_info[0]['username'])
    else:
        return None

@exceptions.ExceptionHandler
def _get_user_event_intervention_datapoint_identification(event):
    event_info=connection.session.execute(stmtevents.S_A_DATUEINTERVDPIDENTIFICATION_B_UID_DATE,(event.uid, event.date))
    if event_info:
        return ormevents.UserEventInterventionDatapointIdentification(uid=event.uid, date=event.date, priority=event.priority, pid=event_info[0]['pid'], datasourcename=event_info[0]['datasourcename'], datapointname=event_info[0]['datapointname'])
    else:
        return None

def insert_user_event(event):
    if not isinstance(event, ormevents.UserEvent):
        return False
    else:
        try:
            return insert_user_event_funcs[event.type](event)
        except KeyError:
            return None

@exceptions.ExceptionHandler
def _insert_user_event_notification_new_user(event):
    if not isinstance(event, ormevents.UserEventNotificationNewUser):
        return False
    else:
        connection.session.execute(stmtevents.I_A_DATUSEREVENTS,(event.uid,event.date,event.priority,types.USER_EVENT_NOTIFICATION_NEW_USER))
        connection.session.execute(stmtevents.I_A_DATUENOTIFNEWUSER, (event.uid, event.date, event.username))
        return True

@exceptions.ExceptionHandler
def _insert_user_event_notification_new_agent(event):
    if not isinstance(event, ormevents.UserEventNotificationNewAgent):
        return False
    else:
        connection.session.execute(stmtevents.I_A_DATUSEREVENTS,(event.uid,event.date,event.priority,types.USER_EVENT_NOTIFICATION_NEW_AGENT))
        connection.session.execute(stmtevents.I_A_DATUENOTIFNEWAGENT, (event.uid, event.date, event.aid, event.agentname))
        return True

@exceptions.ExceptionHandler
def _insert_user_event_notification_new_datasource(event):
    if not isinstance(event, ormevents.UserEventNotificationNewDatasource):
        return False
    else:
        connection.session.execute(stmtevents.I_A_DATUSEREVENTS,(event.uid,event.date,event.priority,types.USER_EVENT_NOTIFICATION_NEW_DATASOURCE))
        connection.session.execute(stmtevents.I_A_DATUENOTIFNEWDATASOURCE, (event.uid, event.date, event.aid, event.did, event.datasourcename))
        return True

@exceptions.ExceptionHandler
def _insert_user_event_notification_new_datapoint(event):
    if not isinstance(event, ormevents.UserEventNotificationNewDatapoint):
        return False
    else:
        connection.session.execute(stmtevents.I_A_DATUSEREVENTS,(event.uid,event.date,event.priority,types.USER_EVENT_NOTIFICATION_NEW_DATAPOINT))
        connection.session.execute(stmtevents.I_A_DATUENOTIFNEWDATAPOINT, (event.uid, event.date, event.did, event.pid, event.datasourcename, event.datapointname))
        return True

@exceptions.ExceptionHandler
def _insert_user_event_notification_new_widget(event):
    if not isinstance(event, ormevents.UserEventNotificationNewWidget):
        return False
    else:
        connection.session.execute(stmtevents.I_A_DATUSEREVENTS,(event.uid,event.date,event.priority,types.USER_EVENT_NOTIFICATION_NEW_WIDGET))
        connection.session.execute(stmtevents.I_A_DATUENOTIFNEWWIDGET, (event.uid, event.date, event.wid, event.widgetname))
        return True

@exceptions.ExceptionHandler
def _insert_user_event_notification_new_dashboard(event):
    if not isinstance(event, ormevents.UserEventNotificationNewDashboard):
        return False
    else:
        connection.session.execute(stmtevents.I_A_DATUSEREVENTS,(event.uid,event.date,event.priority,types.USER_EVENT_NOTIFICATION_NEW_DASHBOARD))
        connection.session.execute(stmtevents.I_A_DATUENOTIFNEWDASHBOARD, (event.uid, event.date, event.bid, event.dashboardname))
        return True

@exceptions.ExceptionHandler
def _insert_user_event_notification_new_circle(event):
    if not isinstance(event, ormevents.UserEventNotificationNewCircle):
        return False
    else:
        connection.session.execute(stmtevents.I_A_DATUSEREVENTS,(event.uid,event.date,event.priority,types.USER_EVENT_NOTIFICATION_NEW_CIRCLE))
        connection.session.execute(stmtevents.I_A_DATUENOTIFNEWCIRCLE, (event.uid, event.date, event.cid, event.circlename))
        return True

@exceptions.ExceptionHandler
def _insert_user_event_intervention_datapoint_identification(event):
    if not isinstance(event, ormevents.UserEventInterventionDatapointIdentification):
        return False
    else:
        connection.session.execute(stmtevents.I_A_DATUSEREVENTS,(event.uid,event.date,event.priority,types.USER_EVENT_INTERVENTION_DATAPOINT_IDENTIFICATION))
        connection.session.execute(stmtevents.I_A_DATUEINTERVDPIDENTIFICATION, (event.uid, event.date, event.pid, event.datasourcename, event.datapointname))
        return True

@exceptions.ExceptionHandler
def _insert_user_event_notification_new_snapshot_shared(event):
    if not isinstance(event, ormevents.UserEventNotificationNewSnapshotShared):
        return False
    else:
        connection.session.execute(stmtevents.I_A_DATUSEREVENTS,(event.uid,event.date,event.priority,types.USER_EVENT_NOTIFICATION_NEW_SNAPSHOT_SHARED))
        connection.session.execute(stmtevents.I_A_DATUENOTIFNEWSNAPSHOTSHARED, (event.uid, event.date, event.nid, event.tid, event.widgetname, event.shared_with_users, event.shared_with_circles))
        return True

@exceptions.ExceptionHandler
def _insert_user_event_notification_new_snapshot_shared_with_me(event):
    if not isinstance(event, ormevents.UserEventNotificationNewSnapshotSharedWithMe):
        return False
    else:
        connection.session.execute(stmtevents.I_A_DATUSEREVENTS,(event.uid,event.date,event.priority,types.USER_EVENT_NOTIFICATION_NEW_SNAPSHOT_SHARED_WITH_ME))
        connection.session.execute(stmtevents.I_A_DATUENOTIFNEWSNAPSHOTSHAREDWITHME, (event.uid, event.date, event.nid, event.tid, event.username, event.widgetname))
        return True

@exceptions.ExceptionHandler
def delete_user_events(uid):
    connection.session.execute(stmtevents.D_A_DATUSEREVENTS_B_UID,(uid,))
    connection.session.execute(stmtevents.D_A_DATUSEREVENTSDISABLED_B_UID,(uid,))
    connection.session.execute(stmtevents.D_A_DATUSEREVENTSDATASUMMARY_B_UID,(uid,))
    connection.session.execute(stmtevents.D_A_DATUENOTIFNEWUSER_B_UID,(uid,))
    connection.session.execute(stmtevents.D_A_DATUENOTIFNEWAGENT_B_UID,(uid,))
    connection.session.execute(stmtevents.D_A_DATUENOTIFNEWDATASOURCE_B_UID,(uid,))
    connection.session.execute(stmtevents.D_A_DATUENOTIFNEWDATAPOINT_B_UID,(uid,))
    connection.session.execute(stmtevents.D_A_DATUENOTIFNEWWIDGET_B_UID,(uid,))
    connection.session.execute(stmtevents.D_A_DATUENOTIFNEWDASHBOARD_B_UID,(uid,))
    connection.session.execute(stmtevents.D_A_DATUENOTIFNEWCIRCLE_B_UID,(uid,))
    connection.session.execute(stmtevents.D_A_DATUEINTERVDPIDENTIFICATION_B_UID,(uid,))
    connection.session.execute(stmtevents.D_A_DATUENOTIFNEWSNAPSHOTSHARED_B_UID,(uid,))
    connection.session.execute(stmtevents.D_A_DATUENOTIFNEWSNAPSHOTSHAREDWITHME_B_UID,(uid,))
    delete_user_events_responses_intervention_datapoint_identification(uid=uid)
    return True

@exceptions.ExceptionHandler
def enable_user_event(event):
    if not isinstance(event, ormevents.UserEvent):
        return False
    else:
        row=connection.session.execute(stmtevents.S_A_DATUSEREVENTSDISABLED_B_UID_DATE,(event.uid,event.date))
        if row and row[0]['type']==event.type:
            connection.session.execute(stmtevents.I_A_DATUSEREVENTS,(event.uid,event.date,event.priority,event.type))
            connection.session.execute(stmtevents.D_A_DATUSEREVENTSDISABLED_B_UID_DATE,(event.uid,event.date))
            return True
        return False

@exceptions.ExceptionHandler
def disable_user_event(event):
    if not isinstance(event, ormevents.UserEvent):
        return False
    else:
        row=connection.session.execute(stmtevents.S_A_DATUSEREVENTS_B_UID_DATE,(event.uid,event.date))
        if row and row[0]['type']==event.type:
            connection.session.execute(stmtevents.I_A_DATUSEREVENTSDISABLED,(event.uid,event.date,event.priority,event.type))
            connection.session.execute(stmtevents.D_A_DATUSEREVENTS_B_UID_DATE,(event.uid,event.date))
            return True
        return False

# User Event Responses

def get_user_event_responses(event):
    if not isinstance(event, ormevents.UserEvent):
        return []
    else:
        try:
            return get_user_event_responses_funcs[event.type](event)
        except KeyError:
            return []

@exceptions.ExceptionHandler
def _get_user_event_responses_intervention_datapoint_identification(event):
    responses=[]
    row=connection.session.execute(stmtevents.S_A_DATUERINTERVDPIDENTIFICATION_B_UID_DATE,(event.uid,event.date))
    if row:
        for r in row:
            responses.append(ormevents.UserEventResponseInterventionDatapointIdentification(uid=r['uid'],date=r['date'],response_date=r['response_date'],data=r['data']))
    return responses

@exceptions.ExceptionHandler
def get_user_events_responses_intervention_datapoint_identification(uid):
    responses=[]
    row=connection.session.execute(stmtevents.S_A_DATUERINTERVDPIDENTIFICATION_B_UID,(uid,))
    if row:
        for r in row:
            responses.append(ormevents.UserEventResponseInterventionDatapointIdentification(uid=r['uid'],date=r['date'],response_date=r['response_date'],data=r['data']))
    return responses

def insert_user_event_response(response):
    if not isinstance(response, ormevents.UserEventResponse):
        return False
    else:
        try:
            return insert_user_event_response_funcs[response.type](response)
        except KeyError:
            return False

@exceptions.ExceptionHandler
def _insert_user_event_response_intervention_datapoint_identification(response):
    connection.session.execute(stmtevents.I_A_DATUERINTERVDPIDENTIFICATION, (response.uid,response.date,response.response_date, response.data))
    return True

@exceptions.ExceptionHandler
def delete_user_events_responses_intervention_datapoint_identification(uid):
    connection.session.execute(stmtevents.D_A_DATUERINTERVDPIDENTIFICATION_B_UID,(uid,))
    return True

@exceptions.ExceptionHandler
def get_user_event_data_summary(uid, date):
    row=connection.session.execute(stmtevents.S_A_DATUSEREVENTSDATASUMMARY_B_UID_DATE,(uid,date))
    if row:
        return ormevents.UserEventDataSummary(**row[0])
    else:
        return None

@exceptions.ExceptionHandler
def insert_user_event_data_summary(summary):
    if not isinstance(summary, ormevents.UserEventDataSummary):
        return False
    else:
        try:
            text_summary=json.dumps(summary.summary) if isinstance(summary.summary,dict) else summary.summary
            connection.session.execute(stmtevents.I_A_DATUSEREVENTSDATASUMMARY, (summary.uid,summary.date,text_summary))
            return True
        except TypeError:
            return False

@exceptions.ExceptionHandler
def delete_user_event_data_summary(uid, date):
    connection.session.execute(stmtevents.D_A_DATUSEREVENTSDATASUMMARY_B_UID_DATE,(uid,date))
    return True

def delete_user_event(event):
    if not isinstance(event, ormevents.UserEvent):
        return False
    else:
        try:
            return delete_user_event_funcs[event.type](event.uid, event.date)
        except KeyError:
            return False

@exceptions.ExceptionHandler
def _delete_user_event_notification_new_user(uid, date):
    connection.session.execute(stmtevents.D_A_DATUSEREVENTS_B_UID_DATE,(uid,date))
    connection.session.execute(stmtevents.D_A_DATUENOTIFNEWUSER_B_UID_DATE, (uid, date))
    return True

@exceptions.ExceptionHandler
def _delete_user_event_notification_new_agent(uid, date):
    connection.session.execute(stmtevents.D_A_DATUSEREVENTS_B_UID_DATE,(uid, date))
    connection.session.execute(stmtevents.D_A_DATUENOTIFNEWAGENT_B_UID_DATE, (uid, date))
    return True

@exceptions.ExceptionHandler
def _delete_user_event_notification_new_datasource(uid, date):
    connection.session.execute(stmtevents.D_A_DATUSEREVENTS_B_UID_DATE,(uid, date))
    connection.session.execute(stmtevents.D_A_DATUENOTIFNEWDATASOURCE_B_UID_DATE, (uid, date))
    return True

@exceptions.ExceptionHandler
def _delete_user_event_notification_new_datapoint(uid, date):
    connection.session.execute(stmtevents.D_A_DATUSEREVENTS_B_UID_DATE,(uid, date))
    connection.session.execute(stmtevents.D_A_DATUENOTIFNEWDATAPOINT_B_UID_DATE, (uid, date))
    return True

@exceptions.ExceptionHandler
def _delete_user_event_notification_new_widget(uid, date):
    connection.session.execute(stmtevents.D_A_DATUSEREVENTS_B_UID_DATE,(uid, date))
    connection.session.execute(stmtevents.D_A_DATUENOTIFNEWWIDGET_B_UID_DATE, (uid, date))
    return True

@exceptions.ExceptionHandler
def _delete_user_event_notification_new_dashboard(uid, date):
    connection.session.execute(stmtevents.D_A_DATUSEREVENTS_B_UID_DATE,(uid, date))
    connection.session.execute(stmtevents.D_A_DATUENOTIFNEWDASHBOARD_B_UID_DATE, (uid, date))
    return True

@exceptions.ExceptionHandler
def _delete_user_event_notification_new_circle(uid, date):
    connection.session.execute(stmtevents.D_A_DATUSEREVENTS_B_UID_DATE,(uid, date))
    connection.session.execute(stmtevents.D_A_DATUENOTIFNEWCIRCLE_B_UID_DATE, (uid, date))
    return True

@exceptions.ExceptionHandler
def _delete_user_event_intervention_datapoint_identification(uid, date):
    connection.session.execute(stmtevents.D_A_DATUSEREVENTS_B_UID_DATE,(uid, date))
    connection.session.execute(stmtevents.D_A_DATUEINTERVDPIDENTIFICATION_B_UID_DATE, (uid, date))
    return True

@exceptions.ExceptionHandler
def _delete_user_event_notification_new_snapshot_shared(uid, date):
    connection.session.execute(stmtevents.D_A_DATUSEREVENTS_B_UID_DATE,(uid,date))
    connection.session.execute(stmtevents.D_A_DATUENOTIFNEWSNAPSHOTSHARED_B_UID_DATE, (uid, date))
    return True

@exceptions.ExceptionHandler
def _delete_user_event_notification_new_snapshot_shared_with_me(uid, date):
    connection.session.execute(stmtevents.D_A_DATUSEREVENTS_B_UID_DATE,(uid, date))
    connection.session.execute(stmtevents.D_A_DATUENOTIFNEWSNAPSHOTSHAREDWITHME_B_UID_DATE, (uid, date))
    return True

@exceptions.ExceptionHandler
def _delete_user_event_intervention_datapoint_identification(uid, date):
    connection.session.execute(stmtevents.D_A_DATUSEREVENTS_B_UID_DATE,(uid, date))
    connection.session.execute(stmtevents.D_A_DATUEINTERVDPIDENTIFICATION_B_UID_DATE, (uid, date))
    return True

def delete_user_event_responses(event):
    if not isinstance(event, ormevents.UserEvent):
        return False
    else:
        responses=get_user_event_responses(event)
        for response in responses:
            delete_user_event_response(response)
        return True

def delete_user_event_response(response):
    if not isinstance(response, ormevents.UserEventResponse):
        return False
    else:
        try:
            return delete_user_event_response_funcs[response.type](response.uid, response.date, response.response_date)
        except KeyError:
            return False

@exceptions.ExceptionHandler
def _delete_user_event_response_intervention_datapoint_identification(uid, date, response_date):
    connection.session.execute(stmtevents.D_A_DATUERINTERVDPIDENTIFICATION_B_UID_DATE_RESPDATE,(uid,date,response_date))
    return True

#### Type Funcs associations


get_user_event_funcs = {
    types.USER_EVENT_NOTIFICATION_NEW_USER:_get_user_event_notification_new_user,
    types.USER_EVENT_NOTIFICATION_NEW_AGENT:_get_user_event_notification_new_agent,
    types.USER_EVENT_NOTIFICATION_NEW_DATASOURCE:_get_user_event_notification_new_datasource,
    types.USER_EVENT_NOTIFICATION_NEW_DATAPOINT:_get_user_event_notification_new_datapoint,
    types.USER_EVENT_NOTIFICATION_NEW_WIDGET:_get_user_event_notification_new_widget,
    types.USER_EVENT_NOTIFICATION_NEW_DASHBOARD:_get_user_event_notification_new_dashboard,
    types.USER_EVENT_NOTIFICATION_NEW_CIRCLE:_get_user_event_notification_new_circle,
    types.USER_EVENT_NOTIFICATION_NEW_SNAPSHOT_SHARED:_get_user_event_notification_new_snapshot_shared,
    types.USER_EVENT_NOTIFICATION_NEW_SNAPSHOT_SHARED_WITH_ME:_get_user_event_notification_new_snapshot_shared_with_me,
    types.USER_EVENT_INTERVENTION_DATAPOINT_IDENTIFICATION:_get_user_event_intervention_datapoint_identification,
}

insert_user_event_funcs = {
    types.USER_EVENT_NOTIFICATION_NEW_USER:_insert_user_event_notification_new_user,
    types.USER_EVENT_NOTIFICATION_NEW_AGENT:_insert_user_event_notification_new_agent,
    types.USER_EVENT_NOTIFICATION_NEW_DATASOURCE:_insert_user_event_notification_new_datasource,
    types.USER_EVENT_NOTIFICATION_NEW_DATAPOINT:_insert_user_event_notification_new_datapoint,
    types.USER_EVENT_NOTIFICATION_NEW_WIDGET:_insert_user_event_notification_new_widget,
    types.USER_EVENT_NOTIFICATION_NEW_DASHBOARD:_insert_user_event_notification_new_dashboard,
    types.USER_EVENT_NOTIFICATION_NEW_CIRCLE:_insert_user_event_notification_new_circle,
    types.USER_EVENT_NOTIFICATION_NEW_SNAPSHOT_SHARED:_insert_user_event_notification_new_snapshot_shared,
    types.USER_EVENT_NOTIFICATION_NEW_SNAPSHOT_SHARED_WITH_ME:_insert_user_event_notification_new_snapshot_shared_with_me,
    types.USER_EVENT_INTERVENTION_DATAPOINT_IDENTIFICATION:_insert_user_event_intervention_datapoint_identification,
}

delete_user_event_funcs = {
    types.USER_EVENT_NOTIFICATION_NEW_USER:_delete_user_event_notification_new_user,
    types.USER_EVENT_NOTIFICATION_NEW_AGENT:_delete_user_event_notification_new_agent,
    types.USER_EVENT_NOTIFICATION_NEW_DATASOURCE:_delete_user_event_notification_new_datasource,
    types.USER_EVENT_NOTIFICATION_NEW_DATAPOINT:_delete_user_event_notification_new_datapoint,
    types.USER_EVENT_NOTIFICATION_NEW_WIDGET:_delete_user_event_notification_new_widget,
    types.USER_EVENT_NOTIFICATION_NEW_DASHBOARD:_delete_user_event_notification_new_dashboard,
    types.USER_EVENT_NOTIFICATION_NEW_CIRCLE:_delete_user_event_notification_new_circle,
    types.USER_EVENT_NOTIFICATION_NEW_SNAPSHOT_SHARED:_delete_user_event_notification_new_snapshot_shared,
    types.USER_EVENT_NOTIFICATION_NEW_SNAPSHOT_SHARED_WITH_ME:_delete_user_event_notification_new_snapshot_shared_with_me,
    types.USER_EVENT_INTERVENTION_DATAPOINT_IDENTIFICATION:_delete_user_event_intervention_datapoint_identification,
}

get_user_event_responses_funcs = {
    types.USER_EVENT_INTERVENTION_DATAPOINT_IDENTIFICATION:_get_user_event_responses_intervention_datapoint_identification,
}

insert_user_event_response_funcs = {
    types.USER_EVENT_RESPONSE_INTERVENTION_DATAPOINT_IDENTIFICATION:_insert_user_event_response_intervention_datapoint_identification,
}

delete_user_event_response_funcs = {
    types.USER_EVENT_RESPONSE_INTERVENTION_DATAPOINT_IDENTIFICATION:_delete_user_event_response_intervention_datapoint_identification,
}

