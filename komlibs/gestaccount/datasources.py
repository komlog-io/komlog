'''
datasources.py: library for managing datasource operations

This file implements the logic of different datasource operations at a service level.
At this point, authorization and autentication has been passed

creation date: 2013/03/31
author: jcazor
'''

import uuid
import json
import os
from datetime import datetime
from komcass import api as cassapi
from komfs import api as fsapi
from komlibs.gestaccount import states,types,exceptions

def create_datasource(username,aid,dsname,dstype,dsparams,session):
    now=datetime.utcnow()
    did=uuid.uuid4()
    kwargs={}
    try:
        for dbkey,webkey in types.DSPARAMS_WEB2DB[types.DS_STR2INT[dstype]]:
            kwargs[dbkey]=dsparams[webkey]
        dstype=types.DS_STR2INT[dstype]
    except Exception as e:
        print str(e)
        raise exceptions.BadParametersException()
    useruidr=cassapi.get_useruidrelation(username,session)
    if not useruidr:
        raise exceptions.UserNotFoundException()
    uid=useruidr.uid
    uidagentr=cassapi.get_useragentrelation(uid,session)
    if not uidagentr:
        raise exceptions.AgentNotFoundException()
    try:
        index=uidagentr.aids.index(aid)
    except ValueError:
        raise exceptions.AgentNotFoundException()
    dsinfo=cassapi.DatasourceInfo(did=did,aid=aid,dsname=dsname,dstype=dstype,creation_date=now,state=states.DATASOURCE['ACTIVE'],**kwargs)
    if cassapi.register_datasource(dsinfo, session):
        return {'did':str(did)}
    else:
        raise exceptions.DatasourceCreationException()

def get_datasourcedata(did,session,date=None):
    dsinfo=cassapi.get_dsinfo(did,{'last_received':u'','last_mapped':u''},session)
    if dsinfo:
        data={}
        last_mapped=dsinfo.last_mapped
        last_received=date if date else dsinfo.last_received
        dsdata=cassapi.get_datasourcedata(did,last_received,session)
        dsvars=[]
        dsdtps={}
        if last_mapped:
            dsmapvars=cassapi.get_datasourcemapvars(did,last_received,session)
            if dsmapvars:
                dsvars=dsmapvars.content
        dsmapdtps=cassapi.get_datasourcemapdtps(did,last_received,session)
        if dsmapdtps:
            dsdtps=json.loads(dsmapdtps.jsoncontent)
        location={}
        data['did']=str(did)
        data['ds_date']=last_received.isoformat()
        data['ds_location']=location
        data['ds_vars']=dsvars
        data['ds_content']=dsdata.content
        data['ds_dtps']=dsdtps
        return data
    else:
        raise exceptions.DatasourceNotFoundException()

def upload_content(did,content,session,dest_dir):
    dsinfo=cassapi.get_dsinfo(did,{},session)
    if dsinfo:
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

def get_datasourceconfig(did,session):
    dsinfo=cassapi.get_dsinfo(did,{},session)
    if dsinfo:
        ds_name=dsinfo.dsname
        last_received=dsinfo.last_received.isoformat() if dsinfo.last_received else None
        ds_type=types.DS_INT2STR[dsinfo.dstype]
        params={}
        for webkey,dbkey in types.DSPARAMS_DB2WEB[dsinfo.dstype]:
            print webkey,dbkey
            params[webkey]=getattr(dsinfo,dbkey)
        data={}
        data['did']=str(did)
        data['ds_name']=ds_name
        data['last_received']=last_received
        data['ds_type']=ds_type
        data['ds_params']=params
        return data
    else:
        raise exceptions.DatasourceNotFoundException()

def update_datasourceconfig(did,session,data):
    dsinfo=cassapi.get_dsinfo(did,{},session)
    if dsinfo:
        for dbkey,webkey in types.DSPARAMS_WEB2DB[dsinfo.dstype]:
            setattr(dsinfo,dbdict[dbkey],data['ds_params'][webkey])
        dsinfo.dsname=data['ds_name']
        dsinfo.state=data['ds_state']
        if cassapi.update_ds(dsinfo,session):
            return dsinfo
        else:
            raise exceptions.DatasourceUpdateException()
    else:
        raise exceptions.DatasourceNotFoundException()
        
