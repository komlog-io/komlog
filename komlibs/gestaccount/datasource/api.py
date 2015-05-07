#coding: utf-8
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
from komfig import logger
from komcass.api import user as cassapiuser
from komcass.api import agent as cassapiagent
from komcass.api import datasource as cassapidatasource
from komcass.api import datapoint as cassapidatapoint
from komcass.api import widget as cassapiwidget
from komcass.api import dashboard as cassapidashboard
from komcass.model.orm import datasource as ormdatasource
from komfs import api as fsapi
from komlibs.gestaccount.datasource import states
from komlibs.gestaccount import exceptions, errors
from komlibs.general.validation import arguments as args
from komlibs.general.time import timeuuid
from komlibs.textman import api as textmanapi

def create_datasource(uid,aid,datasourcename):
    if not args.is_valid_uuid(uid):
        raise exceptions.BadParametersException(error=errors.E_GDA_CRD_IU)
    if not args.is_valid_uuid(aid):
        raise exceptions.BadParametersException(error=errors.E_GDA_CRD_IA)
    if not args.is_valid_datasourcename(datasourcename):
        raise exceptions.BadParametersException(error=errors.E_GDA_CRD_IDN)
    now=timeuuid.uuid1()
    did=uuid.uuid4()
    user=cassapiuser.get_user(uid=uid)
    agent=cassapiagent.get_agent(aid=aid)
    if not user:
        raise exceptions.UserNotFoundException(error=errors.E_GDA_CRD_UNF)
    if not agent:
        raise exceptions.AgentNotFoundException(error=errors.E_GDA_CRD_ANF)
    datasource=ormdatasource.Datasource(did=did,aid=aid,uid=uid,datasourcename=datasourcename,state=states.ACTIVE,creation_date=now)
    if cassapidatasource.new_datasource(datasource=datasource):
        return {'did':datasource.did, 'datasourcename':datasource.datasourcename, 'uid': datasource.uid, 'aid':datasource.aid, 'state':datasource.state}
    else:
        raise exceptions.DatasourceCreationException(error=errors.E_GDA_CRD_IDE)

def get_last_processed_datasource_data(did):
    if not args.is_valid_uuid(did):
        raise exceptions.BadParametersException(error=errors.E_GDA_GLPD_ID)
    datasource_stats=cassapidatasource.get_datasource_stats(did=did)
    if datasource_stats and datasource_stats.last_mapped:
        last_mapped=datasource_stats.last_mapped
        datasource_data=cassapidatasource.get_datasource_data_at(did=did,date=last_mapped)
        if not datasource_data or not datasource_data.content:
            raise exceptions.DatasourceDataNotFoundException(error=errors.E_GDA_GLPD_DDNF)
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
        raise exceptions.DatasourceNotFoundException(error=errors.E_GDA_GLPD_DNF)

def upload_datasource_data(did,content,dest_dir):
    if not args.is_valid_uuid(did):
        raise exceptions.BadParametersException(error=errors.E_GDA_UDD_ID)
    if not args.is_valid_datasource_content(content):
        raise exceptions.BadParametersException(error=errors.E_GDA_UDD_IDC)
    if not args.is_valid_string(dest_dir):
        raise exceptions.BadParametersException(error=errors.E_GDA_UDD_IDD)
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
            raise exceptions.BadParametersException(error=errors.E_GDA_UDD_IFD)
        filename=now.hex+'_'+did.hex+'.pspl'
        destfile=os.path.join(dest_dir,filename)
        if fsapi.create_sample(destfile,json_filedata):
            return destfile
        else:
            logger.logger.debug('Could not store datasource content on disk: '+str(destfile))
            raise exceptions.DatasourceUploadContentException(error=errors.E_GDA_UDD_ESD)
    else:
        raise exceptions.DatasourceNotFoundException(error=errors.E_GDA_UDD_DNF)

def get_datasource_data(did, date):
    if not args.is_valid_uuid(did):
        raise exceptions.BadParametersException(error=errors.E_GDA_GDD_ID)
    if not args.is_valid_date(date):
        raise exceptions.BadParametersException(error=errors.E_GDA_GDD_IDT)
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
        raise exceptions.DatasourceDataNotFoundException(error=errors.E_GDA_GDD_DDNF)

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
        raise exceptions.BadParametersException(error=errors.E_GDA_GDC_ID)
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
        raise exceptions.DatasourceNotFoundException(error=errors.E_GDA_GDC_DNF)

def get_datasources_config(uid):
    if not args.is_valid_uuid(uid):
        raise exceptions.BadParametersException(error=errors.E_GDA_GDSC_IU)
    user=cassapiuser.get_user(uid=uid)
    if not user:
        raise exceptions.UserNotFoundException(error=errors.E_GDA_GDSC_UNF)
    else:
        datasources=cassapidatasource.get_datasources(uid=uid)
        data=[]
        if datasources:
            for datasource in datasources:
                data.append({'did':datasource.did,'aid':datasource.aid,'datasourcename':datasource.datasourcename})
        return data

def update_datasource_config(did,datasourcename):
    if not args.is_valid_uuid(did):
        raise exceptions.BadParametersException(error=errors.E_GDA_UDS_ID)
    if not args.is_valid_datasourcename(datasourcename):
        raise exceptions.BadParametersException(error=errors.E_GDA_UDS_IDN)
    datasource=cassapidatasource.get_datasource(did=did)
    if datasource:
        datasource.datasourcename=datasourcename
        if cassapidatasource.insert_datasource(datasource=datasource):
            return True
        else:
            raise exceptions.DatasourceUpdateException(error=errors.E_GDA_UDS_IDE)
    else:
        raise exceptions.DatasourceNotFoundException(error=errors.E_GDA_UDS_DNF)

def generate_datasource_map(did, date):
    '''
    Los pasos son los siguientes:
    - Obtenemos el contenido
    - extraemos las variables que contiene, con la informacion necesaria para ser identificadas univocamente
    - almacenamos esta informacion en bbdd 
    '''
    if not args.is_valid_uuid(did):
        raise exceptions.BadParametersException(error=errors.E_GDA_GDM_ID)
    if not args.is_valid_date(date):
        raise exceptions.BadParametersException(error=errors.E_GDA_GDM_IDT)
    varlist=[]
    dsdata=cassapidatasource.get_datasource_data_at(did=did, date=date)
    if dsdata:
        variables=textmanapi.get_variables_from_text(text_content=dsdata.content)
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
            logger.logger.exception('Exception creating Map for did '+str(did)+': '+str(e))
            cassapidatasource.delete_datasource_map(did=did, date=date)
            return False
    else:
        logger.logger.error('Datasource data not found: '+str(did)+' '+str(date))
        raise exceptions.DatasourceDataNotFoundException(error=errors.E_GDA_GDM_DDNF)

def delete_datasource(did):
    if not args.is_valid_uuid(did):
        raise exceptions.BadParametersException(error=errors.E_GDA_DD_ID)
    datasource=cassapidatasource.get_datasource(did=did)
    if not datasource:
        raise exceptions.DatasourceNotFoundException(error=errors.E_GDA_DD_DNF)
    bids=cassapidashboard.get_dashboards_bids(uid=datasource.uid)
    wids=[]
    pids=cassapidatapoint.get_datapoints_pids(did=did)
    for pid in pids:
        dp_wid=cassapiwidget.get_widget_dp(pid=pid)
        if dp_wid:
            wids.append(dp_wid.wid)
    ds_wid=cassapiwidget.get_widget_ds(did=did)
    if ds_wid:
        wids.append(ds_wid.wid)
    for bid in bids:
        for wid in wids:
            cassapidashboard.delete_widget_from_dashboard(wid=wid, bid=bid)
    for wid in wids:
        cassapiwidget.delete_widget(wid=wid)
    for pid in pids:
        cassapidatapoint.delete_datapoint(pid=pid)
        cassapidatapoint.delete_datapoint_stats(pid=pid)
        cassapidatapoint.delete_datapoint_data(pid=pid)
    cassapidatasource.delete_datasource(did=datasource.did)
    cassapidatasource.delete_datasource_stats(did=datasource.did)
    cassapidatasource.delete_datasource_data(did=datasource.did)
    cassapidatasource.delete_datasource_maps(did=datasource.did)
    return True

