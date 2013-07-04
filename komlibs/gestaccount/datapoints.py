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
from datetime import timedelta
from komcass import api as cassapi
from komlibs.gestaccount import states,types,exceptions

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

