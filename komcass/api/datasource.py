'''
Created on 01/10/2014

@author: komlog crew
'''

from komlibs.general.time import timeuuid
from komcass.model.orm import datasource as ormdatasource
from komcass.model.statement import datasource as stmtdatasource
from komcass.exception import datasource as excpdatasource
from komcass import connection


def get_datasource(did):
    row=connection.session.execute(stmtdatasource.S_A_MSTDATASOURCE_B_DID,(did,))
    if not row:
        return None
    else:
        return ormdatasource.Datasource(**row[0])

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
    return row[0]['count'] if row else 0

def new_datasource(datasource):
    if not datasource:
        return False
    else:
        resp=connection.session.execute(stmtdatasource.I_A_MSTDATASOURCE_INE,(datasource.did,datasource.aid,datasource.uid,datasource.datasourcename,datasource.creation_date))
        return resp[0]['[applied]'] if resp else False

def insert_datasource(datasource):
    if not isinstance(datasource, ormdatasource.Datasource):
        return False
    else:
        connection.session.execute(stmtdatasource.I_A_MSTDATASOURCE,(datasource.did,datasource.aid,datasource.uid,datasource.datasourcename,datasource.creation_date))
        return True

def delete_datasource(did):
    connection.session.execute(stmtdatasource.D_A_MSTDATASOURCE_B_DID,(did,))
    return True

def get_datasource_stats(did):
    row=connection.session.execute(stmtdatasource.S_A_MSTDATASOURCESTATS_B_DID,(did,))
    if not row:
        return None
    else:
        return ormdatasource.DatasourceStats(**row[0])

def set_last_received(did, last_received):
    connection.session.execute(stmtdatasource.I_LASTRECEIVED_MSTDATASOURCESTATS_B_DID,(did,last_received))
    return True

def set_last_mapped(did, last_mapped):
    connection.session.execute(stmtdatasource.I_LASTMAPPED_MSTDATASOURCESTATS_B_DID,(did,last_mapped))
    return True

def delete_datasource_stats(did):
    connection.session.execute(stmtdatasource.D_A_MSTDATASOURCESTATS_B_DID,(did,))
    return True

def get_datasource_data_at(did, date):
    row=connection.session.execute(stmtdatasource.S_A_DATDATASOURCE_B_DID_DATE,(did,date))
    if not row:
        return None
    else:
        return ormdatasource.DatasourceData(**row[0])

def get_datasource_data(did, fromdate, todate, count=None):
    data=[]
    if count is None:
        row=connection.session.execute(stmtdatasource.S_A_DATDATASOURCE_B_DID_INITDATE_ENDDATE,(did,fromdate,todate))
    else:
        row=connection.session.execute(stmtdatasource.S_A_DATDATASOURCE_B_DID_INITDATE_ENDDATE_COUNT,(did,fromdate,todate, count))
    if row:
        for d in row:
            data.append(ormdatasource.DatasourceData(**d))
    return data

def insert_datasource_data(dsdobj):
    if not isinstance(dsdobj, ormdatasource.DatasourceData):
        return False
    else:
        connection.session.execute(stmtdatasource.I_A_DATDATASOURCE_B_DID_DATE,(dsdobj.did,dsdobj.date,dsdobj.content))
        return True

def delete_datasource_data_at(did, date):
    connection.session.execute(stmtdatasource.D_A_DATDATASOURCE_B_DID_DATE,(did,date))
    return True

def delete_datasource_data(did):
    connection.session.execute(stmtdatasource.D_A_DATDATASOURCE_B_DID,(did,))
    return True

def insert_datasource_map(dsmapobj):
    if not isinstance(dsmapobj, ormdatasource.DatasourceMap):
        return False
    else:
        connection.session.execute(stmtdatasource.I_A_DATDATASOURCEMAP_B_DID_DATE,(dsmapobj.did,dsmapobj.date,dsmapobj.content,dsmapobj.variables, dsmapobj.datapoints))
        return True

def add_variable_to_datasource_map(did, date, position, length):
    connection.session.execute(stmtdatasource.U_VARIABLES_DATDATASOURCEMAP_B_DID_DATE,(position,length,did,date))
    return True

def add_datapoint_to_datasource_map(did, date, pid, position):
    connection.session.execute(stmtdatasource.U_DATAPOINTS_DATDATASOURCEMAP_B_DID_DATE,(pid, position, did,date))
    return True

def delete_datapoint_from_datasource_map(did, date, pid):
    connection.session.execute(stmtdatasource.D_DATAPOINT_DATDATASOURCEMAP_B_PID_DID_DATE,(pid, did, date))
    return True

def get_datasource_map(did, date):
    row=connection.session.execute(stmtdatasource.S_A_DATDATASOURCEMAP_B_DID_DATE,(did,date))
    if not row:
        return None
    else:
        return ormdatasource.DatasourceMap(**row[0])

def get_datasource_maps(did, fromdate, todate, count=None):
    if not count:
        row=connection.session.execute(stmtdatasource.S_A_DATDATASOURCEMAP_B_DID_INITDATE_ENDDATE,(did,fromdate,todate))
    else:
        row=connection.session.execute(stmtdatasource.S_A_DATDATASOURCEMAP_B_DID_INITDATE_ENDDATE_COUNT,(did,fromdate,todate,count))
    data=[]
    if row:
        for m in row:
            data.append(ormdatasource.DatasourceMap(**m))
    return data

def get_datasource_map_dates(did, fromdate, todate):
    row=connection.session.execute(stmtdatasource.S_DATE_DATDATASOURCEMAP_B_DID_INITDATE_ENDDATE,(did,fromdate,todate))
    data=[]
    if row:
        data=[r['date'] for r in row]
    return data

def get_datasource_map_variables(did, date):
    row=connection.session.execute(stmtdatasource.S_VARIABLES_DATDATASOURCEMAP_B_DID_DATE,(did,date))
    return row[0]['variables'] if row else None

def get_datasource_map_datapoints(did, date):
    row=connection.session.execute(stmtdatasource.S_DATAPOINTS_DATDATASOURCEMAP_B_DID_DATE,(did,date))
    return row[0]['datapoints'] if row else None

def delete_datasource_map(did, date):
    connection.session.execute(stmtdatasource.D_A_DATDATASOURCEMAP_B_DID_DATE,(did,date))
    return True

def delete_datasource_maps(did):
    connection.session.execute(stmtdatasource.D_A_DATDATASOURCEMAP_B_DID,(did,))
    return True

def get_datasource_text_summary(did, date):
    row=connection.session.execute(stmtdatasource.S_A_DATDATASOURCETEXTSUMMARY_B_DID_DATE,(did,date))
    if row:
        return ormdatasource.DatasourceTextSummary(**row[0])
    else:
        return None

def get_datasource_text_summaries(did, fromdate, todate):
    row=connection.session.execute(stmtdatasource.S_A_DATDATASOURCETEXTSUMMARY_B_DID_INITDATE_ENDDATE,(did,fromdate,todate))
    data=[]
    if row:
        for m in row:
            data.append(ormdatasource.DatasourceTextSummary(**m))
    return data

def insert_datasource_text_summary(dstextsummaryobj):
    if not isinstance(dstextsummaryobj, ormdatasource.DatasourceTextSummary):
        return False
    else:
        connection.session.execute(stmtdatasource.I_A_DATDATASOURCETEXTSUMMARY,(dstextsummaryobj.did,dstextsummaryobj.date,dstextsummaryobj.content_length,dstextsummaryobj.num_lines,dstextsummaryobj.num_words, dstextsummaryobj.word_frecuency))
        return True

def delete_datasource_text_summary(did, date):
    connection.session.execute(stmtdatasource.D_A_DATDATASOURCETEXTSUMMARY_B_DID_DATE,(did,date))
    return True

def delete_datasource_text_summaries(did):
    connection.session.execute(stmtdatasource.D_A_DATDATASOURCETEXTSUMMARY_B_DID,(did,))
    return True

def get_datasource_novelty_detectors_for_datapoint(did,pid):
    row=connection.session.execute(stmtdatasource.S_A_DATDATASOURCENOVELTYDETECTORDATAPOINT_B_DID_PID,(did,pid))
    data=[]
    if row:
        for d in row:
            data.append(ormdatasource.DatasourceNoveltyDetector(**d))
    return data

def get_last_datasource_novelty_detector_for_datapoint(did,pid):
    row=connection.session.execute(stmtdatasource.S_LAST_DATDATASOURCENOVELTYDETECTORDATAPOINT_B_DID_PID,(did,pid))
    if row:
        return ormdatasource.DatasourceNoveltyDetector(**row[0])
    else:
        return None

def insert_datasource_novelty_detector_for_datapoint(obj):
    if not isinstance(obj, ormdatasource.DatasourceNoveltyDetector):
        return False
    connection.session.execute(stmtdatasource.I_A_DATDATASOURCENOVELTYDETECTORDATAPOINT,(obj.did,obj.pid,obj.date,obj.nd,obj.features))
    return True

def delete_datasource_novelty_detector_for_datapoint(did, pid, date=None):
    if did and pid and date:
        connection.session.execute(stmtdatasource.D_A_DATDATASOURCENOVELTYDETECTORDATAPOINT_B_DID_PID_DATE,(did,pid,date))
        return True
    elif did and pid:
        connection.session.execute(stmtdatasource.D_A_DATDATASOURCENOVELTYDETECTORDATAPOINT_B_DID_PID,(did,pid))
        return True
    return False

