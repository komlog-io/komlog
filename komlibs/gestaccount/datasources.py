'''
datasources.py: library for managing administrative datasource operations

creation date: 2013/03/31
author: jcazor
'''

import uuid
from datetime import datetime
from komcass import api as cassapi
from komlibs.gestaccount import states,types

def create_datasource(aid,dsname,dstype,dsparams,session):
    now=datetime.utcnow()
    did=uuid.uuid4()
    kwargs={}
    if dstype == types.DATASOURCE['SCRIPT']:
        kwargs['script_name']=dsparams['script_name']
        kwargs['day_of_week']=dsparams['day_of_week']
        kwargs['month']=dsparams['month']
        kwargs['day_of_month']=dsparams['day_of_month']
        kwargs['hour']=dsparams['hour']
        kwargs['minute']=dsparams['minute']
    dsinfo=cassapi.DatasourceInfo(did=did,aid=aid,dsname=dsname,dstype=dstype,creation_date=now,state=states.DATASOURCE['ACTIVE'],**kwargs)
    if cassapi.register_datasource(dsinfo, session):
        return True
    else:
        return False
