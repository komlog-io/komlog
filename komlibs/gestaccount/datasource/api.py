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
from datetime import datetime
from komcass.api import user as cassapiuser
from komcass.api import agent as cassapiagent
from komcass.api import datasource as cassapidatasource
from komcass.model.orm import datasource as ormdatasource
from komfs import api as fsapi
from komlibs.gestaccount.datasource import states
from komlibs.gestaccount import exceptions
from komlibs.gestaccount.widget import api as gestwidget
from komlibs.general.validation import arguments

def create_datasource(username,aid,datasourcename):
    if not arguments.is_valid_username(username) or not arguments.is_valid_uuid(aid) or not arguments.is_valid_datasourcename(datasourcename):
        raise exceptions.BadParametersException()
    now=datetime.utcnow()
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

def get_datasource_data(did,date=None):
    if not arguments.is_valid_uuid(did):
        raise exceptions.BadParametersException()
    logger.logger.debug('getting datasource data of '+str(did))
    datasource_stats=cassapidatasource.get_datasource_stats(did=did)
    if datasource_stats:
        data={}
        last_mapped=datasource_stats.last_mapped
        logger.logger.debug('last mapped: '+str(last_mapped))
        last_received=date if date else datasource_stats.last_received
        logger.logger.debug('last received: '+str(last_received))
        datasource_data=cassapidatasource.get_datasource_data_at(did=did,date=last_received)
        dsvars={}
        dsdtps=[]
        if last_mapped>=last_received:
            logger.logger.debug('getting mapped data')
            dsvars=cassapidatasource.get_datasource_map_variables(did=did,date=last_received)
            logger.logger.debug('Datasource vars: '+str(dsvars))
            # REVISAR SI ANTES SE DEVOLVIA UNA LISTA DE TUPLAS Y AHORA UN DICT
            datasource_datapoints=cassapidatasource.get_datasource_map_datapoints(did=did, date=last_received)
            if datasource_datapoints:
                logger.logger.debug('Datasource datapoints: '+str(datasource_datapoints))
                for pid,pos in datasource_datapoints.items():
                    dsdtps.append({'pid':str(pid),'id':str(pos)})
        data['did']=str(did)
        data['ds_date']=last_received.isoformat()+'Z'
        data['ds_vars']=[(pos,length) for pos,length in dsvars.items()] if dsvars else None
        data['ds_content']=datasource_data.content
        data['ds_dtps']=dsdtps
        return data
    else:
        raise exceptions.DatasourceNotFoundException()

def upload_datasource_data(did,content,dest_dir):
    if not arguments.is_valid_uuid(did) or not arguments.is_valid_datasource_content(content):
        raise exceptions.BadParametersException()
    logger.logger.debug('upload_content Init')
    datasource=cassapidatasource.get_datasource(did=did)
    if datasource:
        logger.logger.debug('Datasource Exists')
        now=datetime.utcnow().isoformat()
        filedata={}
        filedata['received']=now
        filedata['did']=str(did)
        logger.logger.debug('json_content')
        filedata['json_content']=content
        logger.logger.debug('preparing file content')
        json_filedata=json.dumps(filedata)
        logger.logger.debug('generating filename')
        filename=now+'_'+str(did)+'.pspl'
        destfile=os.path.join(dest_dir,filename)
        logger.logger.debug('storing file on disk')
        if fsapi.create_sample(destfile,json_filedata):
            logger.logger.debug('success')
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
        
