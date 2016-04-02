#coding: utf-8
'''
Created on 01/10/2014

@author: komlog crew
'''

from komlog.komcass.model.orm import segment as ormsegment
from komlog.komcass.model.statement import segment as stmtsegment
from komlog.komcass.exception import segment as excpsegment
from komlog.komcass import connection


def get_user_segment(sid):
    row=connection.session.execute(stmtsegment.S_A_PRMUSERSEGMENT_B_SID,(sid,))
    if not row:
        return None
    else:
        return ormsegment.UserSegment(**row[0])

def insert_user_segment(sobj):
    if not isinstance(sobj, ormsegment.UserSegment):
        return False
    else:
        connection.session.execute(stmtsegment.I_A_PRMUSERSEGMENT,(sobj.sid,sobj.segmentname,sobj.params))
        return True

def set_user_segment_params(sid, params):
    connection.session.execute(stmtsegment.I_PARAMS_PRMUSERSEGMENT_B_PARAMS_SID,(sid,params))
    return True

def set_user_segment_param(sid, param, value):
    connection.session.execute(stmtsegment.U_PARAM_PRMUSERSEGMENT_B_PARAM_SID,(param,value,sid))
    return True

def delete_user_segment_param(sid, param):
    connection.session.execute(stmtsegment.D_PARAM_PRMUSERSEGMENT_B_PARAM_SID,(param,sid))
    return True

def delete_user_segment(sid):
    connection.session.execute(stmtsegment.D_A_PRMUSERSEGMENT_B_SID,(sid,))
    return True

