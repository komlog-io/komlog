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
from datetime import datetime
from komcass.api import user as cassapiuser
from komcass.api import agent as cassapiagent
from komcass.api import datasource as cassapidatasource
from komcass.model.orm import datasource as ormdatasource
from komfs import api as fsapi
from komlibs.gestaccount import states,types,exceptions
from komlibs.gestaccount import widget as gestwidget
from komlibs.ifaceops import operations
from komimc import messages
from komlibs.general import crontab

def create_datasource(username,aid,datasourcename,msgbus):
    print 'llegamos al create datasource'
    now=datetime.utcnow()
    did=uuid.uuid4()
    user=cassapiuser.get_user(username=username)
    agent=cassapiagent.get_agent(aid=aid)
    if not user:
        raise exceptions.UserNotFoundException()
    if not agent:
        raise exceptions.AgentNotFoundException()
    print 'antes de create el objeto datasource'
    datasource=ormdatasource.Datasource(did=did,aid=aid,uid=user.uid,datasourcename=datasourcename,state=states.DATASOURCE['ACTIVE'],creation_date=now)
    print 'antes de lanzar el insert'
    if cassapidatasource.new_datasource(datasource=datasource):
        print 'insert correcto'
        ''' before returning, send quote and resource authorization message '''
        operation=operations.NewDatasourceOperation(uid=user.uid,aid=aid,did=did)
        message=messages.UpdateQuotesMessage(operation=operation)
        msgbus.sendMessage(message)
        message=messages.ResourceAuthorizationUpdateMessage(operation=operation)
        msgbus.sendMessage(message)
        ''' create related widget every time a new datasource is created '''
        gestwidget.new_widget_ds(username=username,did=did,msgbus=msgbus)
        return {'did':str(did)}
    else:
        raise exceptions.DatasourceCreationException()

def get_datasource_data(did,date=None):
    datasource_stats=cassapidatasource.get_datasource_stats(did=did)
    if datasource_stats:
        data={}
        last_mapped=datasource_stats.last_mapped
        last_received=date if date else datasource_stats.last_received
        datasource_data=cassapidatasource.get_datasource_data(did=did,date=last_received)
        dsvars=[]
        dsdtps=[]
        if last_mapped>=last_received:
            dsvars=cassapidatasource.get_datasource_map_variables(did=did,date=last_received)
            #Con el nuevo model de datos, las dos lineas siguientes no deben hacer falta
            #if datasource_variables:
            #    dsvars=json.loads(dsmapvars.content)
            # REVISAR SI ANTES SE DEVOLVIA UNA LISTA DE TUPLAS Y AHORA UN DICT
            datasource_datapoints=cassapidatasource.get_datasource_map_datapoints(did=did, date=last_received)
            if datasource_datapoints:
                #lo mismo que antes, en bbdd ya no almacenamos datos en json
                #datapoints=json.loads(dsmapdtps.jsoncontent)
                print 'lo doy aqui'
                print datasource_datapoints
                for pid,pos in datasource_datapoints.iteritems():
                    dsdtps.append({'pid':str(pid),'id':str(pos)})
                print 'aqui no llego'
        data['did']=str(did)
        data['ds_date']=last_received.isoformat()+'Z'
        data['ds_vars']=[(pos,length) for pos,length in dsvars.iteritems()]
        data['ds_content']=datasource_data.content
        data['ds_dtps']=dsdtps
        return data
    else:
        raise exceptions.DatasourceNotFoundException()

def upload_content(did,content,dest_dir):
    datasource=cassapidatasource.get_datasource(did=did)
    if datasource:
        now=datetime.utcnow().isoformat()
        filedata={}
        filedata['received']=now
        filedata['did']=str(did)
        filedata['json_content']=content
        json_filedata=json.dumps(filedata)
        filename=now+'_'+str(did)+'.pspl'
        destfile=os.path.join(dest_dir,filename)
        if fsapi.create_sample(destfile,json_filedata):
            return destfile
        else:
            raise exceptions.DatasourceUploadContentException()
    else:
        raise exceptions.DatasourceNotFoundException()

def get_datasource_config(did):
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
    datasource=cassapidatasource.get_datasource(sesion, did=did)
    if datasource:
        if data.has_key('ds_name'):
            datasource.datasourcename=data['ds_name']
        if cassapidatasource.insert_datasource(datasource=datasource):
            return True
        else:
            raise exceptions.DatasourceUpdateException()
    else:
        raise exceptions.DatasourceNotFoundException()
        
