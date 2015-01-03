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
from komcass.model.orm import datasource as ormdatasource
from komfs import api as fsapi
from komlibs.gestaccount.datasource import states
from komlibs.gestaccount import exceptions
from komlibs.gestaccount.widget import api as gestwidget
from komlibs.general.validation import arguments
from komlibs.general.time import timeuuid

def create_datasource(username,aid,datasourcename):
    if not arguments.is_valid_username(username) or not arguments.is_valid_uuid(aid) or not arguments.is_valid_datasourcename(datasourcename):
        raise exceptions.BadParametersException()
    now=timeuuid.uuid1()
    did=uuid.uuid4()
    user=cassapiuser.get_user(username=username)
    agent=cassapiagent.get_agent(aid=aid)
    if not user:
        raise exceptions.UserNotFoundException()
    if not agent:
        raise exceptions.AgentNotFoundException()
    datasource=ormdatasource.Datasource(did=did,aid=aid,uid=user.uid,datasourcename=datasourcename,state=states.ACTIVE,creation_date=now)
    if cassapidatasource.new_datasource(datasource=datasource):
        return datasource
    else:
        raise exceptions.DatasourceCreationException()

def get_last_processed_datasource_data(did):
    if not arguments.is_valid_uuid(did):
        raise exceptions.BadParametersException()
    datasource_stats=cassapidatasource.get_datasource_stats(did=did)
    if datasource_stats and datasource_stats.last_mapped:
        last_mapped=datasource_stats.last_mapped
        datasource_data=cassapidatasource.get_datasource_data_at(did=did,date=last_mapped)
        if not datasource_data or not datasource_data.content:
            raise exceptions.DatasourceNotFoundException()
        dsvars=cassapidatasource.get_datasource_map_variables(did=did,date=last_mapped)
        # REVISAR SI ANTES SE DEVOLVIA UNA LISTA DE TUPLAS Y AHORA UN DICT
        datasource_datapoints=cassapidatasource.get_datasource_map_datapoints(did=did, date=last_mapped)
        dsdtps=[]
        if datasource_datapoints:
            for pid,pos in datasource_datapoints.items():
                dsdtps.append({'pid':str(pid),'id':str(pos)})
        data={}
        data['did']=str(did)
        data['ds_date']=timeuuid.get_unix_timestamp(last_mapped)
        data['ds_seq']=datasource_data.get_sequence()
        data['ds_vars']=[(pos,length) for pos,length in dsvars.items()] if dsvars else None
        data['ds_content']=datasource_data.content
        data['ds_dtps']=dsdtps
        return data
    else:
        raise exceptions.DatasourceNotFoundException()

def upload_datasource_data(did,content,dest_dir):
    if not arguments.is_valid_uuid(did) or not arguments.is_valid_datasource_content(content):
        raise exceptions.BadParametersException()
    datasource=cassapidatasource.get_datasource(did=did)
    if datasource:
        hex_now=timeuuid.uuid1().hex
        hex_did=did.hex
        filedata={}
        filedata['received']=hex_now
        filedata['did']=hex_did
        filedata['json_content']=content
        json_filedata=json.dumps(filedata)
        filename=hex_now+'_'+hex_did+'.pspl'
        destfile=os.path.join(dest_dir,filename)
        if fsapi.create_sample(destfile,json_filedata):
            return destfile
        else:
            logger.logger.debug('failed')
            raise exceptions.DatasourceUploadContentException()
    else:
        raise exceptions.DatasourceNotFoundException()

def get_datasource_config(did):
    if not arguments.is_valid_uuid(did):
        raise exceptions.BadParametersException()
    datasource=cassapidatasource.get_datasource(did=did)
    if datasource:
        data={}
        data['did']=str(did)
        data['aid']=str(datasource.aid)
        data['name']=datasource.datasourcename
        return data
    else:
        raise exceptions.DatasourceNotFoundException()

def get_datasources_config(username):
    if not arguments.is_valid_username(username):
        raise exceptions.BadParametersException()
    user=cassapiuser.get_user(username=username)
    if not user:
        raise exceptions.UserNotFoundException()
    else:
        datasources=cassapidatasource.get_datasources(uid=user.uid)
        data=[]
        if datasources:
            for datasource in datasources:
                data.append({'did':str(datasource.did),'aid':str(datasource.aid),'name':datasource.datasourcename})
        return data

def update_datasource_config(did,data):
    if not arguments.is_valid_uuid(did) or not arguments.is_valid_dict(data):
        raise exceptions.BadParametersException()
    if not 'ds_name' in data or not arguments.is_valid_datasourcename(data['ds_name']):
        raise exceptions.BadParametersException()
    datasource=cassapidatasource.get_datasource(did=did)
    if datasource:
        datasource.datasourcename=data['ds_name']
        if cassapidatasource.insert_datasource(datasource=datasource):
            return True
        else:
            raise exceptions.DatasourceUpdateException()
    else:
        raise exceptions.DatasourceNotFoundException()
        
