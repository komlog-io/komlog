#coding: utf-8
'''
Created on 01/10/2014

@author: komlog crew
'''

from komcass.model.orm import datasource as ormdatasource
from komcass.model.statement import datasource as stmtdatasource
from komcass.exception import datasource as excpdatasource


def get_datasource(session, did):
    row=session.execute(stmtdatasource.S_A_MSTDATASOURCE_B_DID,(did,))
    if not row:
        return None
    elif len(row)==1:
        return ormdatasource.Datasource(**row[0])
    else:
        raise excpdatasource.DataConsistencyException(function='get_datasource',field='did',value=did)

def get_datasources(session, aid=None, uid=None):
    datasources=[]
    if aid:
        row=session.execute(stmtdatasource.S_A_MSTDATASOURCE_B_AID,(aid,))
    elif uid:
        row=session.execute(stmtdatasource.S_A_MSTDATASOURCE_B_UID,(uid,))
    else:
        return datasources
    if row:
        for r in row:
            datasources.append(ormdatasource.Datasource(**r))
    return datasources

def get_datasources_dids(session, aid=None, uid=None):
    dids=[]
    if aid:
        row=session.execute(stmtdatasource.S_DID_MSTDATASOURCE_B_AID,(aid,))
    elif uid:
        row=session.execute(stmtdatasource.S_DID_MSTDATASOURCE_B_UID,(uid,))
    else:
        return dids
    if row:
        for r in row:
            dids.append(r['did'])
    return dids

def get_number_of_datasources_by_aid(session, aid):
    row=session.execute(stmtdatasource.S_COUNT_MSTDATASOURCE_B_AID,(aid,))
    return row[0]['count']

def new_datasource(session, datasource):
    if not datasource:
        return False
    else:
        existing_datasource=get_datasource(session, did=datasource.did)
        if existing_datasource:
            return False
        else:
            session.execute(stmtdatasource.I_A_MSTDATASOURCE,(datasource.did,datasource.aid,datasource.uid,datasource.datasourcename,datasource.state,datasource.creation_date))
            return True

def insert_datasource(session, datasource):
    if not datasource:
        return False
    session.execute(stmtdatasource.I_A_MSTDATASOURCE,(datasource.did,datasource.aid,datasource.uid,datasource.datasourcename,datasource.state,datasource.creation_date))
    return True

def delete_datasource(session, did):
    session.execute(stmtdatasource.D_A_MSTDATASOURCE_B_DID,(did,))
    session.execute(stmtdatasource.D_A_MSTDATASOURCESTATS_B_DID,(did,))
    session.execute(stmtdatasource.D_A_DATDATASOURCE_B_DID,(did,))
    session.execute(stmtdatasource.D_A_DATDATASOURCEMAP_B_DID,(did,))
    return True

def get_datasource_stats(session, did):
    row=session.execute(stmtdatasource.S_A_MSTDATASOURCESTATS_B_DID,(did,))
    if not row:
        return None
    elif len(row)==1:
        return ormdatasource.DatasourceStats(**row[0])
    else:
        raise excpdatasource.DataConsistencyException(function='get_datasource_stats',field='did',value=did)

def set_last_received(session, did, last_received):
    session.execute(stmtdatasource.I_LASTRECEIVED_MSTDATASOURCESTATS_B_DID,(did,last_received))
    return True

def set_last_mapped(session, did, last_mapped):
    session.execute(stmtdatasource.I_LASTMAPPED_MSTDATASOURCESTATS_B_DID,(did,last_mapped))
    return True

def get_datasource_data(session, did, date):
    row=session.execute(stmtdatasource.S_A_DATDATASOURCE_B_DID_DATE,(did,date))
    if not row:
        return None
    elif len(row)==1:
        return ormdatasource.DatasourceData(**row[0])
    else:
        raise excpdatasource.DataConsistencyException(function='get_datasource_data',field='did',value=did)

def insert_datasource_data(session, dsdobj):
    session.execute(stmtdatasource.I_A_DATDATASOURCE_B_DID_DATE,(dsdobj.did,dsdobj.date,dsdobj.content))
    return True

def delete_datasource_data(session, did, date):
    session.execute(stmtdatasource.D_A_DATDATASOURCE_B_DID_DATE,(did,date))
    return True

def insert_datasource_map(session, dsmapobj):
    session.execute(stmtdatasource.I_A_DATDATASOURCEMAP_B_DID_DATE,(dsmapobj.did,dsmapobj.date,dsmapobj.content,dsmapobj.variables, dsmapobj.datapoints))
    return True

def add_variable_to_datasource_map(session, did, date, position, length):
    session.execute(stmtdatasource.U_VARIABLES_DATASOURCEMAP_B_DID_DATE,(position,length,did,date))
    return True

def add_datapoint_to_datasource_map(session, did, date, pid, position):
    session.execute(stmtdatasource.U_DATAPOINTS_DATASOURCEMAP_B_DID_DATE,(pid, position, did,date))
    return True

def get_datasource_map(session, did, date):
    row=session.execute(stmtdatasource.S_A_DATDATASOURCEMAP_B_DID_DATE,(did,date))
    if not row:
        return None
    elif len(row)==1:
        return ormdatasource.DatasourceMap(**row[0])
    else:
        raise excpdatasource.DataConsistencyException(function='get_datasource_map',field='did',value=did)

def get_datasource_maps(session, did, fromdate, todate):
    row=session.execute(stmtdatasource.S_A_DATDATASOURCEMAP_B_DID_INITDATE_ENDDATE,(did,fromdate,todate))
    data=[]
    if row:
        for m in row:
            data.append(ormdatasource.DatasourceMap(**m))
    return data

def get_datasource_map_variables(session, did, date):
    row=session.execute(stmtdatasource.S_VARIABLES_DATDATASOURCEMAP_B_DID_DATE,(did,date))
    if not row:
        return None
    if len(row)==1:
        return row[0]['variables']
    else:
        raise excpdatasource.DataConsistencyException(function='get_datasource_map_variables',field='did',value=did)

def get_datasource_map_datapoints(session, did, date):
    row=session.execute(stmtdatasource.S_DATAPOINTS_DATDATASOURCEMAP_B_DID_DATE,(did,date))
    if not row:
        return None
    elif len(row)==1:
        return row[0]['datapoints']
    else:
        raise excpdatasource.DataConsistencyException(function='get_datasource_map_variables',field='did',value=did)

def delete_datasource_map(session, did, date):
    session.execute(stmtdatasource.D_A_DATDATASOURCEMAP_B_DID_DATE,(did,date))
    return True

