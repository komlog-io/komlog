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
import random
from datetime import datetime
from komcass import api as cassapi
from komlibs.gestaccount import states,types,exceptions
from komimc import messages
from komlibs.ifaceops import operations

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
        dtpinfo.dbcols['default_color']=get_randomcolor()
        cassapi.update_dtp(dtpinfo,session)
    datapointcolor=dtpinfo.dbcols['default_color']
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
    print 'Entramos en graphconfig'
    graphinfo=cassapi.get_graphinfo(gid,session)
    print 'despues de graphinfo'
    if not graphinfo:
        raise exceptions.GraphNotFoundException()
    data={}
    data['gid']=str(graphinfo.gid)
    data['graph_name']=graphinfo.name
    data['datapoints']={}
    print 'llegamos a los datapoints'
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

def get_randomcolor():
    r = lambda: random.randint(0,255)
    return '#%02X%02X%02X' % (r(),r(),r())
