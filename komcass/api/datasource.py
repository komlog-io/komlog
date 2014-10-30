#coding: utf-8
'''
Created on 01/10/2014

@author: komlog crew
'''

from komcass.model.orm import datasource as ormdatasource
from komcass.model.statement import datasource as stmtdatasource
from komcass.exception import datasource as excpdatasource
from komcass import connection


def get_datasource(did):
    row=connection.session.execute(stmtdatasource.S_A_MSTDATASOURCE_B_DID,(did,))
    if not row:
        return None
    elif len(row)==1:
        return ormdatasource.Datasource(**row[0])
    else:
        raise excpdatasource.DataConsistencyException(function='get_datasource',field='did',value=did)

def get_datasources(aid=None, uid=None):
    datasources=[]
    if aid:
        row=connection.session.execute(stmtdatasource.S_A_MSTDATASOURCE_B_AID,(aid,))
    elif uid:
        row=connection.session.execute(stmtdatasource.S_A_MSTDATASOURCE_B_UID,(uid,))
    else:
        return datasources
    if row:
        for r in row:
            datasources.append(ormdatasource.Datasource(**r))
    return datasources

def get_datasources_dids(aid=None, uid=None):
    dids=[]
    if aid:
        row=connection.session.execute(stmtdatasource.S_DID_MSTDATASOURCE_B_AID,(aid,))
    elif uid:
        row=connection.session.execute(stmtdatasource.S_DID_MSTDATASOURCE_B_UID,(uid,))
    else:
        return dids
    if row:
        for r in row:
            dids.append(r['did'])
    return dids

def get_number_of_datasources_by_aid(aid):
    row=connection.session.execute(stmtdatasource.S_COUNT_MSTDATASOURCE_B_AID,(aid,))
    return row[0]['count']

def new_datasource(datasource):
    if not datasource:
        return False
    else:
        existing_datasource=get_datasource(did=datasource.did)
        if existing_datasource:
            return False
        else:
            connection.session.execute(stmtdatasource.I_A_MSTDATASOURCE,(datasource.did,datasource.aid,datasource.uid,datasource.datasourcename,datasource.state,datasource.creation_date))
            return True

def insert_datasource(datasource):
    if not datasource:
        return False
    connection.session.execute(stmtdatasource.I_A_MSTDATASOURCE,(datasource.did,datasource.aid,datasource.uid,datasource.datasourcename,datasource.state,datasource.creation_date))
    return True

def delete_datasource(did):
    connection.session.execute(stmtdatasource.D_A_MSTDATASOURCE_B_DID,(did,))
    connection.session.execute(stmtdatasource.D_A_MSTDATASOURCESTATS_B_DID,(did,))
    connection.session.execute(stmtdatasource.D_A_DATDATASOURCE_B_DID,(did,))
    connection.session.execute(stmtdatasource.D_A_DATDATASOURCEMAP_B_DID,(did,))
    return True

def get_datasource_stats(did):
    row=connection.session.execute(stmtdatasource.S_A_MSTDATASOURCESTATS_B_DID,(did,))
    if not row:
        return None
    elif len(row)==1:
        return ormdatasource.DatasourceStats(**row[0])
    else:
        raise excpdatasource.DataConsistencyException(function='get_datasource_stats',field='did',value=did)

def set_last_received(did, last_received):
    connection.session.execute(stmtdatasource.I_LASTRECEIVED_MSTDATASOURCESTATS_B_DID,(did,last_received))
    return True

def set_last_mapped(did, last_mapped):
    connection.session.execute(stmtdatasource.I_LASTMAPPED_MSTDATASOURCESTATS_B_DID,(did,last_mapped))
    return True

def get_datasource_data(did, date):
    row=connection.session.execute(stmtdatasource.S_A_DATDATASOURCE_B_DID_DATE,(did,date))
    if not row:
        return None
    elif len(row)==1:
        return ormdatasource.DatasourceData(**row[0])
    else:
        raise excpdatasource.DataConsistencyException(function='get_datasource_data',field='did',value=did)

def insert_datasource_data(dsdobj):
    connection.session.execute(stmtdatasource.I_A_DATDATASOURCE_B_DID_DATE,(dsdobj.did,dsdobj.date,dsdobj.content))
    return True

def delete_datasource_data(did, date):
    connection.session.execute(stmtdatasource.D_A_DATDATASOURCE_B_DID_DATE,(did,date))
    return True

def insert_datasource_map(dsmapobj):
    connection.session.execute(stmtdatasource.I_A_DATDATASOURCEMAP_B_DID_DATE,(dsmapobj.did,dsmapobj.date,dsmapobj.content,dsmapobj.variables, dsmapobj.datapoints))
    return True

def add_variable_to_datasource_map(did, date, position, length):
    connection.session.execute(stmtdatasource.U_VARIABLES_DATASOURCEMAP_B_DID_DATE,(position,length,did,date))
    return True

def add_datapoint_to_datasource_map(did, date, pid, position):
    connection.session.execute(stmtdatasource.U_DATAPOINTS_DATASOURCEMAP_B_DID_DATE,(pid, position, did,date))
    return True

def get_datasource_map(did, date):
    row=connection.session.execute(stmtdatasource.S_A_DATDATASOURCEMAP_B_DID_DATE,(did,date))
    if not row:
        return None
    elif len(row)==1:
        return ormdatasource.DatasourceMap(**row[0])
    else:
        raise excpdatasource.DataConsistencyException(function='get_datasource_map',field='did',value=did)

def get_datasource_maps(did, fromdate, todate):
    row=connection.session.execute(stmtdatasource.S_A_DATDATASOURCEMAP_B_DID_INITDATE_ENDDATE,(did,fromdate,todate))
    data=[]
    if row:
        for m in row:
            data.append(ormdatasource.DatasourceMap(**m))
    return data

def get_datasource_map_variables(did, date):
    row=connection.session.execute(stmtdatasource.S_VARIABLES_DATDATASOURCEMAP_B_DID_DATE,(did,date))
    if not row:
        return None
    if len(row)==1:
        return row[0]['variables']
    else:
        raise excpdatasource.DataConsistencyException(function='get_datasource_map_variables',field='did',value=did)

def get_datasource_map_datapoints(did, date):
    row=connection.session.execute(stmtdatasource.S_DATAPOINTS_DATDATASOURCEMAP_B_DID_DATE,(did,date))
    if not row:
        return None
    elif len(row)==1:
        return row[0]['datapoints']
    else:
        raise excpdatasource.DataConsistencyException(function='get_datasource_map_variables',field='did',value=did)

def delete_datasource_map(did, date):
    connection.session.execute(stmtdatasource.D_A_DATDATASOURCEMAP_B_DID_DATE,(did,date))
    return True

