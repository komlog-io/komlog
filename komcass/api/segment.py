#coding: utf-8
'''
Created on 01/10/2014

@author: komlog crew
'''

from komcass.model.orm import segment as ormsegment
from komcass.model.statement import segment as stmtsegment
from komcass.exception import segment as excpsegment


def get_user_segment(session, sid):
    row=session.execute(stmtsegment.S_A_PRMUSERSEGMENT_B_SID,(sid,))
    if not row:
        return None
    if len(row)==1:
        return ormsegment.UserSegment(**row[0])
    else:
        raise excpsegment.DataConsistencyException(function='get_segment_info',field='id',value=segment_id)

def insert_user_segment(session, sobj):
    session.execute(stmtsegment.I_A_PRMUSERSEGMENT,(sobj.sid,sobj.segmentname,sobj.params))
    return True

def set_user_segment_params(session, sid, params):
    session.execute(stmtsegment.I_PARAMS_PRMUSERSEGMENT_B_PARAMS_SID,(sid,params))
    return True

def set_user_segment_param(session, sid, param, value):
    session.execute(stmtsegment.U_PARAM_PRMUSERSEGMENT_B_PARAM_SID,(param,value,sid))
    return True

def delete_user_segment_param(session, sid, param):
    session.execute(stmtsegment.D_PARAM_PRMUSERSEGMENT_B_PARAM_SID,(param,sid))
    return True

def delete_user_segment_params(session, sid):
    session.execute(stmtsegment.D_A_PRMUSERSEGMENT_B_SID,(sid,))
    return True

