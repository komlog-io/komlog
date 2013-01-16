'''
Created on 14/12/2012

@author: jcazor
'''

import exceptions, schema
from pycassa.cassandra.ttypes import NotFoundException

class Sample(object):
    def __init__(self, sid, content=None, session=None):
        if session:
            self.dbsample = session.get(schema.SampleORM(key=str(sid)))
            self.sid = self.dbsample.sid
            self.dbdict = self.dbsample.dbdict #utf-8 format
            self.content = ''.join(self.dbdict.values()).decode('utf8')
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
    return Sample(sid=sid, session=session)

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
        
            