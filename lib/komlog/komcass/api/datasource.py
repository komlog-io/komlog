'''
Created on 01/10/2014

@author: komlog crew
'''

from komlog.komlibs.general.time import timeuuid
from komlog.komcass.model.orm import datasource as ormdatasource
from komlog.komcass.model.statement import datasource as stmtdatasource
from komlog.komcass import connection, exceptions


@exceptions.ExceptionHandler
def get_datasource(did):
    row=connection.session.execute(stmtdatasource.S_A_MSTDATASOURCE_B_DID,(did,))
    if not row:
        return None
    else:
        return ormdatasource.Datasource(**row[0])

@exceptions.ExceptionHandler
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

@exceptions.ExceptionHandler
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

@exceptions.ExceptionHandler
def get_number_of_datasources_by_aid(aid):
    row=connection.session.execute(stmtdatasource.S_COUNT_MSTDATASOURCE_B_AID,(aid,))
    return row[0]['count'] if row else 0

@exceptions.ExceptionHandler
def new_datasource(datasource):
    if not isinstance(datasource, ormdatasource.Datasource):
        return False
    else:
        resp=connection.session.execute(stmtdatasource.I_A_MSTDATASOURCE_INE,(datasource.did,datasource.aid,datasource.uid,datasource.datasourcename,datasource.creation_date))
        return resp[0]['[applied]'] if resp else False

@exceptions.ExceptionHandler
def insert_datasource(datasource):
    if not isinstance(datasource, ormdatasource.Datasource):
        return False
    else:
        connection.session.execute(stmtdatasource.I_A_MSTDATASOURCE,(datasource.did,datasource.aid,datasource.uid,datasource.datasourcename,datasource.creation_date))
        return True

@exceptions.ExceptionHandler
def delete_datasource(did):
    connection.session.execute(stmtdatasource.D_A_MSTDATASOURCE_B_DID,(did,))
    return True

@exceptions.ExceptionHandler
def get_datasource_stats(did):
    row=connection.session.execute(stmtdatasource.S_A_MSTDATASOURCESTATS_B_DID,(did,))
    if not row:
        return None
    else:
        return ormdatasource.DatasourceStats(**row[0])

@exceptions.ExceptionHandler
def set_last_received(did, last_received):
    connection.session.execute(stmtdatasource.I_LASTRECEIVED_MSTDATASOURCESTATS_B_DID,(did,last_received))
    return True

@exceptions.ExceptionHandler
def set_last_mapped(did, last_mapped):
    connection.session.execute(stmtdatasource.I_LASTMAPPED_MSTDATASOURCESTATS_B_DID,(did,last_mapped))
    return True

@exceptions.ExceptionHandler
def delete_datasource_stats(did):
    connection.session.execute(stmtdatasource.D_A_MSTDATASOURCESTATS_B_DID,(did,))
    return True

@exceptions.ExceptionHandler
def get_datasource_data_at(did, date):
    row=connection.session.execute(stmtdatasource.S_A_DATDATASOURCE_B_DID_DATE,(did,date))
    if not row:
        return None
    else:
        return ormdatasource.DatasourceData(**row[0])

@exceptions.ExceptionHandler
def get_datasource_data(did, fromdate=None, todate=None, count=None):
    data=[]
    if fromdate:
        if todate:
            if count:
                row=connection.session.execute(stmtdatasource.S_A_DATDATASOURCE_B_DID_INITDATE_ENDDATE_COUNT,(did,fromdate, todate, count))
            else:
                row=connection.session.execute(stmtdatasource.S_A_DATDATASOURCE_B_DID_INITDATE_ENDDATE,(did, fromdate, todate))
        else:
            if count:
                row=connection.session.execute(stmtdatasource.S_A_DATDATASOURCE_B_DID_INITDATE_COUNT,(did, fromdate, count))
            else:
                row=connection.session.execute(stmtdatasource.S_A_DATDATASOURCE_B_DID_INITDATE,(did, fromdate))
    else:
        if todate:
            if count:
                row=connection.session.execute(stmtdatasource.S_A_DATDATASOURCE_B_DID_ENDDATE_COUNT,(did, todate, count))
            else:
                row=connection.session.execute(stmtdatasource.S_A_DATDATASOURCE_B_DID_ENDDATE,(did, todate))
        else:
            if count:
                row=connection.session.execute(stmtdatasource.S_A_DATDATASOURCE_B_DID_COUNT,(did, count))
            else:
                row=connection.session.execute(stmtdatasource.S_A_DATDATASOURCE_B_DID,(did, ))
    if row:
        for d in row:
            data.append(ormdatasource.DatasourceData(**d))
    return data

@exceptions.ExceptionHandler
def insert_datasource_data(dsdobj):
    if not isinstance(dsdobj, ormdatasource.DatasourceData):
        return False
    else:
        connection.session.execute(stmtdatasource.I_A_DATDATASOURCE_B_DID_DATE,(dsdobj.did,dsdobj.date,dsdobj.content))
        return True

@exceptions.ExceptionHandler
def delete_datasource_data_at(did, date):
    connection.session.execute(stmtdatasource.D_A_DATDATASOURCE_B_DID_DATE,(did,date))
    return True

@exceptions.ExceptionHandler
def delete_datasource_data(did):
    connection.session.execute(stmtdatasource.D_A_DATDATASOURCE_B_DID,(did,))
    return True

@exceptions.ExceptionHandler
def insert_datasource_map(dsmapobj):
    if not isinstance(dsmapobj, ormdatasource.DatasourceMap):
        return False
    else:
        connection.session.execute(stmtdatasource.I_A_DATDATASOURCEMAP_B_DID_DATE,(dsmapobj.did,dsmapobj.date,dsmapobj.variables, dsmapobj.datapoints))
        return True

@exceptions.ExceptionHandler
def add_variable_to_datasource_map(did, date, position, length):
    connection.session.execute(stmtdatasource.U_VARIABLES_DATDATASOURCEMAP_B_DID_DATE,(position,length,did,date))
    return True

@exceptions.ExceptionHandler
def add_datapoint_to_datasource_map(did, date, pid, position):
    connection.session.execute(stmtdatasource.U_DATAPOINTS_DATDATASOURCEMAP_B_DID_DATE,(pid, position, did,date))
    return True

@exceptions.ExceptionHandler
def delete_datapoint_from_datasource_map(did, date, pid):
    connection.session.execute(stmtdatasource.D_DATAPOINT_DATDATASOURCEMAP_B_PID_DID_DATE,(pid, did, date))
    return True

@exceptions.ExceptionHandler
def get_datasource_map(did, date):
    row=connection.session.execute(stmtdatasource.S_A_DATDATASOURCEMAP_B_DID_DATE,(did,date))
    if not row:
        return None
    else:
        return ormdatasource.DatasourceMap(**row[0])

@exceptions.ExceptionHandler
def get_datasource_maps(did, fromdate=None, todate=None, count=None):
    data=[]
    if fromdate:
        if todate:
            if count:
                row=connection.session.execute(stmtdatasource.S_A_DATDATASOURCEMAP_B_DID_INITDATE_ENDDATE_COUNT,(did,fromdate, todate, count))
            else:
                row=connection.session.execute(stmtdatasource.S_A_DATDATASOURCEMAP_B_DID_INITDATE_ENDDATE,(did, fromdate, todate))
        else:
            if count:
                row=connection.session.execute(stmtdatasource.S_A_DATDATASOURCEMAP_B_DID_INITDATE_COUNT,(did, fromdate, count))
            else:
                row=connection.session.execute(stmtdatasource.S_A_DATDATASOURCEMAP_B_DID_INITDATE,(did, fromdate))
    else:
        if todate:
            if count:
                row=connection.session.execute(stmtdatasource.S_A_DATDATASOURCEMAP_B_DID_ENDDATE_COUNT,(did, todate, count))
            else:
                row=connection.session.execute(stmtdatasource.S_A_DATDATASOURCEMAP_B_DID_ENDDATE,(did, todate))
        else:
            if count:
                row=connection.session.execute(stmtdatasource.S_A_DATDATASOURCEMAP_B_DID_COUNT,(did, count))
            else:
                row=connection.session.execute(stmtdatasource.S_A_DATDATASOURCEMAP_B_DID,(did, ))
    if row:
        for m in row:
            data.append(ormdatasource.DatasourceMap(**m))
    return data

@exceptions.ExceptionHandler
def get_datasource_map_dates(did, fromdate=None, todate=None, count=None):
    data=[]
    if fromdate:
        if todate:
            if count:
                row=connection.session.execute(stmtdatasource.S_DATE_DATDATASOURCEMAP_B_DID_INITDATE_ENDDATE_COUNT,(did,fromdate, todate, count))
            else:
                row=connection.session.execute(stmtdatasource.S_DATE_DATDATASOURCEMAP_B_DID_INITDATE_ENDDATE,(did, fromdate, todate))
        else:
            if count:
                row=connection.session.execute(stmtdatasource.S_DATE_DATDATASOURCEMAP_B_DID_INITDATE_COUNT,(did, fromdate, count))
            else:
                row=connection.session.execute(stmtdatasource.S_DATE_DATDATASOURCEMAP_B_DID_INITDATE,(did, fromdate))
    else:
        if todate:
            if count:
                row=connection.session.execute(stmtdatasource.S_DATE_DATDATASOURCEMAP_B_DID_ENDDATE_COUNT,(did, todate, count))
            else:
                row=connection.session.execute(stmtdatasource.S_DATE_DATDATASOURCEMAP_B_DID_ENDDATE,(did, todate))
        else:
            if count:
                row=connection.session.execute(stmtdatasource.S_DATE_DATDATASOURCEMAP_B_DID_COUNT,(did, count))
            else:
                row=connection.session.execute(stmtdatasource.S_DATE_DATDATASOURCEMAP_B_DID,(did, ))
    if row:
        data=[r['date'] for r in row]
    return data


@exceptions.ExceptionHandler
def get_datasource_map_variables(did, date):
    row=connection.session.execute(stmtdatasource.S_VARIABLES_DATDATASOURCEMAP_B_DID_DATE,(did,date))
    return row[0]['variables'] if row else None

@exceptions.ExceptionHandler
def get_datasource_map_datapoints(did, date):
    row=connection.session.execute(stmtdatasource.S_DATAPOINTS_DATDATASOURCEMAP_B_DID_DATE,(did,date))
    return row[0]['datapoints'] if row else None

@exceptions.ExceptionHandler
def delete_datasource_map(did, date):
    connection.session.execute(stmtdatasource.D_A_DATDATASOURCEMAP_B_DID_DATE,(did,date))
    return True

@exceptions.ExceptionHandler
def delete_datasource_maps(did):
    connection.session.execute(stmtdatasource.D_A_DATDATASOURCEMAP_B_DID,(did,))
    return True

@exceptions.ExceptionHandler
def get_datasource_text_summary(did, date):
    row=connection.session.execute(stmtdatasource.S_A_DATDATASOURCETEXTSUMMARY_B_DID_DATE,(did,date))
    if row:
        return ormdatasource.DatasourceTextSummary(**row[0])
    else:
        return None

@exceptions.ExceptionHandler
def get_datasource_text_summaries(did, fromdate, todate):
    row=connection.session.execute(stmtdatasource.S_A_DATDATASOURCETEXTSUMMARY_B_DID_INITDATE_ENDDATE,(did,fromdate,todate))
    data=[]
    if row:
        for m in row:
            data.append(ormdatasource.DatasourceTextSummary(**m))
    return data

@exceptions.ExceptionHandler
def insert_datasource_text_summary(dstextsummaryobj):
    if not isinstance(dstextsummaryobj, ormdatasource.DatasourceTextSummary):
        return False
    else:
        connection.session.execute(stmtdatasource.I_A_DATDATASOURCETEXTSUMMARY,(dstextsummaryobj.did,dstextsummaryobj.date,dstextsummaryobj.content_length,dstextsummaryobj.num_lines,dstextsummaryobj.num_words, dstextsummaryobj.word_frecuency))
        return True

@exceptions.ExceptionHandler
def delete_datasource_text_summary(did, date):
    connection.session.execute(stmtdatasource.D_A_DATDATASOURCETEXTSUMMARY_B_DID_DATE,(did,date))
    return True

@exceptions.ExceptionHandler
def delete_datasource_text_summaries(did):
    connection.session.execute(stmtdatasource.D_A_DATDATASOURCETEXTSUMMARY_B_DID,(did,))
    return True

@exceptions.ExceptionHandler
def get_datasource_hash(did, date):
    row=connection.session.execute(stmtdatasource.S_A_DATDATASOURCEHASH_B_DID_DATE,(did,date))
    if not row:
        return None
    else:
        return ormdatasource.DatasourceHash(**row[0])

@exceptions.ExceptionHandler
def get_datasource_hashes(did, fromdate=None, todate=None, count=None):
    data=[]
    if fromdate:
        if todate:
            if count:
                row=connection.session.execute(stmtdatasource.S_A_DATDATASOURCEHASH_B_DID_INITDATE_ENDDATE_COUNT,(did,fromdate, todate, count))
            else:
                row=connection.session.execute(stmtdatasource.S_A_DATDATASOURCEHASH_B_DID_INITDATE_ENDDATE,(did, fromdate, todate))
        else:
            if count:
                row=connection.session.execute(stmtdatasource.S_A_DATDATASOURCEHASH_B_DID_INITDATE_COUNT,(did, fromdate, count))
            else:
                row=connection.session.execute(stmtdatasource.S_A_DATDATASOURCEHASH_B_DID_INITDATE,(did, fromdate))
    else:
        if todate:
            if count:
                row=connection.session.execute(stmtdatasource.S_A_DATDATASOURCEHASH_B_DID_ENDDATE_COUNT,(did, todate, count))
            else:
                row=connection.session.execute(stmtdatasource.S_A_DATDATASOURCEHASH_B_DID_ENDDATE,(did, todate))
        else:
            if count:
                row=connection.session.execute(stmtdatasource.S_A_DATDATASOURCEHASH_B_DID_COUNT,(did, count))
            else:
                row=connection.session.execute(stmtdatasource.S_A_DATDATASOURCEHASH_B_DID,(did, ))
    if row:
        for d in row:
            data.append(ormdatasource.DatasourceHash(**d))
    return data

@exceptions.ExceptionHandler
def insert_datasource_hash(obj):
    if not isinstance(obj, ormdatasource.DatasourceHash):
        return False
    else:
        connection.session.execute(stmtdatasource.I_A_DATDATASOURCEHASH,(obj.did,obj.date,obj.content))
        return True

@exceptions.ExceptionHandler
def delete_datasource_hash(did, date):
    connection.session.execute(stmtdatasource.D_A_DATDATASOURCEHASH_B_DID_DATE,(did,date))
    return True

@exceptions.ExceptionHandler
def delete_datasource_hashes(did):
    connection.session.execute(stmtdatasource.D_A_DATDATASOURCEHASH_B_DID,(did,))
    return True

@exceptions.ExceptionHandler
def get_datasource_metadata(did, fromdate, todate, count=None):
    data=[]
    if count is None:
        row=connection.session.execute(stmtdatasource.S_A_DATDATASOURCEMETADATA_B_DID_INITDATE_ENDDATE,(did,fromdate,todate))
    else:
        row=connection.session.execute(stmtdatasource.S_A_DATDATASOURCEMETADATA_B_DID_INITDATE_ENDDATE_COUNT,(did,fromdate,todate, count))
    if row:
        for d in row:
            data.append(ormdatasource.DatasourceMetadata(**d))
    return data

@exceptions.ExceptionHandler
def get_datasource_metadata_at(did,date):
    row=connection.session.execute(stmtdatasource.S_A_DATDATASOURCEMETADATA_B_DID_DATE,(did,date))
    if not row:
        return None
    else:
        return ormdatasource.DatasourceMetadata(**row[0])

@exceptions.ExceptionHandler
def get_datasource_metadata_size_at(did, date):
    row=connection.session.execute(stmtdatasource.S_SIZE_DATDATASOURCEMETADATA_B_DID_DATE,(did,date))
    return row[0]['size'] if row else None

@exceptions.ExceptionHandler
def insert_datasource_metadata(obj):
    if not isinstance(obj, ormdatasource.DatasourceMetadata):
        return False
    else:
        connection.session.execute(stmtdatasource.I_A_DATDATASOURCEMETADATA,(obj.did,obj.date,obj.size))
        return True

@exceptions.ExceptionHandler
def delete_datasource_metadata(did):
    connection.session.execute(stmtdatasource.D_A_DATDATASOURCEMETADATA_B_DID,(did,))
    return True

@exceptions.ExceptionHandler
def delete_datasource_metadata_at(did, date):
    connection.session.execute(stmtdatasource.D_A_DATDATASOURCEMETADATA_B_DID_DATE,(did,date))
    return True

@exceptions.ExceptionHandler
def get_datasource_hooks_sids(did):
    sids=[]
    row=connection.session.execute(stmtdatasource.S_SID_MSTDATASOURCEHOOKS_B_DID,(did,))
    if row:
        for r in row:
            sids.append(r['sid'])
    return sids

@exceptions.ExceptionHandler
def insert_datasource_hook(did,sid):
    connection.session.execute(stmtdatasource.I_A_MSTDATASOURCEHOOKS,(did,sid))
    return True

@exceptions.ExceptionHandler
def delete_datasource_hooks(did):
    connection.session.execute(stmtdatasource.D_A_MSTDATASOURCEHOOKS_B_DID,(did,))
    return True

@exceptions.ExceptionHandler
def delete_datasource_hook(did,sid):
    connection.session.execute(stmtdatasource.D_A_MSTDATASOURCEHOOKS_B_DID_SID,(did,sid))
    return True

@exceptions.ExceptionHandler
def get_datasource_supplies(did, fromdate, todate):
    data = []
    row = connection.session.execute(stmtdatasource.S_A_DATDATASOURCESUPPLIES_B_DID_INITDATE_ENDDATE,(did, fromdate, todate))
    if row:
        for d in row:
            data.append(ormdatasource.DatasourceSupplies(**d))
    return data

@exceptions.ExceptionHandler
def get_datasource_supplies_at(did, date):
    row = connection.session.execute(stmtdatasource.S_A_DATDATASOURCESUPPLIES_B_DID_DATE,(did, date))
    return ormdatasource.DatasourceSupplies(**row[0]) if row else None

@exceptions.ExceptionHandler
def get_last_datasource_supplies_count(did, count=1):
    data = []
    row = connection.session.execute(stmtdatasource.S_A_DATDATASOURCESUPPLIES_B_DID_COUNT,(did, count))
    if row:
        for d in row:
            data.append(ormdatasource.DatasourceSupplies(**d))
    return data

@exceptions.ExceptionHandler
def insert_datasource_supplies(did, date, supplies):
    connection.session.execute(stmtdatasource.I_A_DATDATASOURCESUPPLIES,(did, date, supplies))
    return True

@exceptions.ExceptionHandler
def delete_datasource_supplies(did):
    connection.session.execute(stmtdatasource.D_A_DATDATASOURCESUPPLIES_B_DID,(did,))
    return True

@exceptions.ExceptionHandler
def delete_datasource_supplies_at(did, date):
    connection.session.execute(stmtdatasource.D_A_DATDATASOURCESUPPLIES_B_DID_DATE,(did, date))
    return True

@exceptions.ExceptionHandler
def get_datasource_features(did):
    row = connection.session.execute(stmtdatasource.S_DATEFEATURES_MSTDATASOURCEFEATURES_B_DID,(did,))
    return ormdatasource.DatasourceFeatures(did, **row[0]) if row else None

@exceptions.ExceptionHandler
def insert_datasource_features(did, date, features):
    connection.session.execute(stmtdatasource.I_A_MSTDATASOURCEFEATURES,(did, date, features))
    return True

@exceptions.ExceptionHandler
def delete_datasource_features(did):
    connection.session.execute(stmtdatasource.D_A_MSTDATASOURCEFEATURES_B_DID,(did,))
    return True

@exceptions.ExceptionHandler
def get_datasources_by_feature(feature, count=1):
    data = []
    row = connection.session.execute(stmtdatasource.S_DIDWEIGHT_MSTDATASOURCEBYFEATURE_B_FEATURE_COUNT,(feature,count))
    if row:
        for r in row:
            data.append(ormdatasource.DatasourceByFeature(feature, **r))
    return data

@exceptions.ExceptionHandler
def insert_datasource_by_feature(feature, did, weight):
    connection.session.execute(stmtdatasource.I_A_MSTDATASOURCEBYFEATURE,(feature, did, weight))
    return True

@exceptions.ExceptionHandler
def insert_datasource_by_features(did, info):
    stmts = []
    for item in info:
        stmts.append((stmtdatasource.I_A_MSTDATASOURCEBYFEATURE,(item['feature'], did, item['weight'])))
    connection.session.execute_batch(stmts)
    return True

@exceptions.ExceptionHandler
def delete_datasource_by_feature(feature, did):
    connection.session.execute(stmtdatasource.D_A_MSTDATASOURCEBYFEATURE_B_FEATURE_DID,(feature,did))
    return True

@exceptions.ExceptionHandler
def delete_datasource_by_features(did, features):
    stmts = []
    for feature in features:
        stmts.append((stmtdatasource.D_A_MSTDATASOURCEBYFEATURE_B_FEATURE_DID,(feature,did)))
    connection.session.execute_batch(stmts)
    return True

@exceptions.ExceptionHandler
def get_datapoint_classifier_dtree(did):
    row=connection.session.execute(stmtdatasource.S_DTREE_MSTDATAPOINTCLASSIFIERDTREE_B_DID,(did,))
    return row[0]['dtree'] if row else None

@exceptions.ExceptionHandler
def insert_datapoint_classifier_dtree(did, dtree):
    connection.session.execute(stmtdatasource.I_A_MSTDATAPOINTCLASSIFIERDTREE,(did, dtree))
    return True

@exceptions.ExceptionHandler
def delete_datapoint_classifier_dtree(did):
    connection.session.execute(stmtdatasource.D_A_MSTDATAPOINTCLASSIFIERDTREE_B_DID,(did,))
    return True


