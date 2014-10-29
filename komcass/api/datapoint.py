#coding: utf-8
'''
Created on 01/10/2014

@author: komlog crew
'''

from komcass.model.orm import datapoint as ormdatapoint
from komcass.model.statement import datapoint as stmtdatapoint
from komcass.exception import datapoint as excpdatapoint

def get_datapoint(session, pid):
    row=session.execute(stmtdatapoint.S_A_MSTDATAPOINT_B_PID,(pid,))
    if not row:
        return None
    elif len(row)==1:
        return ormdatapoint.Datapoint(**row[0])
    else:
        raise excpdatapoint.DataConsistencyException(function='get_datapoint',field='pid',value=pid)

def get_datapoints(session, did):
    row=session.execute(stmtdatapoint.S_A_MSTDATAPOINT_B_DID,(did,))
    datapoints=[]
    if row:
        for d in row:
            datapoints.append(ormdatapoint.Datapoint(**d))
    return datapoints

def get_datapoints_pids(session, did):
    row=session.execute(stmtdatapoint.S_PID_MSTDATAPOINT_B_DID,(did,))
    pids=[]
    if row:
        for r in row:
            pids.append(r['pid'])
    return pids

def get_number_of_datapoints_by_did(session, did):
    row=session.execute(stmtdatapoint.S_COUNT_MSTDATAPOINT_B_DID,(did,))
    return row[0]['count']

def get_datapoint_stats(session, pid):
    row=session.execute(stmtdatapoint.S_A_MSTDATAPOINTSTATS_B_PID,(pid,))
    if not row:
        return None
    elif len(row)==1:
        return ormdatapoint.DatapointStats(**row[0])
    else:
        raise excpdatapoint.DataConsistencyException(function='get_datapoint_stats',field='pid',value=pid)

def get_datapoint_dtree_positives(session, pid):
    row=session.execute(stmtdatapoint.S_A_DATDATAPOINTDTREEPOSITIVES_B_PID,(pid,))
    data=[]
    if row:
        for r in row:
            data.append(ormdatapoint.DatapointDtreePositives(**r))
    return data

def get_datapoint_dtree_positives_at(session, pid, date):
    row=session.execute(stmtdatapoint.S_A_DATDATAPOINTDTREEPOSITIVES_B_PID_DATE,(pid,date))
    if not row:
        return None
    if len(row)==1:
        return ormdatapoint.DatapointDtreePositives(**row[0])
    else:
        raise excpdatapoint.DataConsistencyException(function='get_datapoint_dtree_positives_at',field='pid',value=pid)

def get_datapoint_dtree_negatives(session, pid):
    row=session.execute(stmtdatapoint.S_A_DATDATAPOINTDTREENEGATIVES_B_PID,(pid,))
    data=[]
    if row:
        for r in row:
            data.append(ormdatapoint.DatapointDtreeNegatives(**r))
    return data

def get_datapoint_dtree_negatives_at(session, pid, date):
    row=session.execute(stmtdatapoint.S_A_DATDATAPOINTDTREENEGATIVES_B_PID_DATE,(pid,date))
    if not row:
        return None
    elif len(row)==1:
        return ormdatapoint.DatapointDtreeNegatives(**row[0])
    else:
        raise excpdatapoint.DataConsistencyException(function='get_datapoint_dtree_negatives_at',field='pid',value=pid)

def get_datapoint_data_at(session, pid, date=None):
    if date:
        row=session.execute(stmtdatapoint.S_A_DATDATAPOINT_B_PID_DATE,(pid,date))
        if not row:
            return None
        elif len(row)==1:
            return ormdatapoint.DatapointData(row[0]['pid'],row[0]['date'],row[0]['value'])
        else:
            raise excpdatapoint.DataConsistencyException(function='get_datapoint_data_at',field='pid',value=pid)
    else:
        return None

def get_datapoint_data(session, pid, fromdate, todate, reverse=False, num_regs=100):
    row=session.execute(stmtdatapoint.S_A_DATDATAPOINT_B_PID_INITDATE_ENDDATE_NUMREGS,(pid,fromdate,todate,num_regs))
    data=[]
    if row:
        for d in row:
            data.append(ormdatapoint.DatapointData(d['pid'],d['date'],d['value']))
    return data

def new_datapoint(session, datapoint):
    if not datapoint:
        return False
    else:
        existing_datapoint=get_datapoint(session, datapoint.pid)
        if existing_datapoint:
            return False
        else:
            session.execute(stmtdatapoint.I_A_MSTDATAPOINT,(datapoint.pid, datapoint.did, datapoint.datapointname, datapoint.color, datapoint.creation_date))
            return True

def insert_datapoint(session, datapoint):
    if not datapoint:
        return False
    session.execute(stmtdatapoint.I_A_MSTDATAPOINT,(datapoint.pid, datapoint.did, datapoint.datapointname, datapoint.color, datapoint.creation_date))
    return True

def insert_datapoint_data(session, pid, date, value):
    session.execute(stmtdatapoint.I_A_DATDATAPOINT,(pid,date,value))
    return True

def set_datapoint_last_received(session, pid, last_received):
    session.execute(stmtdatapoint.U_LASTRECEIVED_MSTDATAPOINTSTATS,(last_received,pid))
    return True

def set_datapoint_dtree(session, pid, dtree):
    session.execute(stmtdatapoint.U_DTREE_MSTDATAPOINTSTATS,(dtree,pid))
    return True

def set_datapoint_decimal_separator(session, pid, decimal_separator):
    if not decimal_separator in (',','.'):
        return None
    else:
        session.execute(stmtdatapoint.U_DECIMALSEPARATOR_MSTDATAPOINTSTATS,(decimal_separator,pid))
        return True

def delete_datapoint(session, pid):
    session.execute(stmtdatapoint.D_A_MSTDATAPOINT_B_PID,(pid,))
    session.execute(stmtdatapoint.D_A_MSTDATAPOINTSTATS_B_PID,(pid,))
    session.execute(stmtdatapoint.D_A_DATDATAPOINTDTREEPOSITIVES_B_PID,(pid,))
    session.execute(stmtdatapoint.D_A_DATDATAPOINTDTREENEGATIVES_B_PID,(pid,))
    session.execute(stmtdatapoint.D_A_DATDATAPOINT_B_PID,(pid,))
    return True

def set_datapoint_dtree_positive_at(session, pid, date, position, length):
    session.execute(stmtdatapoint.U_POSITIONLENGTH_DATDATAPOINTDTREEPOSITIVES_B_PID_DATE,(position,length, pid, date))
    return True

def add_datapoint_dtree_negative_at(session, pid, date, position, length):
    session.execute(stmtdatapoint.U_R_DATDATAPOINTDTREENEGATIVES_B_POS_LEN_PID_DATE,(position, length, pid,date))
    return True

def delete_datapoint_dtree_positive_at(session, pid, date):
    session.execute(stmtdatapoint.D_A_DATDATAPOINTDTREEPOSITIVES_B_PID_DATE,(pid, date))
    return True

def delete_datapoint_dtree_negatives_at(session, pid, date):
    session.execute(stmtdatapoint.D_A_DATDATAPOINTDTREENEGATIVES_B_PID_DATE,(pid, date))
    return True

def delete_datapoint_dtree_negative_at(session, pid, date, position):
    session.execute(stmtdatapoint.D_R_DATDATAPOINTDTREENEGATIVES_B_POS_PID_DATE,(position, pid, date))
    return True

