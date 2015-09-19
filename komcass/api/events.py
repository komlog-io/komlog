'''
@author: komlog crew
'''

from komcass.model.orm import events as ormevents
from komcass.model.parametrization.events import types
from komcass.model.statement import events as stmtevents
from komcass import connection


def get_user_event(uid, date):
    row=connection.session.execute(stmtevents.S_A_DATUSEREVENTS_B_UID_DATE,(uid,date))
    if row:
        return _get_user_event(ormevents.UserEvent(**row[0]))
    else:
        return None

def get_disabled_user_event(uid, date):
    row=connection.session.execute(stmtevents.S_A_DATUSEREVENTSDISABLED_B_UID_DATE,(uid,date))
    if row:
        return _get_user_event(ormevents.UserEvent(**row[0]))
    else:
        return None

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
        if event.type==types.USER_EVENT_NOTIFICATION_NEW_USER:
            event_info=connection.session.execute(stmtevents.S_A_DATUENOTIFNEWUSER_B_UID_DATE,(event.uid, event.date))
            if event_info:
                return ormevents.UserEventNotificationNewUser(uid=event.uid, date=event.date, priority=event.priority, username=event_info[0]['username'])
            else:
                return None
        elif event.type==types.USER_EVENT_NOTIFICATION_NEW_AGENT:
            event_info=connection.session.execute(stmtevents.S_A_DATUENOTIFNEWAGENT_B_UID_DATE,(event.uid, event.date))
            if event_info:
                return ormevents.UserEventNotificationNewAgent(uid=event.uid, date=event.date, priority=event.priority, aid=event_info[0]['aid'], agentname=event_info[0]['agentname'])
            else:
                return None
        elif event.type==types.USER_EVENT_NOTIFICATION_NEW_DATASOURCE:
            event_info=connection.session.execute(stmtevents.S_A_DATUENOTIFNEWDATASOURCE_B_UID_DATE,(event.uid, event.date))
            if event_info:
                return ormevents.UserEventNotificationNewDatasource(uid=event.uid, date=event.date, priority=event.priority, aid=event_info[0]['aid'], did=event_info[0]['did'], datasourcename=event_info[0]['datasourcename'])
            else:
                return None
        elif event.type==types.USER_EVENT_NOTIFICATION_NEW_DATAPOINT:
            event_info=connection.session.execute(stmtevents.S_A_DATUENOTIFNEWDATAPOINT_B_UID_DATE,(event.uid, event.date))
            if event_info:
                return ormevents.UserEventNotificationNewDatapoint(uid=event.uid, date=event.date, priority=event.priority, did=event_info[0]['did'], pid=event_info[0]['pid'], datasourcename=event_info[0]['datasourcename'], datapointname=event_info[0]['datapointname'])
            else:
                return None
        elif event.type==types.USER_EVENT_NOTIFICATION_NEW_WIDGET:
            event_info=connection.session.execute(stmtevents.S_A_DATUENOTIFNEWWIDGET_B_UID_DATE,(event.uid, event.date))
            if event_info:
                return ormevents.UserEventNotificationNewWidget(uid=event.uid, date=event.date, priority=event.priority, wid=event_info[0]['wid'], widgetname=event_info[0]['widgetname'])
            else:
                return None
        elif event.type==types.USER_EVENT_NOTIFICATION_NEW_DASHBOARD:
            event_info=connection.session.execute(stmtevents.S_A_DATUENOTIFNEWDASHBOARD_B_UID_DATE,(event.uid, event.date))
            if event_info:
                return ormevents.UserEventNotificationNewDashboard(uid=event.uid, date=event.date, priority=event.priority, bid=event_info[0]['bid'], dashboardname=event_info[0]['dashboardname'])
            else:
                return None
        elif event.type==types.USER_EVENT_NOTIFICATION_NEW_CIRCLE:
            event_info=connection.session.execute(stmtevents.S_A_DATUENOTIFNEWCIRCLE_B_UID_DATE,(event.uid, event.date))
            if event_info:
                return ormevents.UserEventNotificationNewCircle(uid=event.uid, date=event.date, priority=event.priority, cid=event_info[0]['cid'], circlename=event_info[0]['circlename'])
            else:
                return None
        elif event.type==types.USER_EVENT_INTERVENTION_DATAPOINT_IDENTIFICATION:
            event_info=connection.session.execute(stmtevents.S_A_DATUEINTERVDPIDENTIFICATION_B_UID_DATE,(event.uid, event.date))
            if event_info:
                return ormevents.UserEventInterventionDatapointIdentification(uid=event.uid, date=event.date, priority=event.priority, did=event_info[0]['did'], ds_date=event_info[0]['ds_date'], doubts=event_info[0]['doubts'], discarded=event_info[0]['discarded'])
            else:
                return None
        else:
            return None

def insert_user_event(event):
    if not isinstance(event, ormevents.UserEvent):
        return False
    else:
        if event.type==types.USER_EVENT_NOTIFICATION_NEW_USER:
            return _insert_user_event_notification_new_user(event)
        elif event.type==types.USER_EVENT_NOTIFICATION_NEW_AGENT:
            return _insert_user_event_notification_new_agent(event)
        elif event.type==types.USER_EVENT_NOTIFICATION_NEW_DATASOURCE:
            return _insert_user_event_notification_new_datasource(event)
        elif event.type==types.USER_EVENT_NOTIFICATION_NEW_DATAPOINT:
            return _insert_user_event_notification_new_datapoint(event)
        elif event.type==types.USER_EVENT_NOTIFICATION_NEW_WIDGET:
            return _insert_user_event_notification_new_widget(event)
        elif event.type==types.USER_EVENT_NOTIFICATION_NEW_DASHBOARD:
            return _insert_user_event_notification_new_dashboard(event)
        elif event.type==types.USER_EVENT_NOTIFICATION_NEW_CIRCLE:
            return _insert_user_event_notification_new_circle(event)
        elif event.type==types.USER_EVENT_INTERVENTION_DATAPOINT_IDENTIFICATION:
            return _insert_user_event_intervention_datapoint_identification(event)
        else:
            return False

def _insert_user_event_notification_new_user(event):
    if not isinstance(event, ormevents.UserEventNotificationNewUser):
        return False
    else:
        connection.session.execute(stmtevents.I_A_DATUSEREVENTS,(event.uid,event.date,event.priority,types.USER_EVENT_NOTIFICATION_NEW_USER))
        connection.session.execute(stmtevents.I_A_DATUENOTIFNEWUSER, (event.uid, event.date, event.username))
        return True

def _insert_user_event_notification_new_agent(event):
    if not isinstance(event, ormevents.UserEventNotificationNewAgent):
        return False
    else:
        connection.session.execute(stmtevents.I_A_DATUSEREVENTS,(event.uid,event.date,event.priority,types.USER_EVENT_NOTIFICATION_NEW_AGENT))
        connection.session.execute(stmtevents.I_A_DATUENOTIFNEWAGENT, (event.uid, event.date, event.aid, event.agentname))
        return True

def _insert_user_event_notification_new_datasource(event):
    if not isinstance(event, ormevents.UserEventNotificationNewDatasource):
        return False
    else:
        connection.session.execute(stmtevents.I_A_DATUSEREVENTS,(event.uid,event.date,event.priority,types.USER_EVENT_NOTIFICATION_NEW_DATASOURCE))
        connection.session.execute(stmtevents.I_A_DATUENOTIFNEWDATASOURCE, (event.uid, event.date, event.aid, event.did, event.datasourcename))
        return True

def _insert_user_event_notification_new_datapoint(event):
    if not isinstance(event, ormevents.UserEventNotificationNewDatapoint):
        return False
    else:
        connection.session.execute(stmtevents.I_A_DATUSEREVENTS,(event.uid,event.date,event.priority,types.USER_EVENT_NOTIFICATION_NEW_DATAPOINT))
        connection.session.execute(stmtevents.I_A_DATUENOTIFNEWDATAPOINT, (event.uid, event.date, event.did, event.pid, event.datasourcename, event.datapointname))
        return True

def _insert_user_event_notification_new_widget(event):
    if not isinstance(event, ormevents.UserEventNotificationNewWidget):
        return False
    else:
        connection.session.execute(stmtevents.I_A_DATUSEREVENTS,(event.uid,event.date,event.priority,types.USER_EVENT_NOTIFICATION_NEW_WIDGET))
        connection.session.execute(stmtevents.I_A_DATUENOTIFNEWWIDGET, (event.uid, event.date, event.wid, event.widgetname))
        return True

def _insert_user_event_notification_new_dashboard(event):
    if not isinstance(event, ormevents.UserEventNotificationNewDashboard):
        return False
    else:
        connection.session.execute(stmtevents.I_A_DATUSEREVENTS,(event.uid,event.date,event.priority,types.USER_EVENT_NOTIFICATION_NEW_DASHBOARD))
        connection.session.execute(stmtevents.I_A_DATUENOTIFNEWDASHBOARD, (event.uid, event.date, event.bid, event.dashboardname))
        return True

def _insert_user_event_notification_new_circle(event):
    if not isinstance(event, ormevents.UserEventNotificationNewCircle):
        return False
    else:
        connection.session.execute(stmtevents.I_A_DATUSEREVENTS,(event.uid,event.date,event.priority,types.USER_EVENT_NOTIFICATION_NEW_CIRCLE))
        connection.session.execute(stmtevents.I_A_DATUENOTIFNEWCIRCLE, (event.uid, event.date, event.cid, event.circlename))
        return True

def _insert_user_event_intervention_datapoint_identification(event):
    if not isinstance(event, ormevents.UserEventInterventionDatapointIdentification):
        return False
    else:
        connection.session.execute(stmtevents.I_A_DATUSEREVENTS,(event.uid,event.date,event.priority,types.USER_EVENT_INTERVENTION_DATAPOINT_IDENTIFICATION))
        connection.session.execute(stmtevents.I_A_DATUEINTERVDPIDENTIFICATION, (event.uid, event.date, event.did, event.ds_date, event.doubts, event.discarded))
        return True

def delete_user_events(uid):
    connection.session.execute(stmtevents.D_A_DATUSEREVENTS_B_UID,(uid,))
    connection.session.execute(stmtevents.D_A_DATUSEREVENTSDISABLED_B_UID,(uid,))
    connection.session.execute(stmtevents.D_A_DATUENOTIFNEWUSER_B_UID,(uid,))
    connection.session.execute(stmtevents.D_A_DATUENOTIFNEWAGENT_B_UID,(uid,))
    connection.session.execute(stmtevents.D_A_DATUENOTIFNEWDATASOURCE_B_UID,(uid,))
    connection.session.execute(stmtevents.D_A_DATUENOTIFNEWDATAPOINT_B_UID,(uid,))
    connection.session.execute(stmtevents.D_A_DATUENOTIFNEWWIDGET_B_UID,(uid,))
    connection.session.execute(stmtevents.D_A_DATUENOTIFNEWDASHBOARD_B_UID,(uid,))
    connection.session.execute(stmtevents.D_A_DATUENOTIFNEWCIRCLE_B_UID,(uid,))
    connection.session.execute(stmtevents.D_A_DATUEINTERVDPIDENTIFICATION_B_UID,(uid,))
    delete_user_events_responses_intervention_datapoint_identification(uid=uid)
    return True

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
        if event.type==types.USER_EVENT_INTERVENTION_DATAPOINT_IDENTIFICATION:
            return _get_user_event_responses_intervention_datapoint_identification(uid=event.uid, date=event.date)
        else:
            return []

def _get_user_event_responses_intervention_datapoint_identification(uid, date):
    responses=[]
    row=connection.session.execute(stmtevents.S_A_DATUERINTERVDPIDENTIFICATION_B_UID_DATE,(uid,date))
    if row:
        for r in row:
            responses.append(ormevents.UserEventResponseInterventionDatapointIdentification(uid=r['uid'],date=r['date'],response_date=r['response_date'],missing=r['missing'],identified=r['identified'],not_belonging=r['not_belonging'],to_update=r['to_update'],update_failed=r['update_failed'],update_success=r['update_success']))
    return responses

def get_user_events_responses_intervention_datapoint_identification(uid):
    responses=[]
    row=connection.session.execute(stmtevents.S_A_DATUERINTERVDPIDENTIFICATION_B_UID,(uid,))
    if row:
        for r in row:
            responses.append(ormevents.UserEventResponseInterventionDatapointIdentification(uid=r['uid'],date=r['date'],response_date=r['response_date'],missing=r['missing'],identified=r['identified'],not_belonging=r['not_belonging'],to_update=r['to_update'],update_failed=r['update_failed'],update_success=r['update_success']))
    return responses

def insert_user_event_response(response):
    if not isinstance(response, ormevents.UserEventResponse):
        return False
    else:
        if response.type==types.USER_EVENT_RESPONSE_INTERVENTION_DATAPOINT_IDENTIFICATION:
            return _insert_user_event_response_intervention_datapoint_identification(response)
        else:
            return False

def _insert_user_event_response_intervention_datapoint_identification(response):
    if not isinstance(response, ormevents.UserEventResponseInterventionDatapointIdentification):
        return False
    else:
        connection.session.execute(stmtevents.I_A_DATUERINTERVDPIDENTIFICATION, (response.uid,response.date,response.response_date, response.missing, response.identified, response.not_belonging, response.to_update, response.update_failed, response.update_success))
        return True

def delete_user_events_responses_intervention_datapoint_identification(uid):
    responses=get_user_events_responses_intervention_datapoint_identification(uid=uid)
    for resp in responses:
        connection.session.execute(stmtevents.D_A_DATUERINTERVDPIDENTIFICATION_B_UID_DATE,(resp.uid,resp.date))
    return True

