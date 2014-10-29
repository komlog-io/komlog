#coding: utf-8
'''
datapoint.py: library for managing datapoints operations

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
from komcass.api import datapoint as cassapidatapoint
from komlibs.gestaccount import states,types,exceptions
from komlibs.general import colors
from komimc import messages

def get_datapoint_data(pid,session,end_date=None,start_date=None):
    ''' como se ha pasado por las fases de autorización y autenticación, 
    no comprobamos que el pid existe '''
    print 'entramos aqui'
    print 'Recibimos: '+str(end_date)+' - '+str(start_date)
    if not end_date:
        end_date=datetime.utcnow()
    if not start_date:
        start_date=end_date-timedelta(days=1)
    datapoint_data_list=cassapidatapoint.get_datapoint_data(session,pid=pid,fromdate=start_date,todate=end_date)
    print 'salimos'
    data=[]
    if not datapoint_data_list:
        last_date=end_date-timedelta(days=1)
        raise exceptions.DatapointDataNotFoundException(last_date=last_date)
    else:
        for datapoint_data in datapoint_data_list:
            data.append({'date':datapoint_data.date.isoformat()+'Z','value':str(datapoint_data.value)})
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

def get_datapoint_config(pid,session):
    ''' como se ha pasado por las fases de autorización y autenticación, 
    no comprobamos que el pid existe '''
    datapoint=cassapidatapoint.get_datapoint(session, pid=pid)
    datapoint_stats=cassapidatapoint.get_datapoint_stats(session, pid=pid)
    data={}
    data['pid']=str(pid)
    if datapoint:
        data['name']=datapoint.datapointname if datapoint.datapointname else ''
        data['did']=str(datapoint.did) if datapoint.did else ''
        data['color']=datapoint.color if datapoint.color else ''
        if datapoint_stats:
            data['decimalseparator']=datapoint_stats.decimal_separator if datapoint_stats.decimal_separator else ''
    else:
        raise exceptions.DatapointNotFoundException()
    return data

def update_datapoint_config(pid,session,data):
    datapoint=cassapidatapoint.get_datapoint(session, pid=pid)
    if datapoint:
        if data.has_key('name'):
            datapoint.datapointname=u''+data['name']
        if data.has_key('color'):
            if colors.validate_hexcolor(data['color']):
                datapoint.color=u''+data['color']
            else:
                raise exceptions.BadParametersException()
        if cassapidatapoint.insert_datapoint(session, datapoint):
            return True
        else:
            raise exceptions.DatapointUpdateException()
    else:
        raise exceptions.DatapointNotFoundException()
        
