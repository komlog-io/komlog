'''
Created on 14/12/2012

@author: jcazor
'''

import exceptions, schema
from pycassa.cassandra.ttypes import NotFoundException
import uuid
import json

class DsDtpRelation:
    def __init__(self, did=None, dtps=None, key=None, dbdict=None):
        if key:
            self.did=key
            self.dbcols = dbdict
            self.dtps = []
            for key in self.dbcols.keys():
                self.dtps.append(key)
        else:
            self.did=did
            self.dtps = dtps if dtps else []
            self.prestore()

    def prestore(self):
        self.key=self.did
        self.dbdict = {}
        for pid in self.dtps:
            self.dbdict[pid]=u''


def get_dsdtprelation(did, session):
    try:
        dbobj=session.get(schema.DsDtpRelationORM(key=did,dbdict={}))
        return DsDtpRelation(key=dbobj.key,dbdict=dbobj.dbdict)
    except NotFoundException:
        return None

class DatapointInfo:
    def __init__(self, pid=None, name=None, dtree=None, positives=None, negatives=None, did=None, key=None,dbdict=None):
        if key:
            self.pid=key
            self.dbcols = dbdict
            if self.dbcols.has_key('did'):
                self.did=uuid.UUID(self.dbcols['did'])
            if self.dbcols.has_key('positives'):
                self.dbcols['positives']=json.loads(self.dbcols['positives'])
            if self.dbcols.has_key('negatives'):
                self.dbcols['negatives']=json.loads(self.dbcols['negatives'])
            if self.dbcols.has_key('dtree'):
                self.dbcols['dtree']=json.loads(self.dbcols['dtree'])
        else:
            self.did=did
            self.pid=pid
            self.dbcols={}
            if dtree:
                dtree=json.dumps(dtree)
                self.dbcols['dtree']=dtree
            if positives:
                positives=json.dumps(positives)
                self.dbcols['positives']=positives
            if negatives:
                negatives=json.dumps(negatives)
                self.dbcols['negatives']=negatives
            if did:
                self.dbcols['did']=str(did)
            else:
                raise exceptions.ParameterNotFoundException('did')
            if name:
                self.dbcols['name']=name
            else:
                raise exceptions.ParameterNotFoundException('name')
            self.prestore()
    
    def prestore(self):
        self.key=self.pid
        self.dbdict=self.dbcols


def get_dtpinfo(pid,dbcols,session):
    try:
        kwargs={}
        if len(dbcols.keys())>0:
            kwargs['columns']=[key for key in dbcols.keys()]
        dbobj=session.get(schema.DatapointInfoORM(key=pid,dbdict={}),kwargs)
        return DatapointInfo(key=dbobj.key,dbdict=dbobj.dbdict)
    except NotFoundException:
        return None

def register_dtp(dtp,dsdtprelation,session):
    try:
        dsdtprelation.dtps.insert(0,dtp.pid)
        dsdtprelation.prestore()
        session.insert(schema.DsDtpRelationORM(key=dsdtprelation.key, dbdict=dsdtprelation.dbdict))
        session.insert(schema.DatapointInfoORM(key=dtp.key, dbdict=dtp.dbdict))
        return True
    except Exception:
        remove_dtp(dtp,dsdtprelation,session)
        return False

def remove_dtp(dtp,dsdtprelation,session):
    try:
        session.remove(schema.DatapointInfoORM(key=dtp.key, dbdict=dtp.dbdict))
        kwargs={}
        kwargs['columns']=(dtp.pid,)
        session.remove(schema.DsDtpRelationORM(key=dsdtprelation.key, dbdict=dsdtprelation.dbdict),kwargs)
        return True
    except Exception as e:
        return False

class DatasourceData:
    def __init__(self, did=None, date=None, content=None,key=None,dbdict=None):
        if key:
            self.did=uuid.UUID(key)
            self.date=dbdict.keys()[0] if len(dbdict.keys()) == 1 else dbdict.keys()
            self.content=dbdict.values()[0] if len(dbdict.values()) == 1 else dbdict.values()
        else:
            self.did = did
            self.date = date
            self.content = content # unicode
            self.prestore()

    def prestore():
        self.key=str(self.did)
        self.dbdict = {}
        self.dbdict[date]=self.content.encode('utf8')

def insert_datasourcedata(dsobj,session):
    if session.insert(schema.DatasourceDataORM(key=dsobj.key,dbdict=dsobj.dbdict)):
        return True
    else:
        return False

def get_datasourcedata(did,date,session):
    try:
        kwargs={}
        kwargs['columns']=(date,)
        dbobj=session.get(schema.DatasourceDataORM(key=did,dbdict={date:u''}),kwargs)
        return DatasourceData(key=dbobj.get_key(),dbdict=dbobj.get_dbdict())
    except NotFoundException:
        return None

def remove_datasourcedata(did,date,session):
    kwargs={'columns':(date,)}
    if session.remove(schema.DatasourceDataORM(key=did,dbdict={date:u''}),kwargs):
        return True
    else:
        return False


class DatasourceMap:
    def __init__(self, did=None, date=None, content=None,key=None,dbdict=None):
        if key:
            self.did=key
            self.date=dbdict.keys()[0] if len(dbdict.keys()) == 1 else dbdict.keys()
            self.content=dbdict.values()[0] if len(dbdict.values()) == 1 else dbdict.values()
        else:
            self.did = did
            self.date = date
            self.content = content # unicode
            self._key=self.did
            self._dbdict = {}
            self._dbdict[date]=self.content.encode('utf8')

class DatasourceMapVars:
    def __init__(self, did=None, date=None, content=None,key=None,dbdict=None):
        if key:
            self.did=key
            self.date=dbdict.keys()[0] if len(dbdict.keys()) == 1 else dbdict.keys()
            self.content=dbdict.values()[0] if len(dbdict.values()) == 1 else dbdict.values()
        else:
            self.did = did
            self.date = date
            self.content = content # unicode
            self._key=self.did
            self._dbdict = {}
            self._dbdict[date]=self.content.encode('utf8')

def insert_datasourcemap(dsmobj,dsmvobj,session):
    if session.insert(schema.DatasourceMapORM(key=dsmobj._key,dbdict=dsmobj._dbdict)) and \
       session.insert(schema.DatasourceMapVarsORM(key=dsmvobj._key,dbdict=dsmvobj._dbdict)):
        return True
    else:
        remove_datasourcemap(dsmobj.did,dsmobj.date,session)
        return False

def get_datasourcemap(did,date,session):
    try:
        kwargs={}
        kwargs['columns']=(date,)
        dbobj=session.get(schema.DatasourceMapORM(key=did,dbdict={date:u''}),kwargs)
        return DatasourceMap(key=dbobj.get_key(),dbdict=dbobj.get_dbdict())
    except NotFoundException:
        return None

def get_datasourcemapvars(did,date,session):
    try:
        kwargs={}
        kwargs['columns']=(date,)
        dbobj=session.get(schema.DatasourceMapVarsORM(key=did,dbdict={date:u''}),kwargs)
        return DatasourceMapVars(key=dbobj.get_key(),dbdict=dbobj.get_dbdict())
    except NotFoundException:
        return None

def remove_datasourcemap(did,date,session):
    kwargs={'columns':(date,)}
    if session.remove(schema.DatasourceMapORM(key=did,dbdict={date:u''}),kwargs) and \
       session.remove(schema.DatasourceMapVarsORM(key=did,dbdict={date:u''}),kwargs):
        return True
    else:
        return False


