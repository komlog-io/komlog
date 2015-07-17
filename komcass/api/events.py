'''
@author: komlog crew
'''

from komcass.model.orm import events as ormevents
from komcass.model.statement import events as stmtevents
from komcass import connection


def get_user_event(uid, date):
    row=connection.session.execute(stmtevents.S_A_DATUSEREVENTS_B_UID_DATE,(uid,date))
    if row:
        return ormevents.UserEvent(**row[0])
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
            events.append(ormevents.UserEvent(**r))
    return events

def insert_user_event(event):
    if not isinstance(event, ormevents.UserEvent):
        return False
    else:
        connection.session.execute(stmtevents.I_A_DATUSEREVENTS,(event.uid,event.date,event.active,event.priority,event.type,event.parameters))
        return True

def delete_user_events(uid):
    connection.session.execute(stmtevents.D_A_DATUSEREVENTS_B_UID,(uid,))
    return True

def activate_user_event(uid, date):
    connection.session.execute(stmtevents.U_ACTIVE_DATUSEREVENTS_B_UID_DATE,(True,uid,date))
    return True

def deactivate_user_event(uid, date):
    connection.session.execute(stmtevents.U_ACTIVE_DATUSEREVENTS_B_UID_DATE,(False,uid,date))
    return True

