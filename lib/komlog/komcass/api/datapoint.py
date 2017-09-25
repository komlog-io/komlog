'''
Created on 01/10/2014

@author: komlog crew
'''

from komlog.komcass.model.orm import datapoint as ormdatapoint
from komlog.komcass.model.statement import datapoint as stmtdatapoint
from komlog.komcass import connection, exceptions

@exceptions.ExceptionHandler
def get_datapoint(pid):
    row=connection.session.execute(stmtdatapoint.S_A_MSTDATAPOINT_B_PID,(pid,))
    if not row:
        return None
    else:
        return ormdatapoint.Datapoint(**row[0])

@exceptions.ExceptionHandler
def get_datapoints(did=None, uid=None):
    datapoints=[]
    if did:
        row = connection.session.execute(stmtdatapoint.S_A_MSTDATAPOINT_B_DID,(did,))
    elif uid:
        row = connection.session.execute(stmtdatapoint.S_A_MSTDATAPOINT_B_UID,(uid,))
    else:
        row = None
    if row:
        for d in row:
            datapoints.append(ormdatapoint.Datapoint(**d))
    return datapoints

@exceptions.ExceptionHandler
def get_datapoints_pids(did=None, uid=None):
    pids=[]
    if did:
        row = connection.session.execute(stmtdatapoint.S_PID_MSTDATAPOINT_B_DID,(did,))
    elif uid:
        row = connection.session.execute(stmtdatapoint.S_PID_MSTDATAPOINT_B_UID,(uid,))
    else:
        row = None
    if row:
        for r in row:
            pids.append(r['pid'])
    return pids

@exceptions.ExceptionHandler
def get_number_of_datapoints_by_did(did):
    row=connection.session.execute(stmtdatapoint.S_COUNT_MSTDATAPOINT_B_DID,(did,))
    return row[0]['count'] if row else 0

@exceptions.ExceptionHandler
def get_number_of_datapoints_by_uid(uid):
    row=connection.session.execute(stmtdatapoint.S_COUNT_MSTDATAPOINT_B_UID,(uid,))
    return row[0]['count'] if row else 0

@exceptions.ExceptionHandler
def get_datapoint_stats(pid):
    row=connection.session.execute(stmtdatapoint.S_A_MSTDATAPOINTSTATS_B_PID,(pid,))
    if not row:
        return None
    else:
        return ormdatapoint.DatapointStats(**row[0])

@exceptions.ExceptionHandler
def get_datapoint_dtree_positives(pid):
    row=connection.session.execute(stmtdatapoint.S_A_DATDATAPOINTDTREEPOSITIVES_B_PID,(pid,))
    data=[]
    if row:
        for r in row:
            data.append(ormdatapoint.DatapointDtreePositives(**r))
    return data

@exceptions.ExceptionHandler
def get_datapoint_dtree_positive(pid, date):
    row=connection.session.execute(stmtdatapoint.S_A_DATDATAPOINTDTREEPOSITIVES_B_PID_DATE,(pid,date))
    if not row:
        return None
    else:
        return ormdatapoint.DatapointDtreePositives(**row[0])

@exceptions.ExceptionHandler
def get_datapoint_dtree_negatives(pid, date=None):
    if date != None:
        row=connection.session.execute(stmtdatapoint.S_A_DATDATAPOINTDTREENEGATIVES_B_PID_DATE,(pid,date))
    else:
        row=connection.session.execute(stmtdatapoint.S_A_DATDATAPOINTDTREENEGATIVES_B_PID,(pid,))
    data=[]
    if row:
        for r in row:
            data.append(ormdatapoint.DatapointDtreeNegatives(**r))
    return data

@exceptions.ExceptionHandler
def get_datapoint_dtree_negative(pid, date, position):
    row=connection.session.execute(stmtdatapoint.S_A_DATDATAPOINTDTREENEGATIVES_B_PID_DATE,(pid,date))
    if not row:
        return None
    else:
        return ormdatapoint.DatapointDtreeNegatives(**row[0])

@exceptions.ExceptionHandler
def get_datapoint_data_at(pid, date):
    row=connection.session.execute(stmtdatapoint.S_A_DATDATAPOINT_B_PID_DATE,(pid,date))
    if not row:
        return None
    else:
        return ormdatapoint.DatapointData(row[0]['pid'],row[0]['date'],row[0]['value'])

@exceptions.ExceptionHandler
def get_datapoint_data(pid, fromdate, todate, count=None):
    if count is None:
        row=connection.session.execute(stmtdatapoint.S_DATEVALUE_DATDATAPOINT_B_PID_INITDATE_ENDDATE,(pid,fromdate,todate))
    else:
        row=connection.session.execute(stmtdatapoint.S_DATEVALUE_DATDATAPOINT_B_PID_INITDATE_ENDDATE_COUNT,(pid,fromdate,todate,count))
    data=[]
    if row:
        for d in row:
            data.append(d)
    return data

@exceptions.ExceptionHandler
def new_datapoint(datapoint):
    if not isinstance(datapoint, ormdatapoint.Datapoint):
        return False
    else:
        resp=connection.session.execute(stmtdatapoint.I_A_MSTDATAPOINT_INE,(datapoint.pid, datapoint.did, datapoint.uid, datapoint.datapointname, datapoint.color, datapoint.creation_date))
        return resp[0]['[applied]'] if resp else False

@exceptions.ExceptionHandler
def insert_datapoint(datapoint):
    if not isinstance(datapoint, ormdatapoint.Datapoint):
        return False
    else:
        connection.session.execute(stmtdatapoint.I_A_MSTDATAPOINT,(datapoint.pid, datapoint.did, datapoint.uid, datapoint.datapointname, datapoint.color, datapoint.creation_date))
        return True

@exceptions.ExceptionHandler
def delete_datapoint(pid):
    connection.session.execute(stmtdatapoint.D_A_MSTDATAPOINT_B_PID,(pid,))
    return True

@exceptions.ExceptionHandler
def insert_datapoint_data(pid, date, value):
    connection.session.execute(stmtdatapoint.I_A_DATDATAPOINT,(pid,date,value))
    return True

@exceptions.ExceptionHandler
def delete_datapoint_data_at(pid, date):
    connection.session.execute(stmtdatapoint.D_A_DATDATAPOINT_B_PID_DATE,(pid,date))
    return True

@exceptions.ExceptionHandler
def delete_datapoint_data(pid):
    connection.session.execute(stmtdatapoint.D_A_DATDATAPOINT_B_PID,(pid,))
    return True

@exceptions.ExceptionHandler
def set_datapoint_last_received(pid, last_received):
    connection.session.execute(stmtdatapoint.U_LASTRECEIVED_MSTDATAPOINTSTATS,(last_received,pid))
    return True

@exceptions.ExceptionHandler
def set_datapoint_decimal_separator(pid, decimal_separator):
    if not decimal_separator in (',','.'):
        return None
    else:
        connection.session.execute(stmtdatapoint.U_DECIMALSEPARATOR_MSTDATAPOINTSTATS,(decimal_separator,pid))
        return True

@exceptions.ExceptionHandler
def set_datapoint_dtree_positive_at(pid, date, position, length):
    connection.session.execute(stmtdatapoint.U_POSITIONLENGTH_DATDATAPOINTDTREEPOSITIVES_B_PID_DATE,(position,length, pid, date))
    return True

@exceptions.ExceptionHandler
def update_datapoint_dtree_positive(pid, date, position, length):
    ''' This function sets the specified row in database. It will return True only if the row 
        is created or updated. In case the row already existed with the same values, the row will
        not be updated and the function will return False.
    '''
    result = connection.session.execute(stmtdatapoint.I_A_DATDATAPOINTDTREEPOSITIVES_INE, (pid, date, position, length))
    if result:
        if result[0]['[applied]'] is False:
            value = False
            result = connection.session.execute(stmtdatapoint.U_POSITION_DATDATAPOINTDTREEPOSITIVES_B_PID_DATE_POSITION_INEQ, (position, pid, date, position))
            if result:
                value = result[0]['[applied]']
            result = connection.session.execute(stmtdatapoint.U_LENGTH_DATDATAPOINTDTREEPOSITIVES_B_PID_DATE_LENGTH_INEQ, (length, pid, date, length))
            if value == False and result:
                value = result[0]['[applied]']
            return value
        else:
            return True
    return False

@exceptions.ExceptionHandler
def add_datapoint_dtree_negative_at(pid, date, position, length):
    connection.session.execute(stmtdatapoint.U_LENGTH_DATDATAPOINTDTREENEGATIVES_B_PID_DATE_POSITION,(length, pid, date, position))
    return True

@exceptions.ExceptionHandler
def update_datapoint_dtree_negative(pid, date, position, length):
    ''' This function sets the specified row in database. It will return True only if the row 
        is created or updated. In case the row already existed with the same values, the row will
        not be updated and the function will return False.
    '''
    result = connection.session.execute(stmtdatapoint.I_A_DATDATAPOINTDTREENEGATIVES_INE, (pid, date, position, length))
    if result:
        if result[0]['[applied]'] is False:
            result = connection.session.execute(stmtdatapoint.U_LENGTH_DATDATAPOINTDTREENEGATIVES_B_PID_DATE_POSITION_LENGTH_INEQ, (length, pid, date, position, length))
            if result:
                return result[0]['[applied]']
        else:
            return True
    return False

@exceptions.ExceptionHandler
def delete_datapoint_dtree_positive(pid, date, position=None):
    ''' if position is None, the delete statement is executed if row exists and the function
        returns True or False whether it was executed or not.
        if position is not None, the delete statement is executed only if the row exists and
        position is the value passed. The function returns if the statement was executed or not.
    '''
    if position != None:
        result = connection.session.execute(stmtdatapoint.D_A_DATDATAPOINTDTREEPOSITIVES_B_PID_DATE_POSITION,(pid, date, position))
        return result[0]['[applied]'] if result else False
    else:
        result = connection.session.execute(stmtdatapoint.D_A_DATDATAPOINTDTREEPOSITIVES_B_PID_DATE_IE,(pid, date))
        return result[0]['[applied]'] if result else False

@exceptions.ExceptionHandler
def delete_datapoint_dtree_positives(pid):
    connection.session.execute(stmtdatapoint.D_A_DATDATAPOINTDTREEPOSITIVES_B_PID,(pid,))
    return True

@exceptions.ExceptionHandler
def delete_datapoint_dtree_negative(pid, date, position):
    ''' the delete statement is executed only if row exists. The function returns whether the
        delete statement was executed or not.
    '''
    result = connection.session.execute(stmtdatapoint.D_A_DATDATAPOINTDTREENEGATIVES_B_PID_DATE_POSITION_IE,(pid, date, position))
    return result[0]['[applied]'] if result else False

@exceptions.ExceptionHandler
def delete_datapoint_dtree_negatives(pid, date=None):
    if date != None:
        connection.session.execute(stmtdatapoint.D_A_DATDATAPOINTDTREENEGATIVES_B_PID_DATE,(pid, date))
    else:
        connection.session.execute(stmtdatapoint.D_A_DATDATAPOINTDTREENEGATIVES_B_PID,(pid,))
    return True

@exceptions.ExceptionHandler
def delete_datapoint_stats(pid):
    connection.session.execute(stmtdatapoint.D_A_MSTDATAPOINTSTATS_B_PID,(pid,))
    return True

@exceptions.ExceptionHandler
def dissociate_datapoint_from_datasource(pid):
    connection.session.execute(stmtdatapoint.U_DID_MSTDATAPOINT,(None,pid,))
    return True

@exceptions.ExceptionHandler
def get_datapoint_hooks_sids(pid):
    sids=[]
    row=connection.session.execute(stmtdatapoint.S_SID_MSTDATAPOINTHOOKS_B_PID,(pid,))
    if row:
        for r in row:
            sids.append(r['sid'])
    return sids

@exceptions.ExceptionHandler
def insert_datapoint_hook(pid,sid):
    connection.session.execute(stmtdatapoint.I_A_MSTDATAPOINTHOOKS,(pid,sid))
    return True

@exceptions.ExceptionHandler
def delete_datapoint_hooks(pid):
    connection.session.execute(stmtdatapoint.D_A_MSTDATAPOINTHOOKS_B_PID,(pid,))
    return True

@exceptions.ExceptionHandler
def delete_datapoint_hook(pid,sid):
    connection.session.execute(stmtdatapoint.D_A_MSTDATAPOINTHOOKS_B_PID_SID,(pid,sid))
    return True

