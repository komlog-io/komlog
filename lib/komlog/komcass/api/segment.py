#coding: utf-8
'''
Created on 01/10/2014

@author: komlog crew
'''

from komlog.komcass.model.orm import segment as ormsegment
from komlog.komcass.model.statement import segment as stmtsegment
from komlog.komcass import connection, exceptions


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

