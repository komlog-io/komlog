'''
graphs.py: library for managing graphs operations

This file implements the logic of different graphs operations at a service level.
At this point, authorization and autentication has been passed

creation date: 2013/08/07
author: jcazor
'''

import uuid
import json
import os
import os.path
import random
from datetime import datetime
from komcass import api as cassapi
from komlibs.gestaccount import states,types,exceptions
from komimc import messages
from komlibs.ifaceops import operations
from komlibs.general import colors

def create_graph(username,graphname,pid,datapointname,session,msgbus):
    now=datetime.utcnow()
    useruidr=cassapi.get_useruidrelation(username,session)
    if not useruidr:
        raise exceptions.UserNotFoundException()
    uid=useruidr.uid
    gid=uuid.uuid4()
    dtpinfo=cassapi.get_dtpinfo(pid,{},session)
    if not dtpinfo:
        raise exceptions.DatapointNotFoundException()
    graphinfo=cassapi.GraphInfo(gid,uid,graphname)
    if not dtpinfo.dbcols.has_key('default_color'):
        dtpinfo.dbcols['default_color']=colors.get_randomcolor()
        cassapi.update_dtp(dtpinfo,session)
    datapointcolor=dtpinfo.dbcols['default_color']
    datapointname=dtpinfo.dbcols['name']
    graphinfo.add_datapoint(pid,datapointcolor,datapointname)
    message=messages.UpdateGraphWeightMessage(gid=gid)
    if cassapi.create_graph(graphinfo,session):
        msgbus.sendMessage(message)
        ''' Before returning, send quote and resource authorization message '''
        operation=operations.NewGraphOperation(uid=uid,gid=gid)
        message=messages.UpdateQuotesMessage(operation=operation)
        msgbus.sendMessage(message)
        message=messages.ResourceAuthorizationUpdateMessage(operation=operation)
        msgbus.sendMessage(message)
        return {'gid':str(gid)}
    else:
        raise exceptions.GraphCreationException()

def get_graphconfig(gid,session):
    graphinfo=cassapi.get_graphinfo(gid,session)
    if not graphinfo:
        raise exceptions.GraphNotFoundException()
    data={}
    data['gid']=str(graphinfo.gid)
    data['graph_name']=graphinfo.name
    data['datapoints']={}
    datapoints=graphinfo.get_datapoints()
    if datapoints:
        for datapoint in datapoints:
            datapoint_info=graphinfo.get_datapoint_info(datapoint)
            data['datapoints'][str(datapoint)]=datapoint_info
    graphdsw=cassapi.get_graphdatasourceweight(gid,session)
    if graphdsw:
        data['graph_ds']=[]
        for did,weight in graphdsw.dids.items():
            data['graph_ds'].append((str(did),weight))
    return data

def update_graph_configuration(gid, session, data):
    if not data:
        raise exceptions.BadParametersException()
    graphinfo=cassapi.get_graphinfo(gid,session)
    if not graphinfo:
        raise exceptions.GraphNotFoundException()
    for key in data.keys():
        if key not in ('graph_name','datapoints'):
            raise exceptions.BadParametersException()
    if data.has_key('graph_name'):
        graphinfo.name=data['graph_name']
    if data.has_key('datapoints'):
        graphdatapoints=graphinfo.get_datapoints()
        for datapoint in data['datapoints']:
            try:
                uuid_datapoint=uuid.UUID(datapoint)
            except Exception:
                raise exceptions.BadParametersException()
            if uuid_datapoint in graphdatapoints:
                datapointinfo=graphinfo.get_datapoint_info(uuid_datapoint)
                for attribute in data['datapoints'][datapoint].keys():
                    if attribute=='name':
                        datapointinfo[attribute]=data['datapoints'][datapoint][attribute]
                    elif attribute=='color':
                        if colors.validate_hexcolor(data['datapoints'][datapoint][attribute]):
                            datapointinfo[attribute]=data['datapoints'][datapoint][attribute]
                        else:
                            raise exceptions.BadParametersException()
                    else:
                        raise exceptions.BadParametersException()
                graphinfo.add_datapoint(uuid_datapoint,datapointinfo['color'],datapointinfo['name'])
            else:
                raise exceptions.BadParametersException()
    if cassapi.update_graphinfo(graphinfo,session):
        return True
    else:
        raise exceptions.GraphUpdateException()

def get_plotimage(username, session, msgbus, gid):
    ruta='/var/local/komlog/plots'
    plot=str(gid)+'.png'
    if os.path.isfile(os.path.join(ruta,plot)):
        return open(os.path.join(ruta,plot),'rb').read()


def add_datapoint_to_existing_graph(username, gid, pid, session, msgbus):
    useruidr=cassapi.get_useruidrelation(username,session)
    if not useruidr:
        raise exceptions.UserNotFoundException()
    uid=useruidr.uid
    graphinfo=cassapi.get_graphinfo(gid,session)
    dtpinfo=cassapi.get_dtpinfo(pid,{},session)
    if not graphinfo:
        raise exceptions.GraphNotFoundException()
    if not dtpinfo:
        raise exceptions.DatapointNotFoundException()
    if not dtpinfo.dbcols.has_key('default_color'):
        dtpinfo.dbcols['default_color']=colors.get_randomcolor()
        cassapi.update_dtp(dtpinfo,session)
    datapointcolor=dtpinfo.dbcols['default_color']
    datapointname=dtpinfo.dbcols['name']
    graphinfo.add_datapoint(pid,datapointcolor,datapointname)
    message=messages.UpdateGraphWeightMessage(gid=gid)
    if cassapi.create_graph(graphinfo,session):
        msgbus.sendMessage(message)
        ''' Before returning, send quote and resource authorization message '''
        operation=operations.NewGraphOperation(uid=uid,gid=gid)
        message=messages.UpdateQuotesMessage(operation=operation)
        msgbus.sendMessage(message)
        message=messages.ResourceAuthorizationUpdateMessage(operation=operation)
        msgbus.sendMessage(message)
        return {'gid':str(gid)}
    else:
        raise exceptions.GraphCreationException()

