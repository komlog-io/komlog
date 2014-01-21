#coding: utf-8
'''
datapoints.py: library for managing datapoints operations

This file implements the logic of different datapoint operations at a service level.
At this point, authorization and autentication has been passed

creation date: 2013/07/04
author: jcazor
'''

import uuid
import json
import os
import dateutil.parser
from datetime import timedelta
from komcass import api as cassapi
from komlibs.gestaccount import states,types,exceptions
from komlibs.general import colors
from komimc import messages

def get_datapointdata(pid,session,todate):
    ''' como se ha pasado por las fases de autorización y autenticación, 
    no comprobamos que el pid existe '''
    dtpdatas=cassapi.get_datapointdata(pid,session,todate=todate)
    data=[]
    if not dtpdatas:
        last_date=todate-timedelta(days=1)
        raise exceptions.DatapointDataNotFoundException(last_date=last_date)
    else:
        for dtpdata in dtpdatas:
            data.append((dtpdata.date.isoformat(),str(dtpdata.content)))
    return data

def create_datapoint(did,dsdate,pos,length,name,msgbus):
    '''
    Funcion utilizada para la monitorización de una variable y
    la creación del datapoint correspondiente
    '''
    did=uuid.UUID(did)
    dsdate=dateutil.parser.parse(dsdate)
    pos=str(pos)
    length=str(length)
    name=u''+name
    message=messages.MonitorVariableMessage(did=did,date=dsdate,pos=pos,length=length,name=name)
    msgbus.sendMessage(message)
    return True

def get_datapointconfig(pid,session):
    ''' como se ha pasado por las fases de autorización y autenticación, 
    no comprobamos que el pid existe '''
    dtpinfo=cassapi.get_dtpinfo(pid,{'did':'','name':'','decimalseparator':'','default_color':''},session)
    data={}
    data['pid']=str(pid)
    if dtpinfo:
        for key in ('name','did','decimalseparator','default_color'):
            try:
                data[key]=dtpinfo.dbcols[key]
            except KeyError:
                pass
    else:
        raise exceptions.DatapointNotFoundException()
    return data

def update_datapointconfig(pid,session,data):
    dtpinfo=cassapi.get_dtpinfo(pid,{},session)
    if dtpinfo:
        if data.has_key('name'):
            dtpinfo.dbcols['name']=u''+data['name']
        if data.has_key('default_color'):
            if colors.validate_hexcolor(data['default_color']):
                dtpinfo.dbcols['default_color']=u''+data['default_color']
            else:
                raise exceptions.BadParametersException()
        if cassapi.update_dtp(dtpinfo,session):
            return True
        else:
            raise exceptions.DatapointUpdateException()
    else:
        raise exceptions.DatapointNotFoundException()
        
