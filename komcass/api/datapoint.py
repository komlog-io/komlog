#coding: utf-8
'''
Created on 01/10/2014

@author: komlog crew
'''

from komcass.model.orm import datapoint as ormdatapoint
from komcass.model.statement import datapoint as stmtdatapoint
from komcass.exception import datapoint as excpdatapoint
from komcass import connection

def get_datapoint(pid):
    row=connection.session.execute(stmtdatapoint.S_A_MSTDATAPOINT_B_PID,(pid,))
    if not row:
        return None
    elif len(row)==1:
        return ormdatapoint.Datapoint(**row[0])
    else:
        raise excpdatapoint.DataConsistencyException(function='get_datapoint',field='pid',value=pid)

def get_datapoints(did):
    row=connection.session.execute(stmtdatapoint.S_A_MSTDATAPOINT_B_DID,(did,))
    datapoints=[]
    if row:
        for d in row:
            datapoints.append(ormdatapoint.Datapoint(**d))
    return datapoints

def get_datapoints_pids(did):
    row=connection.session.execute(stmtdatapoint.S_PID_MSTDATAPOINT_B_DID,(did,))
    pids=[]
    if row:
        for r in row:
            pids.append(r['pid'])
    return pids

def get_number_of_datapoints_by_did(did):
    row=connection.session.execute(stmtdatapoint.S_COUNT_MSTDATAPOINT_B_DID,(did,))
    return row[0]['count'] if row else 0

def get_datapoint_stats(pid):
    row=connection.session.execute(stmtdatapoint.S_A_MSTDATAPOINTSTATS_B_PID,(pid,))
    if not row:
        return None
    elif len(row)==1:
        return ormdatapoint.DatapointStats(**row[0])
    else:
        raise excpdatapoint.DataConsistencyException(function='get_datapoint_stats',field='pid',value=pid)

def get_datapoint_dtree_positives(pid):
    row=connection.session.execute(stmtdatapoint.S_A_DATDATAPOINTDTREEPOSITIVES_B_PID,(pid,))
    data=[]
    if row:
        for r in row:
            data.append(ormdatapoint.DatapointDtreePositives(**r))
    return data

def get_datapoint_dtree_positives_at(pid, date):
    row=connection.session.execute(stmtdatapoint.S_A_DATDATAPOINTDTREEPOSITIVES_B_PID_DATE,(pid,date))
    if not row:
        return None
    if len(row)==1:
        return ormdatapoint.DatapointDtreePositives(**row[0])
    else:
        raise excpdatapoint.DataConsistencyException(function='get_datapoint_dtree_positives_at',field='pid',value=pid)

def get_datapoint_dtree_negatives(pid):
    row=connection.session.execute(stmtdatapoint.S_A_DATDATAPOINTDTREENEGATIVES_B_PID,(pid,))
    data=[]
    if row:
        for r in row:
            data.append(ormdatapoint.DatapointDtreeNegatives(**r))
    return data

def get_datapoint_dtree_negatives_at(pid, date):
    row=connection.session.execute(stmtdatapoint.S_A_DATDATAPOINTDTREENEGATIVES_B_PID_DATE,(pid,date))
    if not row:
        return None
    elif len(row)==1:
        return ormdatapoint.DatapointDtreeNegatives(**row[0])
    else:
        raise excpdatapoint.DataConsistencyException(function='get_datapoint_dtree_negatives_at',field='pid',value=pid)

def get_datapoint_data_at(pid, date):
    row=connection.session.execute(stmtdatapoint.S_A_DATDATAPOINT_B_PID_DATE,(pid,date))
    if not row:
        return None
    elif len(row)==1:
        return ormdatapoint.DatapointData(row[0]['pid'],row[0]['date'],row[0]['value'])
    else:
        raise excpdatapoint.DataConsistencyException(function='get_datapoint_data_at',field='pid',value=pid)

def get_datapoint_data(pid, fromdate, todate, reverse=False, num_regs=100):
    row=connection.session.execute(stmtdatapoint.S_A_DATDATAPOINT_B_PID_INITDATE_ENDDATE_NUMREGS,(pid,fromdate,todate,num_regs))
    data=[]
    if row:
        for d in row:
            data.append(ormdatapoint.DatapointData(d['pid'],d['date'],d['value']))
    return data

def new_datapoint(datapoint):
    if not isinstance(datapoint, ormdatapoint.Datapoint):
        return False
    else:
        existing_datapoint=get_datapoint(datapoint.pid)
        if existing_datapoint:
            return False
        else:
            connection.session.execute(stmtdatapoint.I_A_MSTDATAPOINT,(datapoint.pid, datapoint.did, datapoint.datapointname, datapoint.color, datapoint.creation_date))
            return True

def insert_datapoint(datapoint):
    if not isinstance(datapoint, ormdatapoint.Datapoint):
        return False
    else:
        connection.session.execute(stmtdatapoint.I_A_MSTDATAPOINT,(datapoint.pid, datapoint.did, datapoint.datapointname, datapoint.color, datapoint.creation_date))
        return True

def insert_datapoint_data(pid, date, value):
    connection.session.execute(stmtdatapoint.I_A_DATDATAPOINT,(pid,date,value))
    return True

def set_datapoint_last_received(pid, last_received):
    connection.session.execute(stmtdatapoint.U_LASTRECEIVED_MSTDATAPOINTSTATS,(last_received,pid))
    return True

def set_datapoint_dtree(pid, dtree):
    connection.session.execute(stmtdatapoint.U_DTREE_MSTDATAPOINTSTATS,(dtree,pid))
    return True

def set_datapoint_decimal_separator(pid, decimal_separator):
    if not decimal_separator in (',','.'):
        return None
    else:
        connection.session.execute(stmtdatapoint.U_DECIMALSEPARATOR_MSTDATAPOINTSTATS,(decimal_separator,pid))
        return True

def delete_datapoint(pid):
    connection.session.execute(stmtdatapoint.D_A_MSTDATAPOINT_B_PID,(pid,))
    connection.session.execute(stmtdatapoint.D_A_MSTDATAPOINTSTATS_B_PID,(pid,))
    connection.session.execute(stmtdatapoint.D_A_DATDATAPOINTDTREEPOSITIVES_B_PID,(pid,))
    connection.session.execute(stmtdatapoint.D_A_DATDATAPOINTDTREENEGATIVES_B_PID,(pid,))
    connection.session.execute(stmtdatapoint.D_A_DATDATAPOINT_B_PID,(pid,))
    return True

def set_datapoint_dtree_positive_at(pid, date, position, length):
    connection.session.execute(stmtdatapoint.U_POSITIONLENGTH_DATDATAPOINTDTREEPOSITIVES_B_PID_DATE,(position,length, pid, date))
    return True

def add_datapoint_dtree_negative_at(pid, date, position, length):
    connection.session.execute(stmtdatapoint.U_R_DATDATAPOINTDTREENEGATIVES_B_POS_LEN_PID_DATE,(position, length, pid,date))
    return True

def delete_datapoint_dtree_positive_at(pid, date):
    connection.session.execute(stmtdatapoint.D_A_DATDATAPOINTDTREEPOSITIVES_B_PID_DATE,(pid, date))
    return True

def delete_datapoint_dtree_negatives_at(pid, date):
    connection.session.execute(stmtdatapoint.D_A_DATDATAPOINTDTREENEGATIVES_B_PID_DATE,(pid, date))
    return True

def delete_datapoint_dtree_negative_at(pid, date, position):
    connection.session.execute(stmtdatapoint.D_R_DATDATAPOINTDTREENEGATIVES_B_POS_PID_DATE,(position, pid, date))
    return True

