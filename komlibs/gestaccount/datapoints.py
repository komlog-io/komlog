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
from komimc import messages

def get_datapointdata(pid,session,todate):
    ''' como se ha pasado por las fases de autorización y autenticación, 
    no comprobamos que el pid existe '''
    dtpdatas=cassapi.get_datapointdata(pid,session,todate=todate)
    data=[]
    if not dtpdatas:
        print 'no hay datos'
        last_date=todate-timedelta(days=1)
        print 'calculada fecha inicial'
        raise exceptions.DatapointDataNotFoundException(last_date=last_date)
    else:
        for dtpdata in dtpdatas:
            data.append((dtpdata.date.isoformat(),dtpdata.content))
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
