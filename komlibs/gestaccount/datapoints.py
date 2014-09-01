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
from datetime import timedelta, datetime
from komcass import api as cassapi
from komlibs.gestaccount import states,types,exceptions
from komlibs.general import colors
from komimc import messages

def get_datapointdata(pid,session,todate=None):
    ''' como se ha pasado por las fases de autorización y autenticación, 
    no comprobamos que el pid existe '''
    dtpdatas=cassapi.get_datapointdata(pid,session,todate=todate)
    data=[]
    if not dtpdatas:
        if not todate:
            todate=datetime.utcnow()
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
        if dtpinfo.dbcols.has_key('name') and dtpinfo.dbcols['name']:
            data['dtp_name']=dtpinfo.dbcols['name']
        if dtpinfo.dbcols.has_key('did') and dtpinfo.dbcols['did']:
            data['did']=dtpinfo.dbcols['did']
        if dtpinfo.dbcols.has_key('default_color') and dtpinfo.dbcols['default_color']:
            data['dtp_color']=dtpinfo.dbcols['default_color']
        if dtpinfo.dbcols.has_key('decimalseparator') and dtpinfo.dbcols['decimalseparator']:
            data['dtp_decimalseparator']=dtpinfo.dbcols['decimalseparator']
    else:
        raise exceptions.DatapointNotFoundException()
    return data

def update_datapointconfig(pid,session,data):
    dtpinfo=cassapi.get_dtpinfo(pid,{},session)
    if dtpinfo:
        if data.has_key('dtp_name'):
            dtpinfo.dbcols['name']=u''+data['dtp_name']
        if data.has_key('dtp_color'):
            if colors.validate_hexcolor(data['dtp_color']):
                dtpinfo.dbcols['default_color']=u''+data['dtp_color']
            else:
                raise exceptions.BadParametersException()
        if cassapi.update_dtp(dtpinfo,session):
            return True
        else:
            raise exceptions.DatapointUpdateException()
    else:
        raise exceptions.DatapointNotFoundException()
        
