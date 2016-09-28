'''
Created on 01/10/2014

@author: komlog crew
'''

from komlog.komcass.model.orm import segment as ormsegment
from komlog.komcass.model.statement import segment as stmtsegment
from komlog.komcass import connection, exceptions
from komlog.komlibs.general.time import timeuuid


@exceptions.ExceptionHandler
def get_user_segment(sid):
    row=connection.session.execute(stmtsegment.S_A_MSTUSERSEGMENT_B_SID,(sid,))
    if row:
        return ormsegment.UserSegment(**row[0])
    else:
        return None

@exceptions.ExceptionHandler
def insert_user_segment(segment):
    if not isinstance(segment, ormsegment.UserSegment):
        return False
    connection.session.execute(stmtsegment.I_A_MSTUSERSEGMENT,(segment.sid,segment.description))
    return True

@exceptions.ExceptionHandler
def delete_user_segment(sid):
    connection.session.execute(stmtsegment.D_A_MSTUSERSEGMENT_B_SID,(sid,))
    return True

@exceptions.ExceptionHandler
def get_user_segment_quotes(sid):
    quotes=[]
    rows=connection.session.execute(stmtsegment.S_A_PRMUSERSEGMENTQUO_B_SID,(sid,))
    if rows:
        for r in rows:
            quotes.append(ormsegment.UserSegmentQuo(**r))
    return quotes

@exceptions.ExceptionHandler
def get_user_segment_quote(sid, quote):
    row=connection.session.execute(stmtsegment.S_A_PRMUSERSEGMENTQUO_B_SID_QUOTE,(sid,quote))
    if row:
        return ormsegment.UserSegmentQuo(**row[0])
    else:
        return None

@exceptions.ExceptionHandler
def insert_user_segment_quote(sid, quote, value):
    connection.session.execute(stmtsegment.I_A_PRMUSERSEGMENTQUO,(sid,quote,value))
    return True

@exceptions.ExceptionHandler
def delete_user_segment_quotes(sid):
    connection.session.execute(stmtsegment.D_A_PRMUSERSEGMENTQUO_B_SID,(sid,))
    return True

@exceptions.ExceptionHandler
def delete_user_segment_quote(sid, quote):
    connection.session.execute(stmtsegment.D_QUOTE_PRMUSERSEGMENTQUO_B_SID_QUOTE,(sid,quote))
    return True

@exceptions.ExceptionHandler
def get_user_segment_transition(uid,date):
    row=connection.session.execute(stmtsegment.S_A_DATUSERSEGMENTTRANSITION_B_UID_DATE,(uid,date))
    if row:
        return ormsegment.UserSegmentTransition(**row[0])
    else:
        return None

@exceptions.ExceptionHandler
def get_user_segment_transitions(uid, init_date=None, end_date=None):
    data=[]
    if init_date == None and end_date == None:
        rows=connection.session.execute(stmtsegment.S_DATESIDPSID_DATUSERSEGMENTTRANSITION_B_UID,(uid,))
    elif init_date and end_date:
        rows=connection.session.execute(stmtsegment.S_DATESIDPSID_DATUSERSEGMENTTRANSITION_B_UID_INITDATE_ENDDATE,(uid,init_date, end_date))
    elif end_date:
        init_date = timeuuid.LOWEST_TIME_UUID
        rows=connection.session.execute(stmtsegment.S_DATESIDPSID_DATUSERSEGMENTTRANSITION_B_UID_INITDATE_ENDDATE,(uid,init_date, end_date))
    else:
        end_date = timeuuid.HIGHEST_TIME_UUID
        rows=connection.session.execute(stmtsegment.S_DATESIDPSID_DATUSERSEGMENTTRANSITION_B_UID_INITDATE_ENDDATE,(uid,init_date, end_date))
    for r in rows:
        data.append(r)
    return data

@exceptions.ExceptionHandler
def insert_user_segment_transition(uid, date, sid, previous_sid):
    connection.session.execute(stmtsegment.I_A_DATUSERSEGMENTTRANSITION,(uid,date,sid,previous_sid))
    return True

@exceptions.ExceptionHandler
def delete_user_segment_transition(uid, date):
    connection.session.execute(stmtsegment.D_A_DATUSERSEGMENTTRANSITION_B_UID_DATE,(uid,date))
    return True

@exceptions.ExceptionHandler
def delete_user_segment_transitions(uid, init_date=None, end_date=None):
    if init_date == None and end_date == None:
        connection.session.execute(stmtsegment.D_A_DATUSERSEGMENTTRANSITION_B_UID,(uid,))
    elif init_date and end_date:
        connection.session.execute(stmtsegment.D_A_DATUSERSEGMENTTRANSITION_B_UID_INITDATE_ENDDATE,(uid,init_date, end_date))
    elif end_date:
        init_date = timeuuid.LOWEST_TIME_UUID
        connection.session.execute(stmtsegment.D_A_DATUSERSEGMENTTRANSITION_B_UID_INITDATE_ENDDATE,(uid,init_date, end_date))
    else:
        end_date = timeuuid.HIGHEST_TIME_UUID
        connection.session.execute(stmtsegment.D_A_DATUSERSEGMENTTRANSITION_B_UID_INITDATE_ENDDATE,(uid,init_date, end_date))
    return True

@exceptions.ExceptionHandler
def get_user_segment_allowed_transitions(sid):
    row=connection.session.execute(stmtsegment.S_A_PRMUSERSEGMENTALLOWEDTRANSITIONS_B_SID,(sid,))
    if row:
        return ormsegment.UserSegmentAllowedTransition(**row[0])
    else:
        return None

@exceptions.ExceptionHandler
def insert_user_segment_allowed_transitions(sid, sids):
    connection.session.execute(stmtsegment.I_A_PRMUSERSEGMENTALLOWEDTRANSITIONS,(sid,sids))
    return True

@exceptions.ExceptionHandler
def delete_user_segment_allowed_transitions(sid):
    connection.session.execute(stmtsegment.D_A_PRMUSERSEGMENTALLOWEDTRANSITIONS_B_SID,(sid,))
    return True

@exceptions.ExceptionHandler
def get_user_segment_fare(sid):
    row=connection.session.execute(stmtsegment.S_A_PRMUSERSEGMENTFARE_B_SID,(sid,))
    if row:
        return ormsegment.UserSegmentFare(**row[0])
    else:
        return None

@exceptions.ExceptionHandler
def insert_user_segment_fare(sid, amount, currency, frequency):
    connection.session.execute(stmtsegment.I_A_PRMUSERSEGMENTFARE,(sid, amount, currency,frequency))
    return True

@exceptions.ExceptionHandler
def delete_user_segment_fare(sid):
    connection.session.execute(stmtsegment.D_A_PRMUSERSEGMENTFARE_B_SID,(sid,))
    return True

