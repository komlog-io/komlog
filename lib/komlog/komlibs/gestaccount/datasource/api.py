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
from komlog.komcass import exceptions as cassexcept
from komlog.komcass.api import user as cassapiuser
from komlog.komcass.api import agent as cassapiagent
from komlog.komcass.api import datasource as cassapidatasource
from komlog.komcass.api import datapoint as cassapidatapoint
from komlog.komcass.api import widget as cassapiwidget
from komlog.komcass.api import dashboard as cassapidashboard
from komlog.komcass.model.orm import datasource as ormdatasource
from komlog.komfs import api as fsapi
from komlog.komlibs.gestaccount import exceptions
from komlog.komlibs.gestaccount.errors import Errors
from komlog.komlibs.general.validation import arguments as args
from komlog.komlibs.general.time import timeuuid
from komlog.komlibs.textman.api import variables as textmanvar
from komlog.komlibs.textman.api import summary as textsumm
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
    if not user:
        raise exceptions.UserNotFoundException(error=Errors.E_GDA_CRD_UNF)
    agent=cassapiagent.get_agent(aid=aid)
    if not agent:
        raise exceptions.AgentNotFoundException(error=Errors.E_GDA_CRD_ANF)
    if not graphuri.new_datasource_uri(uid=uid, uri=datasourcename, did=did):
        raise exceptions.DatasourceCreationException(error=Errors.E_GDA_CRD_ADU)
    datasource=ormdatasource.Datasource(did=did,aid=aid,uid=uid,datasourcename=datasourcename,creation_date=now)
    try:
        if cassapidatasource.new_datasource(datasource=datasource):
            return {'did':datasource.did, 'datasourcename':datasource.datasourcename, 'uid': datasource.uid, 'aid':datasource.aid}
        else:
            graphuri.dissociate_vertex(ido=did)
            raise exceptions.DatasourceCreationException(error=Errors.E_GDA_CRD_IDE)
    except cassexcept.KomcassException:
        graphuri.dissociate_vertex(ido=did)
        cassapidatasource.delete_datasource(did=did)
        raise

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

def get_datasource_data(did, fromdate=None, todate=None, count=None):
    if not args.is_valid_uuid(did):
        raise exceptions.BadParametersException(error=Errors.E_GDA_GDD_ID)
    if fromdate and not args.is_valid_date(fromdate):
        raise exceptions.BadParametersException(error=Errors.E_GDA_GDD_IFD)
    if todate and not args.is_valid_date(todate):
        raise exceptions.BadParametersException(error=Errors.E_GDA_GDD_ITD)
    if count and not args.is_valid_int(count):
        raise exceptions.BadParametersException(error=Errors.E_GDA_GDD_ICNT)
    dsdata=cassapidatasource.get_datasource_data(did=did, fromdate=fromdate, todate=todate, count=count)
    if len(dsdata) == 0:
        raise exceptions.DatasourceDataNotFoundException(error=Errors.E_GDA_GDD_DDNF)
    data = []
    for item in dsdata:
        data.append({
            'date':item.date,
            'content':item.content
        })
    return data

def get_mapped_datasource_data(did, fromdate=None, todate=None, count=None):
    if not args.is_valid_uuid(did):
        raise exceptions.BadParametersException(error=Errors.E_GDA_GMDD_ID)
    if fromdate and not args.is_valid_date(fromdate):
        raise exceptions.BadParametersException(error=Errors.E_GDA_GMDD_IFD)
    if todate and not args.is_valid_date(todate):
        raise exceptions.BadParametersException(error=Errors.E_GDA_GMDD_ITD)
    if count and not args.is_valid_int(count):
        raise exceptions.BadParametersException(error=Errors.E_GDA_GMDD_ICNT)
    mdsdata=cassapidatasource.get_datasource_maps(did=did, fromdate=fromdate, todate=todate, count=count)
    data=[]
    for item in mdsdata:
        dsdata=cassapidatasource.get_datasource_data_at(did=did, date=item.date)
        if dsdata:
            data.append({
                'date':item.date,
                'content':dsdata.content,
                'variables':[(pos,length) for pos,length in item.variables.items()],
                'datapoints':[{'pid':pid, 'position':pos} for pid,pos in item.datapoints.items()]
            })
    if len(data) == 0:
        raise exceptions.DatasourceDataNotFoundException(error=Errors.E_GDA_GMDD_DDNF)
    return data

def store_datasource_data(did, date, content):
    if not args.is_valid_uuid(did) or not args.is_valid_datasource_content(content) or not args.is_valid_date(date):
        return False
    size=len(content.encode('utf-8'))
    dsdobj=ormdatasource.DatasourceData(did=did,date=date,content=content)
    metobj=ormdatasource.DatasourceMetadata(did=did, date=date, size=size)
    dsstats=None
    try:
        if cassapidatasource.insert_datasource_data(dsdobj=dsdobj):
            if cassapidatasource.insert_datasource_metadata(obj=metobj):
                dsstats=cassapidatasource.get_datasource_stats(did=did)
                if dsstats is None or dsstats.last_received is None or dsstats.last_received.time < date.time:
                    cassapidatasource.set_last_received(did=did, last_received=date)
                return True
            else:
                cassapidatasource.delete_datasource_data_at(did=did, date=date)
                return False
        else:
            return False
    except cassexcept.KomcassException:
        cassapidatasource.delete_datasource_data_at(did=did, date=date)
        cassapidatasource.delete_datasource_metadata_at(did=did, date=date)
        if dsstats is None:
            cassapidatasource.delete_datasource_stats(did=did)
        else:
            cassapidatasource.set_last_received(did=did, last_received=dsstats.last_received)
        raise

def get_datasource_config(did, pids_flag=True, widget_flag=True):
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
        if widget_flag:
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
        new_datasource=datasource
        new_datasource.datasourcename=datasourcename
        try:
            if cassapidatasource.insert_datasource(datasource=new_datasource):
                return True
            else:
                raise exceptions.DatasourceUpdateException(error=Errors.E_GDA_UDS_IDE)
        except cassexcept.KomcassException:
            cassapidatasource.insert_datasource(datasource=datasource)
            raise
    else:
        raise exceptions.DatasourceNotFoundException(error=Errors.E_GDA_UDS_DNF)

def generate_datasource_map(did, date):
    '''
    Esta funcion identifica las variables existentes en una muestra recibida de un datasource.
    Los pasos son los siguientes:
    - Obtenemos el contenido
    - extraemos el indice de las variables que contiene
    - almacenamos esta informacion en bbdd 
    '''
    if not args.is_valid_uuid(did):
        raise exceptions.BadParametersException(error=Errors.E_GDA_GDM_ID)
    if not args.is_valid_date(date):
        raise exceptions.BadParametersException(error=Errors.E_GDA_GDM_IDT)
    dsdata=cassapidatasource.get_datasource_data_at(did=did, date=date)
    if dsdata is None:
        raise exceptions.DatasourceDataNotFoundException(error=Errors.E_GDA_GDM_DDNF)
    index=textmanvar.get_variables_index_from_text(text=dsdata.content)
    dsmapobj=ormdatasource.DatasourceMap(did=did,date=date,variables=index)
    dsstats=cassapidatasource.get_datasource_stats(did=did)
    try:
        if not cassapidatasource.insert_datasource_map(dsmapobj=dsmapobj):
            return False
        if dsstats is None or dsstats.last_mapped is None or dsstats.last_mapped.time<date.time:
            cassapidatasource.set_last_mapped(did=did, last_mapped=date)
        return True
    except cassexcept.KomcassException:
        #rollback
        cassapidatasource.delete_datasource_map(did=did, date=date)
        if dsstats is None:
            cassapidatasource.delete_datasource_stats(did=did)
        else:
            cassapidatasource.set_last_mapped(did=did, last_mapped=dsstats.last_mapped)
        raise

def hook_to_datasource(did, sid):
    if not args.is_valid_uuid(did):
        raise exceptions.BadParametersException(error=Errors.E_GDA_HTDS_IDID)
    if not args.is_valid_uuid(sid):
        raise exceptions.BadParametersException(error=Errors.E_GDA_HTDS_ISID)
    datasource=cassapidatasource.get_datasource(did=did)
    if datasource is None:
        raise exceptions.DatasourceNotFoundException(error=Errors.E_GDA_HTDS_DSNF)
    return cassapidatasource.insert_datasource_hook(did=did, sid=sid)

def unhook_from_datasource(did, sid):
    if not args.is_valid_uuid(did):
        raise exceptions.BadParametersException(error=Errors.E_GDA_UHFDS_IDID)
    if not args.is_valid_uuid(sid):
        raise exceptions.BadParametersException(error=Errors.E_GDA_UHFDS_ISID)
    return cassapidatasource.delete_datasource_hook(did=did, sid=sid)

def get_datasource_hooks(did):
    if not args.is_valid_uuid(did):
        raise exceptions.BadParametersException(error=Errors.E_GDA_GDSH_IDID)
    datasource=cassapidatasource.get_datasource(did=did)
    if datasource is None:
        raise exceptions.DatasourceNotFoundException(error=Errors.E_GDA_GDSH_DSNF)
    return cassapidatasource.get_datasource_hooks_sids(did=did)

def get_datasource_supplies(did, count=1):
    if not args.is_valid_uuid(did):
        raise exceptions.BadParametersException(error=Errors.E_GDA_GDSSUP_IDID)
    if not isinstance(count, int) or count < 1:
        raise exceptions.BadParametersException(error=Errors.E_GDA_GDSSUP_ICNT)
    supplies = set()
    ds_supplies_list = cassapidatasource.get_last_datasource_supplies_count(did, count=count)
    for item in ds_supplies_list:
        for uri in item.supplies:
            supplies.add(uri)
    return sorted(list(supplies))

def update_datasource_supplies(did, supplies):
    if not args.is_valid_uuid(did):
        raise exceptions.BadParametersException(error=Errors.E_GDA_UDSSUP_IDID)
    if not isinstance(supplies, list):
        raise exceptions.BadParametersException(error=Errors.E_GDA_UDSSUP_ISUPT)
    for item in supplies:
        if not args.is_valid_uri(item):
            raise exceptions.BadParametersException(error=Errors.E_GDA_UDSSUP_ISUPI)
    datasource=cassapidatasource.get_datasource(did=did)
    if datasource is None:
        raise exceptions.DatasourceNotFoundException(error=Errors.E_GDA_UDSSUP_DSNF)
    current = cassapidatasource.get_last_datasource_supplies_count(did, count=1)
    if current == [] or current[0].supplies != sorted(supplies):
        now = timeuuid.uuid1()
        return cassapidatasource.insert_datasource_supplies(did, now, supplies)
    else:
        return False

def classify_sample(did, date):
    if not args.is_valid_uuid(did):
        raise exceptions.BadParametersException(error=Errors.E_GDA_CLSMP_IDID)
    if not args.is_valid_date(date):
        raise exceptions.BadParametersException(error=Errors.E_GDA_CLSMP_IDT)
    dsdata=cassapidatasource.get_datasource_data_at(did=did, date=item.date)
    if dsdata == None:
        raise exceptions.DatasourceDataNotFoundException(error=Errors.E_GDA_CLSMP_DSDNF)
    features = textsumm.get_content_features([dsdata], max_features=25)
    ds_features = cassapidatasource.get_datasource_features(did=did)
    response = {'new_ds_features':False}
    for feature in features:
        if not feature in ds_features.features:
            response['new_ds_features']=True
            break
    return response

