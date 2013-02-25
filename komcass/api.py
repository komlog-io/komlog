'''
Created on 14/12/2012

@author: jcazor
'''

import exceptions, schema
from pycassa.cassandra.ttypes import NotFoundException

class Sample(object):
    def __init__(self, sid, content=None, session=None):
        if session:
            self.dbsample = session.get(schema.SampleORM(key=str(sid)),column_count=10000)
            self.sid = self.dbsample.key
            self.dbdict = self.dbsample.dbdict #unicode? no se por que
            self.content=u''.join(self.dbdict.values())
        else:
            self.dbsample = None
            self.sid = str(sid)
            self.content = content # unicode
            self.dbdict = {}
            index = 0
            for char in self.content:
                col_name = str(str(index).zfill(9))
                self.dbdict[col_name]=char.encode('utf8')
                index+=1
    
def get_sample(sid, session):
    try:
        return Sample(sid=sid, session=session)
    except NotFoundException:
        return None

def get_sample_list(sids, session):
    samples = []
    for sid in sids:
        samples.append(Sample(sid=sid, session=session))
    return samples

def create_sample(sid, content, session):
    try:
        print 'Creando sample'
        sample = Sample(sid=sid,session=session)
    except NotFoundException:
        print 'No existe el sample en cassandra, correcto lo creamos'
        sample = Sample(sid=sid, content=content)
        session.insert(schema.SampleORM(key=sample.sid, dbdict=sample.dbdict))
    else:
        raise exceptions.AlreadyExistingSample()

def remove_sample(sid, session):
    try:
        sample = Sample(sid=sid, session=session)
    except NotFoundException:
        return True
    else:
        session.remove(schema.SampleORM(key=sample.sid))
        return True

class SampleMap(object):
    def __init__(self, sid, content=None, session=None):
        if session:
            self.dbsample = session.get(schema.SampleMapORM(key=str(sid)), column_count=100000)
            self.sid = self.dbsample.key
            self.dbdict = self.dbsample.dbdict #utf-8 format
            self.content={}
            for key in self.dbdict.keys():
                col_name=key.decode('utf-8')
                self.content[key]=self.dbdict[key].decode('utf-8')
        else:
            self.dbsample = None
            self.sid = str(sid)
            self.content = content # unicode
            self.dbdict = {}
            for key in self.content.keys():
                col_name = str(key)
                self.dbdict[col_name]=self.content[key].encode('utf8')
          
def get_sample_map(sid, session):
    return SampleMap(sid=sid, session=session)

def create_sample_map(sid, content, session):
    try:
        print 'Creando sample Map'
        sample_m = SampleMap(sid=sid,session=session)
    except NotFoundException:
        print 'No existe el sample map en cassandra, correcto lo creamos'
        sample_m = SampleMap(sid=sid, content=content)
        session.insert(schema.SampleMapORM(key=sample_m.sid, dbdict=sample_m.dbdict))
    else:
        raise exceptions.AlreadyExistingSampleMap()

def remove_sample_map(sid, session):
    try:
        sample_m = SampleMap(sid=sid, session=session)
    except NotFoundException:
        return True
    else:
        session.remove(schema.SampleMapORM(key=sample_m.sid))
        return True
