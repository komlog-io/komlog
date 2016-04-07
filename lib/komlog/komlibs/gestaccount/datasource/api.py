'''
datasource.py: library for managing datasource operations

This file implements the logic of different datasource operations at a service level.
At this point, authorization and autentication has been passed

creation date: 2013/03/31
author: jcazor
'''

import uuid
import json
import os
import pickle
from komlog.komfig import logging
from komlog.komcass.api import user as cassapiuser
from komlog.komcass.api import agent as cassapiagent
from komlog.komcass.api import datasource as cassapidatasource
from komlog.komcass.api import datapoint as cassapidatapoint
from komlog.komcass.api import widget as cassapiwidget
from komlog.komcass.api import dashboard as cassapidashboard
from komlog.komcass.model.orm import datasource as ormdatasource
from komlog.komfs import api as fsapi
from komlog.komlibs.ai.decisiontree import api as dtreeapi
from komlog.komlibs.ai.svm import api as svmapi
from komlog.komlibs.gestaccount import exceptions
from komlog.komlibs.gestaccount.errors import Errors
from komlog.komlibs.general.validation import arguments as args
from komlog.komlibs.general.time import timeuuid
from komlog.komlibs.textman.api import variables as textmanvar
from komlog.komlibs.textman.api import summary as textmansummary
from komlog.komlibs.graph.api import uri as graphuri

def create_datasource(uid,aid,datasourcename):
    if not args.is_valid_uuid(uid):
        raise exceptions.BadParametersException(error=Errors.E_GDA_CRD_IU)
    if not args.is_valid_uuid(aid):
        raise exceptions.BadParametersException(error=Errors.E_GDA_CRD_IA)
    if not args.is_valid_uri(datasourcename):
        raise exceptions.BadParametersException(error=Errors.E_GDA_CRD_IDN)
    now=timeuuid.uuid1()
    did=uuid.uuid4()
    user=cassapiuser.get_user(uid=uid)
    agent=cassapiagent.get_agent(aid=aid)
    if not user:
        raise exceptions.UserNotFoundException(error=Errors.E_GDA_CRD_UNF)
    if not agent:
        raise exceptions.AgentNotFoundException(error=Errors.E_GDA_CRD_ANF)
    if not graphuri.new_datasource_uri(uid=uid, uri=datasourcename, did=did):
        raise exceptions.DatasourceCreationException(error=Errors.E_GDA_CRD_ADU)
    datasource=ormdatasource.Datasource(did=did,aid=aid,uid=uid,datasourcename=datasourcename,creation_date=now)
    if cassapidatasource.new_datasource(datasource=datasource):
        return {'did':datasource.did, 'datasourcename':datasource.datasourcename, 'uid': datasource.uid, 'aid':datasource.aid}
    else:
        graphuri.dissociate_vertex(ido=did)
        raise exceptions.DatasourceCreationException(error=Errors.E_GDA_CRD_IDE)

def get_last_processed_datasource_data(did):
    if not args.is_valid_uuid(did):
        raise exceptions.BadParametersException(error=Errors.E_GDA_GLPD_ID)
    datasource_stats=cassapidatasource.get_datasource_stats(did=did)
    if datasource_stats and datasource_stats.last_mapped:
        last_mapped=datasource_stats.last_mapped
        datasource_data=cassapidatasource.get_datasource_data_at(did=did,date=last_mapped)
        if not datasource_data or not datasource_data.content:
            raise exceptions.DatasourceDataNotFoundException(error=Errors.E_GDA_GLPD_DDNF)
        dsvars=cassapidatasource.get_datasource_map_variables(did=did,date=last_mapped)
        datasource_datapoints=cassapidatasource.get_datasource_map_datapoints(did=did, date=last_mapped)
        dsdtps=[]
        if datasource_datapoints:
            for pid,pos in datasource_datapoints.items():
                dsdtps.append({'pid':pid,'position':pos})
        data={}
        data['did']=did
        data['date']=last_mapped
        data['variables']=[(pos,length) for pos,length in dsvars.items()] if dsvars else None
        data['content']=datasource_data.content
        data['datapoints']=dsdtps
        return data
    else:
        raise exceptions.DatasourceNotFoundException(error=Errors.E_GDA_GLPD_DNF)

def upload_datasource_data(did,content,dest_dir):
    if not args.is_valid_uuid(did):
        raise exceptions.BadParametersException(error=Errors.E_GDA_UDD_ID)
    if not args.is_valid_datasource_content(content):
        raise exceptions.BadParametersException(error=Errors.E_GDA_UDD_IDC)
    if not args.is_valid_string(dest_dir):
        raise exceptions.BadParametersException(error=Errors.E_GDA_UDD_IDD)
    datasource=cassapidatasource.get_datasource(did=did)
    if datasource:
        now=timeuuid.uuid1()
        filedata={}
        filedata['received']=now.hex
        filedata['did']=did.hex
        filedata['json_content']=content
        try:
            json_filedata=json.dumps(filedata)
        except Exception:
            raise exceptions.BadParametersException(error=Errors.E_GDA_UDD_IFD)
        filename=now.hex+'_'+did.hex+'.pspl'
        destfile=os.path.join(dest_dir,filename)
        if fsapi.create_sample(destfile,json_filedata):
            return destfile
        else:
            raise exceptions.DatasourceUploadContentException(error=Errors.E_GDA_UDD_ESD)
    else:
        raise exceptions.DatasourceNotFoundException(error=Errors.E_GDA_UDD_DNF)

def get_datasource_data(did, date):
    if not args.is_valid_uuid(did):
        raise exceptions.BadParametersException(error=Errors.E_GDA_GDD_ID)
    if not args.is_valid_date(date):
        raise exceptions.BadParametersException(error=Errors.E_GDA_GDD_IDT)
    dsdata=cassapidatasource.get_datasource_data_at(did=did, date=date)
    if dsdata:
        dsvars=cassapidatasource.get_datasource_map_variables(did=did,date=date)
        datasource_datapoints=cassapidatasource.get_datasource_map_datapoints(did=did, date=date)
        dsdtps=[]
        if datasource_datapoints:
            for pid,pos in datasource_datapoints.items():
                dsdtps.append({'pid':pid,'position':pos})
        data={}
        data['did']=dsdata.did
        data['date']=dsdata.date
        data['variables']=[(pos,length) for pos,length in dsvars.items()] if dsvars else None
        data['content']=dsdata.content
        data['datapoints']=dsdtps
        return data
    else:
        raise exceptions.DatasourceDataNotFoundException(error=Errors.E_GDA_GDD_DDNF)

def store_datasource_data(did, date, content):
    if not args.is_valid_uuid(did) or not args.is_valid_datasource_content(content) or not args.is_valid_date(date):
        return False
    dsdobj=ormdatasource.DatasourceData(did=did,date=date,content=content)
    if cassapidatasource.insert_datasource_data(dsdobj=dsdobj):
        if cassapidatasource.set_last_received(did=did, last_received=date):
            return True
        else:
            cassapidatasource.delete_datasource_data_at(did=did, date=date)
            return False
    else:
        return False

def get_datasource_config(did, pids_flag=True):
    if not args.is_valid_uuid(did):
        raise exceptions.BadParametersException(error=Errors.E_GDA_GDC_ID)
    datasource=cassapidatasource.get_datasource(did=did)
    if datasource:
        data={}
        data['did']=did
        data['aid']=datasource.aid
        data['uid']=datasource.uid
        data['datasourcename']=datasource.datasourcename
        if pids_flag:
            pids=cassapidatapoint.get_datapoints_pids(did=did)
            data['pids']=[pid for pid in pids] if pids else []
        widget=cassapiwidget.get_widget_ds(did=did)
        if widget:
            data['wid']=widget.wid
        return data
    else:
        raise exceptions.DatasourceNotFoundException(error=Errors.E_GDA_GDC_DNF)

def get_datasources_config(uid):
    if not args.is_valid_uuid(uid):
        raise exceptions.BadParametersException(error=Errors.E_GDA_GDSC_IU)
    user=cassapiuser.get_user(uid=uid)
    if not user:
        raise exceptions.UserNotFoundException(error=Errors.E_GDA_GDSC_UNF)
    else:
        datasources=cassapidatasource.get_datasources(uid=uid)
        data=[]
        if datasources:
            for datasource in datasources:
                data.append({'did':datasource.did,'aid':datasource.aid,'datasourcename':datasource.datasourcename})
        return data

def update_datasource_config(did,datasourcename):
    if not args.is_valid_uuid(did):
        raise exceptions.BadParametersException(error=Errors.E_GDA_UDS_ID)
    if not args.is_valid_datasourcename(datasourcename):
        raise exceptions.BadParametersException(error=Errors.E_GDA_UDS_IDN)
    datasource=cassapidatasource.get_datasource(did=did)
    if datasource:
        datasource.datasourcename=datasourcename
        if cassapidatasource.insert_datasource(datasource=datasource):
            return True
        else:
            raise exceptions.DatasourceUpdateException(error=Errors.E_GDA_UDS_IDE)
    else:
        raise exceptions.DatasourceNotFoundException(error=Errors.E_GDA_UDS_DNF)

def generate_datasource_map(did, date):
    '''
    Los pasos son los siguientes:
    - Obtenemos el contenido
    - extraemos las variables que contiene, con la informacion necesaria para ser identificadas univocamente
    - almacenamos esta informacion en bbdd 
    '''
    if not args.is_valid_uuid(did):
        raise exceptions.BadParametersException(error=Errors.E_GDA_GDM_ID)
    if not args.is_valid_date(date):
        raise exceptions.BadParametersException(error=Errors.E_GDA_GDM_IDT)
    varlist=[]
    dsdata=cassapidatasource.get_datasource_data_at(did=did, date=date)
    if dsdata:
        variables=textmanvar.get_variables_from_text(text_content=dsdata.content)
        dsmapobj=ormdatasource.DatasourceMap(did=did,date=date,content=variables.serialize(),variables=variables.get_index())
        datasource_stats=cassapidatasource.get_datasource_stats(did=did)
        try:
            if not cassapidatasource.insert_datasource_map(dsmapobj=dsmapobj):
                return False
            if not datasource_stats or not datasource_stats.last_mapped or timeuuid.get_unix_timestamp(datasource_stats.last_mapped)<timeuuid.get_unix_timestamp(date):
                cassapidatasource.set_last_mapped(did=did, last_mapped=date)
            return True
        except Exception as e:
            #rollback
            cassapidatasource.delete_datasource_map(did=did, date=date)
            return False
    else:
        raise exceptions.DatasourceDataNotFoundException(error=Errors.E_GDA_GDM_DDNF)

def generate_datasource_text_summary(did, date):
    if not args.is_valid_uuid(did):
        raise exceptions.BadParametersException(error=Errors.E_GDA_GDTS_ID)
    if not args.is_valid_date(date):
        raise exceptions.BadParametersException(error=Errors.E_GDA_GDTS_IDT)
    dsdata=cassapidatasource.get_datasource_data_at(did=did, date=date)
    if dsdata:
        summary=textmansummary.get_summary_from_text(text=dsdata.content)
        obj=ormdatasource.DatasourceTextSummary(did=did,date=date,content_length=summary.content_length, num_lines=summary.num_lines, num_words=summary.num_words, word_frecuency=summary.word_frecuency)
        if cassapidatasource.insert_datasource_text_summary(dstextsummaryobj=obj):
            return True
        return False
    else:
        raise exceptions.DatasourceDataNotFoundException(error=Errors.E_GDA_GDTS_DDNF)

def generate_datasource_novelty_detector_for_datapoint(pid):
    if not args.is_valid_uuid(pid):
        raise exceptions.BadParametersException(error=Errors.E_GDA_GDNDFD_IP)
    datapoint=cassapidatapoint.get_datapoint(pid=pid)
    if not datapoint:
        raise exceptions.DatapointNotFoundException(error=Errors.E_GDA_GDNDFD_DNF)
    inline_dates=[]
    for sample in cassapidatapoint.get_datapoint_dtree_positives(pid=pid):
        inline_dates.append(sample.date)
    init_date=timeuuid.uuid1(seconds=1)
    end_date=timeuuid.uuid1()
    count=1000
    for reg in cassapidatapoint.get_datapoint_data(pid=pid, fromdate=init_date, todate=end_date, count=count):
        inline_dates.append(reg['date'])
    inline_dates=sorted(list(set(inline_dates)))
    if len(inline_dates)==0:
        raise exceptions.DatasourceDataNotFoundException(error=Errors.E_GDA_GDNDFD_DSDNF)
    samples=[]
    for date in inline_dates:
        textsumm=cassapidatasource.get_datasource_text_summary(did=datapoint.did, date=date)
        if textsumm:
            samples.append(textsumm.word_frecuency)
    nd=svmapi.generate_novelty_detector_for_datasource(samples=samples)
    if not nd:
        raise exceptions.DatasourceNoveltyDetectorException(error=Errors.E_GDA_GDNDFD_NDF)
    datasource_novelty_detector=ormdatasource.DatasourceNoveltyDetector(did=datapoint.did, pid=pid, date=timeuuid.uuid1(), nd=pickle.dumps(nd.novelty_detector), features=nd.features)
    return cassapidatasource.insert_datasource_novelty_detector_for_datapoint(obj=datasource_novelty_detector)

def should_datapoint_appear_in_sample(pid, date):
    if not args.is_valid_uuid(pid):
        raise exceptions.BadParametersException(error=Errors.E_GDA_SDAIS_IP)
    if not args.is_valid_date(date):
        raise exceptions.BadParametersException(error=Errors.E_GDA_SDAIS_IDT)
    datapoint=cassapidatapoint.get_datapoint(pid=pid)
    if not datapoint:
        raise exceptions.DatapointNotFoundException(error=Errors.E_GDA_SDAIS_DNF)
    #obtenemos las caracteristicas de los datasources en los que aparece el datapoint, si no lo calculamos
    ds_nd=cassapidatasource.get_last_datasource_novelty_detector_for_datapoint(did=datapoint.did,pid=pid)
    if not ds_nd:
        generate_datasource_novelty_detector_for_datapoint(pid=pid)
        ds_nd=cassapidatasource.get_last_datasource_novelty_detector_for_datapoint(did=datapoint.did,pid=pid)
        if not ds_nd:
            raise exceptions.DatasourceNoveltyDetectorException(error=Errors.E_GDA_SDAIS_DSNDNF)
    #una vez obtenido, obtenemos el summary de la muestra en cuestion, si no existe la calculamos
    ds_summary=cassapidatasource.get_datasource_text_summary(did=datapoint.did, date=date)
    if not ds_summary:
        generate_datasource_text_summary(did=datapoint.did, date=date)
        ds_summary=cassapidatasource.get_datasource_text_summary(did=datapoint.did, date=date)
        if not ds_summary:
            raise exceptions.DatasourceTextSummaryException(error=Errors.E_GDA_SDAIS_DSTSNF)
    #una vez obtenidos ambos, los comparamos y si el resultado es muy diferente devolvemos false. Si el resultado es similar, devolvemos True
    nd=pickle.loads(ds_nd.nd)
    sample_values=[]
    for feature in ds_nd.features:
        sample_values.append(ds_summary.word_frecuency[feature]) if feature in ds_summary.word_frecuency else sample_values.append(0)
    result=svmapi.is_row_novel(novelty_detector=nd, row=sample_values)
    return True if result is not None and result[0]>0 else False

def classify_missing_datapoints_in_sample(did, date):
    if not args.is_valid_uuid(did):
        raise exceptions.BadParametersException(error=Errors.E_GDA_CMDIS_ID)
    if not args.is_valid_date(date):
        raise exceptions.BadParametersException(error=Errors.E_GDA_CMDIS_IDT)
    ds_map=cassapidatasource.get_datasource_map(did=did, date=date)
    if not ds_map:
        raise exceptions.DatasourceMapNotFoundException(error=Errors.E_GDA_CMDIS_DSMNF)
    variable_list=textmanvar.get_variables_from_serialized_list(serialization=ds_map.content)
    ds_summary=cassapidatasource.get_datasource_text_summary(did=did, date=date)
    if not ds_summary:
        generate_datasource_text_summary(did=did, date=date)
        ds_summary=cassapidatasource.get_datasource_text_summary(did=did, date=date)
        if not ds_summary:
            raise exceptions.DatasourceTextSummaryException(error=Errors.E_GDA_CMDIS_DSTSNF)
    ds_pids=cassapidatapoint.get_datapoints_pids(did=did)
    pids_to_classify=set(ds_pids)-set(ds_map.datapoints.keys())
    response={'doubts':[],'discarded':[]}
    for pid in pids_to_classify:
        ds_nd=cassapidatasource.get_last_datasource_novelty_detector_for_datapoint(did=did,pid=pid)
        if not ds_nd:
            generate_datasource_novelty_detector_for_datapoint(pid=pid)
            ds_nd=cassapidatasource.get_last_datasource_novelty_detector_for_datapoint(did=did,pid=pid)
            if not ds_nd:
                response['doubts'].append(pid)
                continue
        nd=pickle.loads(ds_nd.nd)
        sample_values=[]
        for feature in ds_nd.features:
            sample_values.append(ds_summary.word_frecuency[feature]) if feature in ds_summary.word_frecuency else sample_values.append(0)
        result=svmapi.is_row_novel(novelty_detector=nd, row=sample_values)
        if result is None or result[0]<0:
            response['discarded'].append(pid)
            continue
        datapoint_stats=cassapidatapoint.get_datapoint_stats(pid=pid)
        if not datapoint_stats or not datapoint_stats.dtree_inv:
            response['doubts'].append(pid)
            continue
        dtree_inv=dtreeapi.get_decision_tree_from_serialized_data(serialization=datapoint_stats.dtree_inv)
        doubt=False
        for var in variable_list:
            if not var.position in ds_map.datapoints.values():
                if not dtree_inv.evaluate_row(var.hash_sequence):
                    doubt=True
                    break
        response['doubts'].append(pid) if doubt else response['discarded'].append(pid)
    return response

