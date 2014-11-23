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
from komlibs.gestaccount import exceptions
from komlibs.general import colors

def get_datapoint_data(pid,end_date=None,start_date=None):
    ''' como se ha pasado por las fases de autorización y autenticación, 
    no comprobamos que el pid existe '''
    if not end_date:
        datapoint_stats=cassapidatapoint.get_datapoint_stats(pid=pid)
        end_date=datapoint_stats.last_received if datapoint_stats and datapoint_stats.last_received else datetime.utcnow()
    if not start_date:
        start_date=end_date-timedelta(days=1)
    datapoint_data_list=cassapidatapoint.get_datapoint_data(pid=pid,fromdate=start_date,todate=end_date)
    data=[]
    if not datapoint_data_list:
        last_date=end_date-timedelta(days=1)
        raise exceptions.DatapointDataNotFoundException(last_date=last_date)
    else:
        for datapoint_data in datapoint_data_list:
            data.append({'date':datapoint_data.date.isoformat()+'Z','value':str(datapoint_data.value)})
    return data

def create_datapoint(did, datapointname, position, length):
    '''
    Funcion utilizada para la monitorización de una variable y
    la creación del datapoint correspondiente
    '''
    datasource=cassapidatasource.get_datasource(did=did)
    if not datasource:
        raise exceptions.DatasourceNotFoundException()
    pid=uuid.uuid4()
    datapoint=ormdatapoint.Datapoint(pid=pid,did=did,datapointname=datapointname,creation_date=datetime.utcnow())
    if cassapidatapoint.new_datapoint(datapoint) and cassapidatapoint.set_datapoint_dtree_positive_at(pid=pid, date=date, position=int(position), length=int(length)):
        return datapoint
    else:
        raise exceptions.DatapointCreationException()

def get_datapoint_config(pid):
    ''' como se ha pasado por las fases de autorización y autenticación, 
    no comprobamos que el pid existe '''
    datapoint=cassapidatapoint.get_datapoint(pid=pid)
    datapoint_stats=cassapidatapoint.get_datapoint_stats(pid=pid)
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

def update_datapoint_config(pid,data):
    datapoint=cassapidatapoint.get_datapoint(pid=pid)
    if datapoint:
        if 'name' in data:
            datapoint.datapointname=''+data['name']
        if 'color' in data:
            if colors.validate_hexcolor(data['color']):
                datapoint.color=''+data['color']
            else:
                raise exceptions.BadParametersException()
        if cassapidatapoint.insert_datapoint(datapoint):
            return True
        else:
            raise exceptions.DatapointUpdateException()
    else:
        raise exceptions.DatapointNotFoundException()
        
